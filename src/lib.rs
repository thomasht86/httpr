#![allow(clippy::too_many_arguments)]
use std::sync::{Arc, LazyLock, Mutex};
use std::time::Duration;
use std::{fs, str};

use anyhow::anyhow;
use bytes::Bytes;
use foldhash::fast::RandomState;
use indexmap::IndexMap;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict};
use pythonize::depythonize;
use reqwest::{
    header::{HeaderValue, COOKIE},
    multipart,
    redirect::Policy,
    Body, Identity, Method,
};
use serde_json::Value;
use tokio::{
    fs::File,
    runtime::{self, Runtime},
};
use tokio_util::codec::{BytesCodec, FramedRead};
use tokio_util::sync::CancellationToken;

mod response;
use response::{CaseInsensitiveHeaderMap, LineIterator, Response, StreamingResponse, TextIterator};

mod params;
use params::{merge_params, normalize_params, params_to_py, Pairs};

mod traits;
use traits::{parse_cookie_header, CookiesTraits, HeadersTraits};

mod utils;
use utils::load_ca_certs;

mod exceptions;
use exceptions::{map_anyhow_error, map_reqwest_error, ClientClosed};

mod lifecycle;
use lifecycle::ClientState;

type IndexMapSSR = IndexMap<String, String, RandomState>;

// Tokio global one-thread runtime
static RUNTIME: LazyLock<Runtime> = LazyLock::new(|| {
    runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .expect("Failed to initialize Tokio runtime")
});

/// Error message for any operation on a client after `close()`; mirrors httpx.
const CLIENT_CLOSED_MSG: &str = "Cannot send a request, as the client has been closed.";

/// The constructor settings a rebuilt `reqwest::Client` has to carry over, so
/// that assigning `client.proxy` keeps TLS verification, the CA bundle, the
/// mTLS identity, redirects, `https_only` and the HTTP version (issue #84).
/// Certificates and the identity are kept in their loaded form; a rebuild never
/// touches the filesystem again.
struct ClientConfig {
    cookie_store: bool,
    referer: bool,
    /// `Some(max)` follows up to `max` redirects, `None` follows none.
    max_redirects: Option<usize>,
    verify: bool,
    root_certs: Vec<reqwest::Certificate>,
    identity: Option<Identity>,
    https_only: bool,
    http2_only: bool,
}

impl ClientConfig {
    /// Builds a client from these settings plus the state that lives on the
    /// `RClient` and may have changed since construction: the default headers,
    /// the proxy and the timeout. `layer` must come from the `ClientState` the
    /// client will live in, so `close()` can cancel its pending connects.
    fn build(
        &self,
        layer: lifecycle::CancelConnectsLayer,
        default_headers: reqwest::header::HeaderMap,
        proxy: Option<&str>,
        timeout: Option<f64>,
    ) -> PyResult<reqwest::Client> {
        let mut builder = reqwest::Client::builder()
            .connector_layer(layer)
            .cookie_store(self.cookie_store)
            .referer(self.referer)
            .redirect(match self.max_redirects {
                Some(max) => Policy::limited(max),
                None => Policy::none(),
            })
            .https_only(self.https_only);
        if !default_headers.is_empty() {
            builder = builder.default_headers(default_headers);
        }
        if let Some(proxy) = proxy {
            builder = builder.proxy(reqwest::Proxy::all(proxy).map_err(map_reqwest_error)?);
        }
        if let Some(seconds) = timeout {
            builder = builder.timeout(Duration::from_secs_f64(seconds));
        }
        if self.verify {
            builder = builder.tls_built_in_root_certs(true);
            for cert in &self.root_certs {
                builder = builder.add_root_certificate(cert.clone());
            }
        } else {
            builder = builder.danger_accept_invalid_certs(true);
        }
        // The mTLS identity applies regardless of `verify`: disabling server
        // verification doesn't imply disabling client authentication.
        if let Some(identity) = &self.identity {
            builder = builder.identity(identity.clone());
        }
        if self.http2_only {
            builder = builder.http2_prior_knowledge();
        }
        builder.build().map_err(map_reqwest_error)
    }
}

