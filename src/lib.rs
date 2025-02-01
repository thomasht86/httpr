//! httpr: A Python package exposing synchronous and asynchronous HTTP clients built on reqwest.
//!
//! The synchronous client uses reqwest’s blocking API (and is marked unsendable), while the asynchronous
//! client uses reqwest’s async API together with pyo3-asyncio. Both support custom configuration,
//! GET/POST requests, cookie handling, and tracking of the last response’s status code.
//!
//! Make sure your Cargo.toml includes the features shown in the example above.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::Duration;

use pyo3::exceptions::{PyException, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use reqwest::header::{HeaderMap, HeaderName, HeaderValue, SET_COOKIE};

// Import pyo3_serde for converting Python objects to/from serde types.

#[derive(Clone)]
#[pyclass]
struct LastResponse {
    /// The HTTP status code.
    #[pyo3(get)]
    status_code: u16,
}

/// ---------------------------
/// Synchronous HTTP Client
/// ---------------------------

/// A synchronous HTTP client that wraps reqwest’s blocking API.
///
/// Note: Because reqwest’s blocking client is not Send, we mark this pyclass as unsendable.
#[pyclass(unsendable)]
struct Client {
    /// The underlying reqwest blocking client.
    inner: reqwest::blocking::Client,
    /// Optional base URL to prefix requests.
    base_url: Option<String>,
    /// Timeout for requests.
    timeout: Option<Duration>,
    /// Whether to follow redirects.
    follow_redirects: bool,
    /// Default headers.
    default_headers: HeaderMap,
    /// Stored cookies.
    cookies: HashMap<String, String>,
    /// The last response’s status code.
    last_response: Option<LastResponse>,
}

#[pymethods]
impl Client {
    /// Create a new synchronous Client.
    ///
    /// Parameters:
    ///     base_url (str, optional): Base URL to prefix all requests.
    ///     timeout (float, optional): Timeout in seconds.
    ///     follow_redirects (bool, optional): Whether to follow redirects (default: True).
    ///     default_headers (dict, optional): Headers to include on every request.
    #[new]
    #[pyo3(text_signature = "($self, base_url=None, timeout=None, follow_redirects=None, default_headers=None)")]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        let timeout_duration = timeout.map(Duration::from_secs_f64);
        let follow = follow_redirects.unwrap_or(true);

        // The cookie_store(true) method requires the "cookies" feature in reqwest.
        let mut builder = reqwest::blocking::Client::builder().cookie_store(true);
        if let Some(t) = timeout_duration {
            builder = builder.timeout(t);
        }
        if !follow {
            builder = builder.redirect(reqwest::redirect::Policy::none());
        }

        // Build default headers from the provided Python dict.
        let mut header_map = HeaderMap::new();
        if let Some(dict) = default_headers {
            for (key, value) in dict.iter() {
                let key_str = key
                    .extract::<String>()
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let value_str = value
                    .extract::<String>()
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_name = HeaderName::from_bytes(key_str.as_bytes()).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header name '{}': {}", key_str, e))
                })?;
                let header_value = HeaderValue::from_str(&value_str).map_err(|e| {
                    PyValueError::new_err(format!(
                        "Invalid header value for '{}': {}",
                        key_str, e
                    ))
                })?;
                header_map.insert(header_name, header_value);
            }
        }

        let client = builder
            .build()
            .map_err(|e| PyException::new_err(format!("Failed to build client: {}", e)))?;

        Ok(Client {
            inner: client,
            base_url,
            timeout: timeout_duration,
            follow_redirects: follow,
            default_headers: header_map,
            cookies: HashMap::new(),
            last_response: None,
        })
    }

    /// Perform a synchronous GET request.
    ///
    /// Parameters:
    ///     url (str): The request URL (absolute or relative).
    ///     params (dict, optional): Query parameters.
    ///     headers (dict, optional): Additional headers.
    ///
    /// Returns:
    ///     str: The response text.
    #[pyo3(text_signature = "($self, url, params=None, headers=None)")]
    fn get(&mut self, url: String, params: Option<&PyAny>, headers: Option<&PyAny>) -> PyResult<String> {
        let full_url = if let Some(base) = &self.base_url {
            if url.starts_with("http") {
                url.clone()
            } else {
                format!("{}{}", base, url)
            }
        } else {
            url.clone()
        };

        let mut req = self.inner.get(&full_url);

        if let Some(py_params) = params {
            let params_map: HashMap<String, String> = py_params
                .extract()
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            req = req.query(&params_map);
        }

        let mut header_map = self.default_headers.clone();
        if let Some(py_headers) = headers {
            let headers_map: HashMap<String, String> = py_headers
                .extract()
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            for (k, v) in headers_map {
                let header_name = HeaderName::from_bytes(k.as_bytes()).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header name '{}': {}", k, e))
                })?;
                let header_value = HeaderValue::from_str(&v).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header value for '{}': {}", k, e))
                })?;
                header_map.insert(header_name, header_value);
            }
        }
        req = req.headers(header_map);

        let resp = req
            .send()
            .map_err(|e| PyException::new_err(format!("Request error: {}", e)))?;

        self.last_response = Some(LastResponse {
            status_code: resp.status().as_u16(),
        });

        for cookie in resp.headers().get_all(SET_COOKIE).iter() {
            if let Ok(cookie_str) = cookie.to_str() {
                if let Some((name, value)) = parse_set_cookie(cookie_str) {
                    self.cookies.insert(name, value);
                }
            }
        }

        resp.text()
            .map_err(|e| PyException::new_err(format!("Error reading response: {}", e)))
    }

    /// Perform a synchronous POST request.
    ///
    /// Parameters:
    ///     url (str): The request URL.
    ///     data (dict, optional): Form data.
    ///     json (dict, optional): JSON data.
    ///     headers (dict, optional): Additional headers.
    ///
    /// Returns:
    ///     str: The response text.
    #[pyo3(text_signature = "($self, url, data=None, json=None, headers=None)")]
    fn post(&mut self, url: String, data: Option<&PyAny>, json: Option<&PyAny>, headers: Option<&PyAny>) -> PyResult<String> {
        let full_url = if let Some(base) = &self.base_url {
            if url.starts_with("http") {
                url.clone()
            } else {
                format!("{}{}", base, url)
            }
        } else {
            url.clone()
        };

        let mut req = self.inner.post(&full_url);

        let mut header_map = self.default_headers.clone();
        if let Some(py_headers) = headers {
            let headers_map: HashMap<String, String> = py_headers
                .extract()
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            for (k, v) in headers_map {
                let header_name = HeaderName::from_bytes(k.as_bytes()).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header name '{}': {}", k, e))
                })?;
                let header_value = HeaderValue::from_str(&v).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header value for '{}': {}", k, e))
                })?;
                header_map.insert(header_name, header_value);
            }
        }
        req = req.headers(header_map);

        // If JSON is provided, use it; otherwise, if form data is provided, use that.
        if let Some(py_json) = json {
            let json_value: serde_json::Value = pyo3_serde::from_pyany(py_json)
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            req = req.json(&json_value);
        } else if let Some(py_data) = data {
            let form_map: HashMap<String, String> = py_data
                .extract()
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            req = req.form(&form_map);
        }

        let resp = req
            .send()
            .map_err(|e| PyException::new_err(format!("Request error: {}", e)))?;

        self.last_response = Some(LastResponse {
            status_code: resp.status().as_u16(),
        });

        for cookie in resp.headers().get_all(SET_COOKIE).iter() {
            if let Ok(cookie_str) = cookie.to_str() {
                if let Some((name, value)) = parse_set_cookie(cookie_str) {
                    self.cookies.insert(name, value);
                }
            }
        }

        resp.text()
            .map_err(|e| PyException::new_err(format!("Error reading response: {}", e)))
    }

    /// Return stored cookies as a Python dictionary.
    #[getter]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<PyObject> {
        let dict = PyDict::new(py);
        for (k, v) in &self.cookies {
            dict.set_item(k, v)?;
        }
        Ok(dict.to_object(py))
    }

    /// Getter for the last response (exposed as `_last_response`).
    #[getter("_last_response")]
    fn last_response_py(&self) -> PyResult<Option<LastResponse>> {
        Ok(self.last_response.clone())
    }
}

