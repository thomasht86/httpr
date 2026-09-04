#![allow(clippy::too_many_arguments)]
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, LazyLock, Mutex};
use std::time::Duration;
use std::{fs, str};

use anyhow::anyhow;
use bytes::Bytes;
use foldhash::fast::RandomState;
use indexmap::IndexMap;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
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

mod response;
use response::{CaseInsensitiveHeaderMap, LineIterator, Response, StreamingResponse, TextIterator};

mod traits;
use traits::{CookiesTraits, HeadersTraits};

mod utils;
use utils::load_ca_certs;

mod exceptions;
use exceptions::{map_anyhow_error, map_reqwest_error, ClientClosed};

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

/// How many scheduler turns `close()` gives the runtime so the connection
/// tasks belonging to the dropped pool can observe the hang-up and shut their
/// sockets down. Each turn is a `yield_now`, so this is microseconds of work.
const CLOSE_SCHEDULER_TURNS: usize = 16;

/// Timer tick used when `close()` has to wait for I/O (see
/// `settle_dropped_pool`). tokio's timer wheel has millisecond resolution, so
/// this is the smallest useful value.
const CLOSE_SETTLE_TICK: Duration = Duration::from_millis(1);

/// Upper bound on those ticks, so a stalled remote handshake cannot make
/// `close()` hang. Whatever is still pending afterwards is torn down the next
/// time the runtime is driven.
const CLOSE_MAX_SETTLE_ROUNDS: usize = 8;

#[pyclass(subclass)]
/// HTTP client that can impersonate web browsers.
pub struct RClient {
    /// `None` once `close()` has been called. Dropping the `reqwest::Client`
    /// drops its connection pool, which is what actually releases the sockets.
    client: Mutex<Option<reqwest::Client>>,
    /// Requests currently inside `request()` / `_stream()`.
    in_flight: AtomicUsize,
    /// Set once two requests have overlapped on this client. That is the only
    /// way hyper can end up racing a fresh connect against an idle-pool
    /// checkout, which is the one case where `close()` has to wait on I/O; see
    /// `settle_dropped_pool`. Sequential clients (including the temporary one
    /// behind `httpr.get()`) never pay for that wait.
    saw_concurrency: AtomicBool,
    headers: Arc<Mutex<reqwest::header::HeaderMap>>,
    #[pyo3(get, set)]
    auth: Option<(String, Option<String>)>,
    #[pyo3(get, set)]
    auth_bearer: Option<String>,
    #[pyo3(get, set)]
    params: Option<IndexMapSSR>,
    #[pyo3(get, set)]
    proxy: Option<String>,
    #[pyo3(get, set)]
    timeout: Option<f64>,
}

/// Drive the single-threaded RUNTIME so a just-dropped connection pool actually
/// releases its sockets. Must be called with the GIL released.
///
/// Pooled connections live in tasks spawned on RUNTIME, which only makes
/// progress inside `block_on`. Dropping a pool hands each idle connection task
/// a hang-up, but the socket is not shut down until that task is polled again,
/// so first give the scheduler a few turns instead of leaving the FIN for the
/// next unrelated request. This part is deterministic and takes microseconds.
///
/// `wait_for_connects` covers the one case yielding cannot: when requests
/// overlap, hyper races a fresh connect against the idle-pool checkout and, if
/// the checkout wins, finishes the connect in the background so the socket is
/// not wasted. That connect future holds the pool alive until it resolves, and
/// resolving needs I/O readiness that `yield_now` never waits for. So drive the
/// I/O driver a timer tick at a time until the runtime's task population has
/// stopped changing, with a small cap. Anything still pending after the cap
/// (e.g. a slow remote TLS handshake) is torn down the next time the runtime
/// is driven.
fn settle_dropped_pool(wait_for_connects: bool) {
    RUNTIME.block_on(async {
        for _ in 0..CLOSE_SCHEDULER_TURNS {
            tokio::task::yield_now().await;
        }
        if !wait_for_connects {
            return;
        }
        let metrics = RUNTIME.metrics();
        let mut alive = metrics.num_alive_tasks();
        let mut stable_rounds = 0;
        for _ in 0..CLOSE_MAX_SETTLE_ROUNDS {
            tokio::time::sleep(CLOSE_SETTLE_TICK).await;
            let now = metrics.num_alive_tasks();
            if now == alive {
                // Two quiet ticks in a row: a connect completing and its pool
                // going away take more than one tick to ripple through.
                stable_rounds += 1;
                if stable_rounds >= 2 {
                    break;
                }
            } else {
                stable_rounds = 0;
                alive = now;
            }
        }
    })
}

/// Decrements `RClient::in_flight` when the request it belongs to finishes.
struct InFlightGuard<'a>(&'a AtomicUsize);