#[pyclass(subclass)]
/// HTTP client that can impersonate web browsers.
pub struct RClient {
    /// The `reqwest::Client`, its in-flight count and the cancellation token
    /// for its pending connects; shared with the requests in flight so that
    /// `close()` can release the pool no matter who drops it last. See
    /// `lifecycle.rs`.
    state: Arc<ClientState>,
    /// What `set_proxy` rebuilds the client from.
    config: ClientConfig,
    headers: Arc<Mutex<reqwest::header::HeaderMap>>,
    #[pyo3(get, set)]
    auth: Option<(String, Option<String>)>,
    #[pyo3(get, set)]
    auth_bearer: Option<String>,
    /// Client-level query parameters, merged into every request (see `params.rs`).
    params: Option<Pairs>,
    #[pyo3(get, set)]
    proxy: Option<String>,
    #[pyo3(get, set)]
    timeout: Option<f64>,
}

impl RClient {
    /// A handle to the underlying `reqwest::Client` plus the in-flight guard
    /// for one request, or `ClientClosed` if `close()` has been called.
    fn begin_request(&self) -> PyResult<(reqwest::Client, lifecycle::InFlight)> {
        self.state
            .begin_request()
            .ok_or_else(|| ClientClosed::new_err(CLIENT_CLOSED_MSG))
    }
}

impl Drop for RClient {
    /// A client that is garbage-collected without `close()` still releases its
    /// pool. Safe to drive the runtime from here: every `block_on` in this
    /// crate runs with the GIL released, so the thread deallocating a Python
    /// object is never inside one.
    fn drop(&mut self) {
        self.state.close();
    }
}

impl RClient {
    /// Everything about a request that is settled before it is sent: the
    /// builder with query, headers, cookies, body, auth and timeout applied.
    /// `files` are attached by `send_request`, since opening them is async.
    /// Shared by `request()` and `_stream()`.
    ///
    /// `client` is consumed so that the only remaining handle to the pool is
    /// the one inside the returned builder, which the caller's future drops
    /// before its `InFlight` guard (see `lifecycle.rs`).
    fn build_request(
        &self,
        client: reqwest::Client,
        method: &str,
        url: &str,
        params: Option<&Bound<'_, PyAny>>,
        headers: Option<IndexMapSSR>,
        cookies: Option<IndexMapSSR>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyAny>>,
        json: Option<&Bound<'_, PyAny>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<reqwest::RequestBuilder> {
        let method = Method::from_bytes(method.as_bytes())
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let mut builder = client.request(method, url);

        // Query: client-level params first, then the request's own; a key the
        // request supplies replaces the client's values for it (issue #82).
        let request_params = params
            .map(|p| normalize_params(p, "params"))
            .transpose()?
            .unwrap_or_default();
        let params = merge_params(self.params.as_deref().unwrap_or(&[]), request_params);
        if !params.is_empty() {
            builder = builder.query(&params);
        }

        // Headers from client, then per-request headers replacing same-named
        // entries, so the request's values take precedence.
        let mut header_map = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?
            .clone();
        if let Some(headers) = headers {
            for (name, value) in headers.to_headermap().iter() {
                header_map.insert(name.clone(), value.clone());
            }
        }

        // Cookies: per-request cookies are merged into the client's `Cookie`
        // header (request wins per name) so exactly one header goes out
        // (RFC 6265 §5.4, issue #82).
        if let Some(cookies) = cookies {
            let mut merged = match header_map.get(COOKIE) {
                Some(existing) => parse_cookie_header(
                    existing
                        .to_str()
                        .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?,
                ),
                None => IndexMap::with_hasher(RandomState::default()),
            };
            merged.extend(cookies);
            header_map.insert(
                COOKIE,
                HeaderValue::from_str(&merged.to_string())
                    .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?,
            );
        }
        builder = builder.headers(header_map);

        // Body: sent for any method the caller supplies one for (RFC 9110, matches httpx)
        if let Some(content) = content {
            builder = builder.body(content);
        }
        // Form data goes through the same normalisation as query params, so
        // list values become repeated fields and insertion order is kept.
        if let Some(data) = data {
            builder = builder.form(&normalize_params(data, "data")?);
        }
        // Json - always serialize as JSON regardless of Accept header
        if let Some(json) = json {
            let json_value: Value =
                depythonize(json).map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
            builder = builder.json(&json_value);
        }

        // Auth
        if let Some((username, password)) = auth.or_else(|| self.auth.clone()) {
            builder = builder.basic_auth(username, password);
        } else if let Some(token) = auth_bearer.or_else(|| self.auth_bearer.clone()) {
            builder = builder.bearer_auth(token);
        }

        // Timeout
        if let Some(seconds) = timeout.or(self.timeout) {
            builder = builder.timeout(Duration::from_secs_f64(seconds));
        }

        Ok(builder)
    }
}