/// ---------------------------
/// Asynchronous HTTP Client
/// ---------------------------

/// An asynchronous HTTP client using reqwest’s async API and pyo3-asyncio.
/// Mutable state is stored in Arcs/Mutexes so that async closures can own clones.
#[pyclass]
#[derive(Clone)]
struct AsyncClient {
    inner: reqwest::Client,
    base_url: Option<String>,
    timeout: Option<Duration>,
    follow_redirects: bool,
    default_headers: HeaderMap,
    cookies: Arc<Mutex<HashMap<String, String>>>,
    last_response: Arc<Mutex<Option<LastResponse>>>,
}

#[pymethods]
impl AsyncClient {
    /// Create a new AsyncClient.
    ///
    /// Parameters are the same as for the synchronous Client.
    #[new]
    #[pyo3(text_signature = "($self, base_url=None, timeout=None, follow_redirects=None, default_headers=None)")]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        let timeout_duration = timeout.map(Duration::from_secs_f64);
        let follow = follow_redirects.unwrap_or(true);

        let mut builder = reqwest::Client::builder().cookie_store(true);
        if let Some(t) = timeout_duration {
            builder = builder.timeout(t);
        }
        if !follow {
            builder = builder.redirect(reqwest::redirect::Policy::none());
        }

        let mut header_map = HeaderMap::new();
        if let Some(dict) = default_headers {
            for (key, value) in dict.iter() {
                let key_str = key
                    .extract::<String>()
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let value_str = value
                    .extract::<String>()
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_name = HeaderName::from_bytes(key_str.as_bytes()).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header name '{}': {}", key_str, e))
                })?;
                let header_value = HeaderValue::from_str(&value_str).map_err(|e| {
                    PyValueError::new_err(format!("Invalid header value for '{}': {}", key_str, e))
                })?;
                header_map.insert(header_name, header_value);
            }
        }
        let client = builder
            .build()
            .map_err(|e| PyException::new_err(format!("Failed to build client: {}", e)))?;

        Ok(AsyncClient {
            inner: client,
            base_url,
            timeout: timeout_duration,
            follow_redirects: follow,
            default_headers: header_map,
            cookies: Arc::new(Mutex::new(HashMap::new())),
            last_response: Arc::new(Mutex::new(None)),
        })
    }

    /// Asynchronous GET request.
    ///
    /// Parameters:
    ///     url (str): The request URL.
    ///     params (dict, optional): Query parameters.
    ///     headers (dict, optional): Additional headers.
    ///
    /// Returns an awaitable resolving to the response text.
    #[pyo3(text_signature = "($self, url, params=None, headers=None)")]
    fn get<'p>(
        &self,
        py: Python<'p>,
        url: String,
        params: Option<&PyAny>,
        headers: Option<&PyAny>,
    ) -> PyResult<&'p PyAny> {
        let this = self.clone();
        let params_map = if let Some(p) = params {
            Some(p.extract::<HashMap<String, String>>()
                .map_err(|e| PyValueError::new_err(e.to_string()))?)
        } else {
            None
        };
        let headers_map_opt = if let Some(h) = headers {
            Some(h.extract::<HashMap<String, String>>()
                .map_err(|e| PyValueError::new_err(e.to_string()))?)
        } else {
            None
        };

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let full_url = if let Some(base) = &this.base_url {
                if url.starts_with("http") {
                    url.clone()
                } else {
                    format!("{}{}", base, url)
                }
            } else {
                url.clone()
            };

            let mut req = this.inner.get(&full_url);
            if let Some(params_map) = params_map {
                req = req.query(&params_map);
            }

            let header_map = if let Some(headers_map) = headers_map_opt {
                let mut hm = this.default_headers.clone();
                for (k, v) in headers_map {
                    let header_name = HeaderName::from_bytes(k.as_bytes()).map_err(|e| {
                        PyValueError::new_err(format!("Invalid header name '{}': {}", k, e))
                    })?;
                    let header_value = HeaderValue::from_str(&v).map_err(|e| {
                        PyValueError::new_err(format!("Invalid header value for '{}': {}", k, e))
                    })?;
                    hm.insert(header_name, header_value);
                }
                hm
            } else {
                this.default_headers.clone()
            };
            req = req.headers(header_map);

            let resp = req.send().await.map_err(|e| {
                PyException::new_err(format!("Request error: {}", e))
            })?;

            {
                let mut lr = this.last_response.lock().unwrap();
                *lr = Some(LastResponse { status_code: resp.status().as_u16() });
            }

            let headers_received = resp.headers().clone();
            let text = resp.text().await.map_err(|e| {
                PyException::new_err(format!("Error reading response: {}", e))
            })?;

            {
                let mut cookies = this.cookies.lock().unwrap();
                for cookie in headers_received.get_all(SET_COOKIE).iter() {
                    if let Ok(cookie_str) = cookie.to_str() {
                        if let Some((name, value)) = parse_set_cookie(cookie_str) {
                            cookies.insert(name, value);
                        }
                    }
                }
            }
            Ok(text)
        })
    }

    /// Asynchronous POST request.
    ///
    /// Parameters:
    ///     url (str): The request URL.
    ///     data (dict, optional): Form data.
    ///     json (dict, optional): JSON data.
    ///     headers (dict, optional): Additional headers.
    ///
    /// Returns an awaitable resolving to the response text.
    #[pyo3(text_signature = "($self, url, data=None, json=None, headers=None)")]
    fn post<'p>(
        &self,
        py: Python<'p>,
        url: String,
        data: Option<&PyAny>,
        json: Option<&PyAny>,
        headers: Option<&PyAny>,
    ) -> PyResult<&'p PyAny> {
        let this = self.clone();
        let headers_map_opt = if let Some(h) = headers {
            Some(h.extract::<HashMap<String, String>>()
                .map_err(|e| PyValueError::new_err(e.to_string()))?)
        } else {
            None
        };
        let data_map_opt = if let Some(d) = data {
            Some(d.extract::<HashMap<String, String>>()
                .map_err(|e| PyValueError::new_err(e.to_string()))?)
        } else {
            None
        };
        let json_value_opt = if let Some(j) = json {
            Some(pyo3_serde::from_pyany(j)
                .map_err(|e| PyValueError::new_err(e.to_string()))?)
        } else {
            None
        };

        pyo3_asyncio::tokio::future_into_py(py, async move {
            let full_url = if let Some(base) = &this.base_url {
                if url.starts_with("http") {
                    url.clone()
                } else {
                    format!("{}{}", base, url)
                }
            } else {
                url.clone()
            };

            let mut req = this.inner.post(&full_url);

            let header_map = if let Some(headers_map) = headers_map_opt {
                let mut hm = this.default_headers.clone();
                for (k, v) in headers_map {
                    let header_name = HeaderName::from_bytes(k.as_bytes()).map_err(|e| {
                        PyValueError::new_err(format!("Invalid header name '{}': {}", k, e))
                    })?;
                    let header_value = HeaderValue::from_str(&v).map_err(|e| {
                        PyValueError::new_err(format!("Invalid header value for '{}': {}", k, e))
                    })?;
                    hm.insert(header_name, header_value);
                }
                hm
            } else {
                this.default_headers.clone()
            };
            req = req.headers(header_map);

            if let Some(json_value) = json_value_opt {
                req = req.json(&json_value);
            } else if let Some(data_map) = data_map_opt {
                req = req.form(&data_map);
            }

            let resp = req.send().await.map_err(|e| {
                PyException::new_err(format!("Request error: {}", e))
            })?;

            {
                let mut lr = this.last_response.lock().unwrap();
                *lr = Some(LastResponse { status_code: resp.status().as_u16() });
            }

            let headers_received = resp.headers().clone();
            let text = resp.text().await.map_err(|e| {
                PyException::new_err(format!("Error reading response: {}", e))
            })?;

            {
                let mut cookies = this.cookies.lock().unwrap();
                for cookie in headers_received.get_all(SET_COOKIE).iter() {
                    if let Ok(cookie_str) = cookie.to_str() {
                        if let Some((name, value)) = parse_set_cookie(cookie_str) {
                            cookies.insert(name, value);
                        }
                    }
                }
            }
            Ok(text)
        })
    }

    /// Return stored cookies as a Python dictionary.
    #[getter]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<PyObject> {
        let dict = PyDict::new(py);
        let cookies = self.cookies.lock().unwrap();
        for (k, v) in cookies.iter() {
            dict.set_item(k, v)?;
        }
        Ok(dict.to_object(py))
    }

    /// Getter for the last response (exposed as `_last_response`).
    #[getter("_last_response")]
    fn last_response_py(&self) -> PyResult<Option<LastResponse>> {
        let lr = self.last_response.lock().unwrap();
        Ok(lr.clone())
    }
}

/// ---------------------------
/// Helper Function
/// ---------------------------

/// A simple parser for a Set-Cookie header.
/// It splits on ';' and then on '=' to extract the cookie name and value.
/// (A production-quality parser would be more robust.)
fn parse_set_cookie(cookie: &str) -> Option<(String, String)> {
    let parts: Vec<&str> = cookie.split(';').collect();
    if parts.is_empty() {
        return None;
    }
    let kv: Vec<&str> = parts[0].splitn(2, '=').collect();
    if kv.len() != 2 {
        return None;
    }
    Some((kv[0].trim().to_string(), kv[1].trim().to_string()))
}

/// ---------------------------
/// Module Initialization
/// ---------------------------

#[pymodule]
fn httpr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_class::<AsyncClient>()?;
    m.add_class::<LastResponse>()?;
    Ok(())
}