impl Drop for InFlightGuard<'_> {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::AcqRel);
    }
}

impl RClient {
    /// `true` once `close()` has taken the client. Does not raise; for use on
    /// paths that only need to know whether pool cleanup is pending.
    fn is_closed_unchecked(&self) -> bool {
        self.client.lock().map(|c| c.is_none()).unwrap_or(false)
    }

    /// Count a request as in flight for the lifetime of the returned guard,
    /// remembering whether it overlapped with another one.
    fn track_in_flight(&self) -> InFlightGuard<'_> {
        if self.in_flight.fetch_add(1, Ordering::AcqRel) > 0 {
            self.saw_concurrency.store(true, Ordering::Relaxed);
        }
        InFlightGuard(&self.in_flight)
    }

    /// Release the sockets of a pool this client just dropped.
    fn settle(&self) {
        settle_dropped_pool(self.saw_concurrency.load(Ordering::Relaxed));
    }

    /// A handle to the underlying `reqwest::Client`, or `ClientClosed` if
    /// `close()` has been called. Cloning is cheap (it is an `Arc` inside), and
    /// taking the clone up front means a request that is already in flight keeps
    /// the pool alive even if the client is closed underneath it.
    fn reqwest_client(&self) -> PyResult<reqwest::Client> {
        self.client
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire client lock: {}", e)))?
            .clone()
            .ok_or_else(|| ClientClosed::new_err(CLIENT_CLOSED_MSG))
    }
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
        params: Option<IndexMapSSR>,
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
        // Client builder
        let mut client_builder = reqwest::Client::builder();

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
            client_builder = client_builder.default_headers(headers_headermap.clone());
            headers_headermap
        } else {
            reqwest::header::HeaderMap::new()
        };

        // Cookie_store
        if cookie_store.unwrap_or(true) {
            client_builder = client_builder.cookie_store(true);
        }

        // Referer
        if referer.unwrap_or(true) {
            client_builder = client_builder.referer(true);
        }

        // Proxy
        let proxy = proxy.or_else(|| std::env::var("HTTPR_PROXY").ok());
        if let Some(proxy) = &proxy {
            client_builder =
                client_builder.proxy(reqwest::Proxy::all(proxy).map_err(map_reqwest_error)?);
        }

        // Timeout
        if let Some(seconds) = timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(seconds));
        }

        // Redirects
        if follow_redirects.unwrap_or(true) {
            client_builder = client_builder.redirect(Policy::limited(max_redirects.unwrap_or(20)));
        } else {
            client_builder = client_builder.redirect(Policy::none());
        }

        // CA bundle: the explicit `ca_cert_file` argument wins, otherwise fall back
        // to the HTTPR_CA_BUNDLE environment variable. The environment is only
        // ever read here, never written, so the setting stays scoped to this
        // client (mirrors how `proxy` falls back to HTTPR_PROXY above).
        let ca_cert_file = ca_cert_file.or_else(|| std::env::var("HTTPR_CA_BUNDLE").ok());

        // Verify
        if verify.unwrap_or(true) {
            client_builder = client_builder.tls_built_in_root_certs(true);
            for cert in load_ca_certs(ca_cert_file.as_deref()).map_err(map_anyhow_error)? {
                client_builder = client_builder.add_root_certificate(cert);
            }
        } else {
            client_builder = client_builder.danger_accept_invalid_certs(true);
        }

        // Client mTLS identity must be applied regardless of `verify`: disabling
        // server verification doesn't imply disabling client authentication.
        let client_identity_pem = if let Some(pem_data) = &client_pem_data {
            Some(pem_data.clone())
        } else if let Some(pem_path) = &client_pem {
            Some(fs::read(pem_path).map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?)
        } else {
            None
        };

        if let Some(pem_bytes) = client_identity_pem {
            let identity = Identity::from_pem(&pem_bytes).map_err(map_reqwest_error)?;
            client_builder = client_builder.identity(identity);
        }

        // Https_only
        if let Some(true) = https_only {
            client_builder = client_builder.https_only(true);
        }

        // Http2_only
        if let Some(true) = http2_only {
            client_builder = client_builder.http2_prior_knowledge();
        }
        let client = Mutex::new(Some(client_builder.build().map_err(map_reqwest_error)?));
        let headers = Arc::new(Mutex::new(headers_headermap));

        Ok(RClient {
            client,
            in_flight: AtomicUsize::new(0),
            saw_concurrency: AtomicBool::new(false),
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
        let mut cookies: IndexMapSSR = IndexMap::with_hasher(RandomState::default());
        if let Some(cookie_header) = headers.get(COOKIE) {
            for part in cookie_header
                .to_str()
                .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?
                .split(';')
            {
                if let Some((key, value)) = part.trim().split_once('=') {
                    cookies.insert(key.to_string(), value.to_string());
                }
            }
        }
        Ok(cookies)
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

    #[getter]
    pub fn get_proxy(&self) -> PyResult<Option<String>> {
        Ok(self.proxy.to_owned())
    }

    #[setter]
    pub fn set_proxy(&mut self, proxy: String) -> PyResult<()> {
        let rproxy = reqwest::Proxy::all(proxy.clone()).map_err(map_reqwest_error)?;
        let new_client = reqwest::Client::builder()
            .proxy(rproxy)
            .build()
            .map_err(map_reqwest_error)?;
        let mut client = self
            .client
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire client lock: {}", e)))?;
        if client.is_none() {
            return Err(ClientClosed::new_err(CLIENT_CLOSED_MSG));
        }
        *client = Some(new_client);
        self.proxy = Some(proxy);
        Ok(())
    }

    /// Whether `close()` has been called on this client.
    #[getter]
    pub fn is_closed(&self) -> PyResult<bool> {
        Ok(self
            .client
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire client lock: {}", e)))?
            .is_none())
    }

    /// Close the client and release its connection pool.
    ///
    /// Drops the underlying `reqwest::Client`. Idle pooled connections are shut
    /// down; requests already in flight hold their own handle to the pool and
    /// finish normally. Any later request on this client raises `ClientClosed`.
    /// Calling `close()` more than once is a no-op.
    pub fn close(&self, py: Python) -> PyResult<()> {
        let closed_client = self
            .client
            .lock()
            .map_err(|e| map_anyhow_error(anyhow!("Failed to acquire client lock: {}", e)))?
            .take();
        if closed_client.is_none() {
            return Ok(());
        }
        drop(closed_client);
        py.detach(|| self.settle());
        Ok(())
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
        params: Option<IndexMapSSR>,
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
        let client = self.reqwest_client()?;
        let _in_flight = self.track_in_flight();
        let method = Method::from_bytes(method.as_bytes())
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let is_post_put_patch = matches!(method, Method::POST | Method::PUT | Method::PATCH);
        let params = params.or_else(|| self.params.clone());
        let data_value: Option<Value> = data
            .map(depythonize)
            .transpose()
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let json_value: Option<Value> = json
            .map(depythonize)
            .transpose()
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let auth = auth.or(self.auth.clone());
        let auth_bearer = auth_bearer.or(self.auth_bearer.clone());
        let timeout: Option<f64> = timeout.or(self.timeout);

        let future = async move {
            // Create request builder
            let mut request_builder = client.request(method, url);

            // Params
            if let Some(params) = params {
                request_builder = request_builder.query(&params);
            }

            // Headers from client
            let client_headers = self
                .headers
                .lock()
                .map_err(|e| anyhow!("Failed to acquire headers lock: {}", e))?
                .clone();
            request_builder = request_builder.headers(client_headers.clone());

            // Headers
            let mut combined_headers = client_headers;
            if let Some(ref headers) = headers {
                let header_map = headers.to_headermap();
                for (key, value) in header_map.iter() {
                    combined_headers.insert(key.clone(), value.clone());
                }
                request_builder = request_builder.headers(headers.to_headermap());
            }

            // Cookies
            if let Some(cookies) = cookies {
                request_builder = request_builder.header(
                    COOKIE,
                    HeaderValue::from_str(&cookies.to_string()).map_err(anyhow::Error::new)?,
                );
            }

            // Only if method POST || PUT || PATCH
            if is_post_put_patch {
                // Content
                if let Some(content) = content {
                    request_builder = request_builder.body(content);
                }
                // Data
                if let Some(form_data) = data_value {
                    request_builder = request_builder.form(&form_data);
                }
                // Json - always serialize as JSON regardless of Accept header
                if let Some(json_data) = json_value {
                    request_builder = request_builder.json(&json_data);
                }
                // Files
                if let Some(files) = files {
                    let mut form = multipart::Form::new();
                    for (file_name, file_path) in files {
                        let file = File::open(file_path).await.map_err(anyhow::Error::new)?;
                        let stream = FramedRead::new(file, BytesCodec::new());
                        let file_body = Body::wrap_stream(stream);
                        let part = multipart::Part::stream(file_body).file_name(file_name.clone());
                        form = form.part(file_name, part);
                    }
                    request_builder = request_builder.multipart(form);
                }
            }

            // Auth
            if let Some((username, password)) = auth {
                request_builder = request_builder.basic_auth(username, password);
            } else if let Some(token) = auth_bearer {
                request_builder = request_builder.bearer_auth(token);
            }

            // Timeout
            if let Some(seconds) = timeout {
                request_builder = request_builder.timeout(Duration::from_secs_f64(seconds));
            }

            // Send the request and await the response
            let resp = request_builder.send().await.map_err(anyhow::Error::new)?;

            // Response items
            let cookies: IndexMapSSR = resp
                .cookies()
                .map(|cookie| (cookie.name().to_string(), cookie.value().to_string()))
                .collect();
            let headers: IndexMapSSR = resp.headers().to_indexmap();
            let status_code = resp.status().as_u16();
            let url = resp.url().to_string();
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
            // The future owns our clone of the reqwest client, which kept the
            // pool alive for the duration of the request; `block_on` drops it.
            let result = RUNTIME.block_on(future);
            // If `close()` ran in the meantime, that drop is what actually tore
            // the pool down, so settle its connections now rather than leaving
            // them until the runtime is next driven. (Streaming responses release
            // their connection on the next runtime drive after being read/closed.)
            if self.is_closed_unchecked() {
                self.settle();
            }
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
        params: Option<IndexMapSSR>,
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
        let client = self.reqwest_client()?;
        let _in_flight = self.track_in_flight();
        let method = Method::from_bytes(method.as_bytes())
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let is_post_put_patch = matches!(method, Method::POST | Method::PUT | Method::PATCH);
        let params = params.or_else(|| self.params.clone());
        let data_value: Option<Value> = data
            .map(depythonize)
            .transpose()
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let json_value: Option<Value> = json
            .map(depythonize)
            .transpose()
            .map_err(|e| map_anyhow_error(anyhow::Error::new(e)))?;
        let auth = auth.or(self.auth.clone());
        let auth_bearer = auth_bearer.or(self.auth_bearer.clone());
        let timeout: Option<f64> = timeout.or(self.timeout);

        let future = async {
            // Create request builder
            let mut request_builder = client.request(method, url);

            // Params
            if let Some(params) = params {
                request_builder = request_builder.query(&params);
            }

            // Headers from client
            let client_headers = self
                .headers
                .lock()
                .map_err(|e| anyhow!("Failed to acquire headers lock: {}", e))?
                .clone();
            request_builder = request_builder.headers(client_headers.clone());

            // Headers
            let mut combined_headers = client_headers;
            if let Some(ref headers) = headers {
                let header_map = headers.to_headermap();
                for (key, value) in header_map.iter() {
                    combined_headers.insert(key.clone(), value.clone());
                }
                request_builder = request_builder.headers(headers.to_headermap());
            }

            // Cookies
            if let Some(cookies) = cookies {
                request_builder = request_builder.header(
                    COOKIE,
                    HeaderValue::from_str(&cookies.to_string()).map_err(anyhow::Error::new)?,
                );
            }

            // Only if method POST || PUT || PATCH
            if is_post_put_patch {
                // Content
                if let Some(content) = content {
                    request_builder = request_builder.body(content);
                }
                // Data
                if let Some(form_data) = data_value {
                    request_builder = request_builder.form(&form_data);
                }
                // Json - always serialize as JSON regardless of Accept header
                if let Some(json_data) = json_value {
                    request_builder = request_builder.json(&json_data);
                }
                // Files
                if let Some(files) = files {
                    let mut form = multipart::Form::new();
                    for (file_name, file_path) in files {
                        let file = File::open(file_path).await.map_err(anyhow::Error::new)?;
                        let stream = FramedRead::new(file, BytesCodec::new());
                        let file_body = Body::wrap_stream(stream);
                        let part = multipart::Part::stream(file_body).file_name(file_name.clone());
                        form = form.part(file_name, part);
                    }
                    request_builder = request_builder.multipart(form);
                }
            }

            // Auth
            if let Some((username, password)) = auth {
                request_builder = request_builder.basic_auth(username, password);
            } else if let Some(token) = auth_bearer {
                request_builder = request_builder.bearer_auth(token);
            }

            // Timeout
            if let Some(seconds) = timeout {
                request_builder = request_builder.timeout(Duration::from_secs_f64(seconds));
            }

            // Send the request and await the response (but don't read body)
            let resp = request_builder.send().await.map_err(anyhow::Error::new)?;

            // Response items (extract before we move resp)
            let cookies: IndexMapSSR = resp
                .cookies()
                .map(|cookie| (cookie.name().to_string(), cookie.value().to_string()))
                .collect();
            let headers: IndexMapSSR = resp.headers().to_indexmap();
            let status_code = resp.status().as_u16();
            let url = resp.url().to_string();

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

        Ok(StreamingResponse::new(
            f_resp,
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

    // Register all exception types
    exceptions::register_exceptions(m)?;

    Ok(())
}