/// Attaches `files` as a multipart form, if any, and sends the request.
async fn send_request(
    mut builder: reqwest::RequestBuilder,
    files: Option<IndexMap<String, String>>,
) -> anyhow::Result<reqwest::Response> {
    if let Some(files) = files {
        let mut form = multipart::Form::new();
        for (file_name, file_path) in files {
            let file = File::open(file_path).await.map_err(anyhow::Error::new)?;
            let stream = FramedRead::new(file, BytesCodec::new());
            let file_body = Body::wrap_stream(stream);
            let part = multipart::Part::stream(file_body).file_name(file_name.clone());
            form = form.part(file_name, part);
        }
        builder = builder.multipart(form);
    }
    builder.send().await.map_err(anyhow::Error::new)
}

/// Cookies, headers, status and final URL of a response.
fn response_meta(resp: &reqwest::Response) -> (IndexMapSSR, IndexMapSSR, u16, String) {
    let cookies: IndexMapSSR = resp
        .cookies()
        .map(|cookie| (cookie.name().to_string(), cookie.value().to_string()))
        .collect();
    let headers: IndexMapSSR = resp.headers().to_indexmap();
    (
        cookies,
        headers,
        resp.status().as_u16(),
        resp.url().to_string(),
    )
}

#[pymethods]
impl RClient {
    /// Initializes an HTTP client that can impersonate web browsers.
    ///
    /// This function creates a new HTTP client instance.
    /// It allows for customization of headers, proxy settings, timeout, SSL certificate verification,
    /// and HTTP version preferences.
    ///
    /// # Arguments
    ///
    /// * `auth` - A tuple containing the username and an optional password for basic authentication. Default is None.
    /// * `auth_bearer` - A string representing the bearer token for bearer token authentication. Default is None.
    /// * `params` - A map of query parameters to append to the URL. Default is None.
    /// * `headers` - An optional map of HTTP headers to send with requests.
    /// * `cookies` - An optional map of cookies to send with requests as the `Cookie` header.
    /// * `cookie_store` - Enable a persistent cookie store. Received cookies will be preserved and included
    ///         in additional requests. Default is `true`.
    /// * `referer` - Enable or disable automatic setting of the `Referer` header. Default is `true`.
    /// * `proxy` - An optional proxy URL for HTTP requests.
    /// * `timeout` - An optional timeout for HTTP requests in seconds.
    /// * `follow_redirects` - A boolean to enable or disable following redirects. Default is `true`.
    /// * `max_redirects` - The maximum number of redirects to follow. Default is 20. Applies if `follow_redirects` is `true`.
    /// * `verify` - An optional boolean indicating whether to verify SSL certificates. Default is `true`.
    /// * `ca_cert_file` - Path to CA certificate store. Default is None.
    /// * `https_only` - Restrict the Client to be used with HTTPS only requests. Default is `false`.
    /// * `http2_only` - If true - use only HTTP/2, if false - use only HTTP/1. Default is `false`.
    ///
    /// # Example
    ///
    /// ```
    /// from httpr import Client
    ///
    /// client = Client(
    ///     auth=("name", "password"),
    ///     params={"p1k": "p1v", "p2k": "p2v"},
    ///     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"},
    ///     cookies={"ck1": "cv1", "ck2": "cv2"},
    ///     cookie_store=False,
    ///     referer=False,
    ///     proxy="http://127.0.0.1:8080",
    ///     timeout=10,
    ///     follow_redirects=True,
    ///     max_redirects=1,
    ///     verify=True,
    ///     ca_cert_file="/cert/cacert.pem",
    ///     client_pem="/cert/client.pem",
    ///     https_only=True,
    ///     http2_only=True,
    /// )
    /// ```
    #[new]
    #[pyo3(signature = (auth=None, auth_bearer=None, params=None, headers=None, cookies=None,
        cookie_store=true, referer=true, proxy=None, timeout=None, follow_redirects=true,
        max_redirects=20, verify=true, ca_cert_file=None, client_pem=None, client_pem_data=None, https_only=false, http2_only=false))]
    fn new(
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        params: Option<&Bound<'_, PyAny>>,
        headers: Option<IndexMapSSR>,
        cookies: Option<IndexMapSSR>,
        cookie_store: Option<bool>,
        referer: Option<bool>,
        proxy: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        max_redirects: Option<usize>,
        verify: Option<bool>,
        ca_cert_file: Option<String>,
        client_pem: Option<String>,
        client_pem_data: Option<Vec<u8>>,
        https_only: Option<bool>,
        http2_only: Option<bool>,
    ) -> PyResult<Self> {
        if client_pem.is_some() && client_pem_data.is_some() {
            return Err(PyValueError::new_err(
                "Only one of client_pem or client_pem_data may be set.",
            ));
        }
        let params = params.map(|p| normalize_params(p, "params")).transpose()?;

        // Headers || Cookies
        let headers_headermap = if headers.is_some() || cookies.is_some() {
            let headers = headers.unwrap_or_else(|| IndexMap::with_hasher(RandomState::default()));
            let mut headers_headermap = headers.to_headermap();
            if let Some(cookies) = cookies {
                let cookies_str = cookies.to_string();
                headers_headermap.insert(
                    COOKIE,
                    HeaderValue::from_str(&cookies_str)
                        .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?,
                );
            }
            headers_headermap
        } else {
            reqwest::header::HeaderMap::new()
        };

        // Proxy: the argument wins, otherwise HTTPR_PROXY. Read once, here;
        // `set_proxy` never consults the environment again.
        let proxy = proxy.or_else(|| std::env::var("HTTPR_PROXY").ok());

        // CA bundle: the explicit `ca_cert_file` argument wins, otherwise fall back
        // to the HTTPR_CA_BUNDLE environment variable. The environment is only
        // ever read here, never written, so the setting stays scoped to this
        // client (mirrors how `proxy` falls back to HTTPR_PROXY above).
        let ca_cert_file = ca_cert_file.or_else(|| std::env::var("HTTPR_CA_BUNDLE").ok());
        let verify = verify.unwrap_or(true);
        let root_certs = if verify {
            load_ca_certs(ca_cert_file.as_deref()).map_err(map_anyhow_error)?
        } else {
            Vec::new()
        };

        // Client mTLS identity, from bytes or from a file read once here.
        let identity_pem = if let Some(pem_data) = client_pem_data {
            Some(pem_data)
        } else if let Some(pem_path) = &client_pem {
            Some(fs::read(pem_path).map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?)
        } else {
            None
        };
        let identity = identity_pem
            .map(|pem| Identity::from_pem(&pem).map_err(map_reqwest_error))
            .transpose()?;

        let config = ClientConfig {
            cookie_store: cookie_store.unwrap_or(true),
            referer: referer.unwrap_or(true),
            max_redirects: follow_redirects
                .unwrap_or(true)
                .then(|| max_redirects.unwrap_or(20)),
            verify,
            root_certs,
            identity,
            https_only: https_only.unwrap_or(false),
            http2_only: http2_only.unwrap_or(false),
        };

        let connects = CancellationToken::new();
        let client = config.build(
            lifecycle::CancelConnectsLayer::new(connects.clone()),
            headers_headermap.clone(),
            proxy.as_deref(),
            timeout,
        )?;
        let headers = Arc::new(Mutex::new(headers_headermap));

        Ok(RClient {
            state: ClientState::new(client, connects),
            config,
            headers,
            auth,
            auth_bearer,
            params,
            proxy,
            timeout,
        })
    }

    #[getter]
    pub fn get_headers(&self) -> PyResult<IndexMapSSR> {
        let headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        let mut headers_clone = headers.clone();
        headers_clone.remove(COOKIE);
        Ok(headers_clone.to_indexmap())
    }

    #[setter]
    pub fn set_headers(&self, new_headers: Option<IndexMapSSR>) -> PyResult<()> {
        let mut headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        let cookie = headers.get(COOKIE).cloned();
        headers.clear();
        if let Some(cookie) = cookie {
            headers.insert(COOKIE, cookie);
        }
        if let Some(new_headers) = new_headers {
            for (k, v) in new_headers {
                headers.insert_key_value(k, v).map_err(map_anyhow_error)?
            }
        }
        Ok(())
    }

    pub fn set_header(&self, key: String, value: String) -> PyResult<()> {
        let mut headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        headers
            .insert_key_value(key, value)
            .map_err(map_anyhow_error)
    }

    pub fn del_header(&self, key: String) -> PyResult<()> {
        let mut headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        headers.remove(key.as_str());
        Ok(())
    }

    #[getter]
    pub fn get_cookies(&self) -> PyResult<IndexMapSSR> {
        let headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        match headers.get(COOKIE) {
            Some(cookie_header) => Ok(parse_cookie_header(
                cookie_header
                    .to_str()
                    .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?,
            )),
            None => Ok(IndexMap::with_hasher(RandomState::default())),
        }
    }

    #[setter]
    pub fn set_cookies(&self, cookies: Option<IndexMapSSR>) -> PyResult<()> {
        let mut headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?;
        if let Some(cookies) = cookies {
            headers.insert(
                COOKIE,
                HeaderValue::from_str(&cookies.to_string())
                    .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?,
            );
        } else {
            headers.remove(COOKIE);
        }
        Ok(())
    }

    /// Client-level query parameters as a dict; a key given more than once
    /// maps to a `list[str]`. Assigning the result back reproduces the same
    /// parameters.
    #[getter]
    pub fn get_params<'py>(&self, py: Python<'py>) -> PyResult<Option<Bound<'py, PyDict>>> {
        self.params
            .as_deref()
            .map(|pairs| params_to_py(py, pairs))
            .transpose()
    }

    #[setter]
    pub fn set_params(&mut self, params: Option<&Bound<'_, PyAny>>) -> PyResult<()> {
        self.params = params.map(|p| normalize_params(p, "params")).transpose()?;
        Ok(())
    }

    #[getter]
    pub fn get_proxy(&self) -> PyResult<Option<String>> {
        Ok(self.proxy.to_owned())
    }

    /// Rebuilds the underlying `reqwest::Client` with the new proxy (`None`
    /// removes it; `HTTPR_PROXY` is not consulted again). Every other setting
    /// from construction is carried over, along with the current default
    /// headers and timeout; a `cookie_store` starts empty again. The old pool
    /// is dropped and its idle connections are released; a connect the old
    /// pool still had pending in the background is left to resolve on its own
    /// (it is torn down the next time the runtime is driven). Raises
    /// `ClientClosed` on a closed client.
    #[setter]
    pub fn set_proxy(&mut self, py: Python, proxy: Option<String>) -> PyResult<()> {
        let default_headers = self
            .headers
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire headers lock: {}", e)))?
            .clone();
        let new_client = self.config.build(
            self.state.connector_layer(),
            default_headers,
            proxy.as_deref(),
            self.timeout,
        )?;
        if !py.detach(|| self.state.replace(new_client)) {
            return Err(ClientClosed::new_err(CLIENT_CLOSED_MSG));
        }
        self.proxy = proxy;
        Ok(())
    }

    /// Whether `close()` has been called on this client.
    #[getter]
    pub fn is_closed(&self) -> bool {
        self.state.is_closed()
    }

    /// Close the client and release its connection pool.
    ///
    /// Drops the underlying `reqwest::Client` and cancels any connect the pool
    /// still had pending, so idle pooled connections are shut down before this
    /// returns. Requests already in flight hold their own handle to the pool
    /// and finish normally; while any of them is running the pool, including
    /// its idle connections, stays alive, and the last one to finish releases
    /// it. Any later request on this client raises `ClientClosed`. Calling
    /// `close()` more than once is a no-op.
    pub fn close(&self, py: Python) {
        py.detach(|| self.state.close());
    }

    /// Constructs an HTTP request with the given method, URL, and optionally sets a timeout, headers, and query parameters.
    /// Sends the request and returns a `Response` object containing the server's response.
    ///
    /// # Arguments
    ///
    /// * `method` - The HTTP method to use (e.g., "GET", "POST").
    /// * `url` - The URL to which the request will be made.
    /// * `params` - A map of query parameters to append to the URL. Default is None.
    /// * `headers` - A map of HTTP headers to send with the request. Default is None.
    /// * `cookies` - An optional map of cookies to send with requests as the `Cookie` header.
    /// * `content` - The content to send in the request body as bytes. Default is None.
    /// * `data` - The form data to send in the request body. Default is None.
    /// * `json` -  A JSON serializable object to send in the request body. Default is None.
    /// * `cbor` -  A CBOR serializable object to send in the request body. Default is None.
    /// * `files` - A map of file fields to file paths to be sent as multipart/form-data. Default is None.
    /// * `auth` - A tuple containing the username and an optional password for basic authentication. Default is None.
    /// * `auth_bearer` - A string representing the bearer token for bearer token authentication. Default is None.
    /// * `timeout` - The timeout for the request in seconds. Default is 30.
    ///
    /// # Returns
    ///
    /// * `Response` - A response object containing the server's response to the request.
    ///
    /// # Errors
    ///
    /// Raises specific exceptions based on the error type:
    /// * `InvalidURL` - If the URL is malformed
    /// * `ConnectTimeout` - If connection times out
    /// * `ReadTimeout` - If reading response times out
    /// * `WriteTimeout` - If writing request times out
    /// * `ConnectError` - If connection fails
    /// * `ReadError` - If reading response fails
    /// * `ProxyError` - If proxy connection fails
    /// * `TooManyRedirects` - If too many redirects occur
    /// * `HTTPStatusError` - If HTTP status is 4xx or 5xx
    /// * `RequestError` - For other request failures
    #[pyo3(signature = (method, url, params=None, headers=None, cookies=None, content=None,
        data=None, json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn request(
        &self,
        py: Python,
        method: &str,
        url: &str,
        params: Option<&Bound<'_, PyAny>>,
        headers: Option<IndexMapSSR>,
        cookies: Option<IndexMapSSR>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyAny>>,
        json: Option<&Bound<'_, PyAny>>,
        files: Option<IndexMap<String, String>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        let (client, in_flight) = self.begin_request()?;
        let builder = self.build_request(
            client,
            method,
            url,
            params,
            headers,
            cookies,
            content,
            data,
            json,
            auth,
            auth_bearer,
            timeout,
        )?;

        let future = async move {
            let resp = send_request(builder, files).await?;
            let (cookies, headers, status_code, url) = response_meta(&resp);
            let buf = resp.bytes().await.map_err(anyhow::Error::new)?;

            tracing::info!("response: {} {} {}", url, status_code, buf.len());
            Ok::<(Bytes, IndexMapSSR, IndexMapSSR, u16, String), anyhow::Error>((
                buf,
                cookies,
                headers,
                status_code,
                url,
            ))
        };

        // Execute an async future, releasing the Python GIL for concurrency.
        // Use Tokio global runtime to block on the future.
        let result = py.detach(|| {
            // The future owns the request builder and with it our clone of the
            // reqwest client, which kept the pool alive for the duration of the
            // request; `block_on` drops both.
            let result = RUNTIME.block_on(future);
            // If `close()` ran in the meantime, ending this request is what
            // really tears the pool down, and the guard releases its sockets.
            drop(in_flight);
            result
        });
        let (f_buf, f_cookies, f_headers, f_status_code, f_url) =
            result.map_err(map_anyhow_error)?;

        Ok(Response {
            content: PyBytes::new(py, &f_buf).unbind(),
            cookies: f_cookies,
            encoding: String::new(),
            headers: CaseInsensitiveHeaderMap::from_indexmap(f_headers),
            status_code: f_status_code,
            url: f_url,
        })
    }

    /// Constructs an HTTP request and returns a StreamingResponse for iterating over chunks.
    ///
    /// Unlike `request()`, this method does not buffer the entire response body.
    /// Instead, it returns a `StreamingResponse` that can be iterated to receive chunks
    /// as they arrive from the server.
    ///
    /// # Arguments
    ///
    /// Same as `request()`.
    ///
    /// # Returns
    ///
    /// * `StreamingResponse` - A streaming response object that can be iterated.
    ///
    /// # Example
    ///
    /// ```python
    /// with client.stream("GET", url) as response:
    ///     for chunk in response.iter_bytes():
    ///         process(chunk)
    /// ```
    #[pyo3(signature = (method, url, params=None, headers=None, cookies=None, content=None,
        data=None, json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn _stream(
        &self,
        py: Python,
        method: &str,
        url: &str,
        params: Option<&Bound<'_, PyAny>>,
        headers: Option<IndexMapSSR>,
        cookies: Option<IndexMapSSR>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyAny>>,
        json: Option<&Bound<'_, PyAny>>,
        files: Option<IndexMap<String, String>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<StreamingResponse> {
        let (client, in_flight) = self.begin_request()?;
        let builder = self.build_request(
            client,
            method,
            url,
            params,
            headers,
            cookies,
            content,
            data,
            json,
            auth,
            auth_bearer,
            timeout,
        )?;

        let future = async move {
            // Send the request and await the response (but don't read body)
            let resp = send_request(builder, files).await?;
            let (cookies, headers, status_code, url) = response_meta(&resp);

            tracing::info!("streaming response: {} {}", url, status_code);
            Ok::<(reqwest::Response, IndexMapSSR, IndexMapSSR, u16, String), anyhow::Error>((
                resp,
                cookies,
                headers,
                status_code,
                url,
            ))
        };

        // Execute an async future, releasing the Python GIL for concurrency.
        let result = py.detach(|| RUNTIME.block_on(future));
        let (f_resp, f_cookies, f_headers, f_status_code, f_url) =
            result.map_err(map_anyhow_error)?;

        // The response keeps the request in flight until it is closed: its
        // connection stays busy, and a `close()` meanwhile must wait for it.
        Ok(StreamingResponse::new(
            f_resp,
            in_flight,
            f_cookies,
            CaseInsensitiveHeaderMap::from_indexmap(f_headers),
            f_status_code,
            f_url,
        ))
    }
}

#[pymodule(gil_used = false)]
fn httpr(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    pyo3_log::init();

    m.add_class::<RClient>()?;
    m.add_class::<Response>()?;
    m.add_class::<StreamingResponse>()?;
    m.add_class::<CaseInsensitiveHeaderMap>()?;
    m.add_class::<TextIterator>()?;
    m.add_class::<LineIterator>()?;
    m.add("_CLIENT_CLOSED_MSG", CLIENT_CLOSED_MSG)?;

    // Register all exception types
    exceptions::register_exceptions(m)?;

    Ok(())
}
