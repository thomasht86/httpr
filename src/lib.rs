//! httpr: A Python package exposing synchronous and asynchronous HTTP clients built on reqwest.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::Duration;

use pyo3::exceptions::{PyException, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyAnyMethods, PyDict, PyDictMethods};
use pyo3::{Bound, Py, PyAny, PyResult};
use serde_pyobject::from_pyobject;

use reqwest::blocking;
use reqwest::header::{HeaderMap, HeaderName, HeaderValue, SET_COOKIE};

// Add at module level
fn parse_set_cookie(cookie_str: &str) -> Option<(String, String)> {
    cookie_str.split_once('=')
        .map(|(k, v)| {
            let value = v.split(';').next().unwrap_or("").trim().to_string();
            (k.trim().to_string(), value)
        })
}

// --------- LastResponse ---------
#[pyclass]
#[derive(Clone)]
struct LastResponse {
    /// The HTTP status code.
    #[pyo3(get)]
    status_code: u16,
}

// --------- Synchronous HTTP Client ---------
#[pyclass(unsendable)]
struct Client {
    inner: blocking::Client,
    base_url: Option<String>,
    timeout: Option<Duration>,
    follow_redirects: bool,
    default_headers: HeaderMap,
    cookies: HashMap<String, String>,
    last_response: Option<Py<LastResponse>>,
}

#[pymethods]
impl Client {
    /// Create a new synchronous Client.
    #[new]
    #[pyo3(signature = (base_url=None, timeout=None, follow_redirects=None, default_headers=None))]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Self> {
        let timeout_duration = timeout.map(Duration::from_secs_f64);
        let follow = follow_redirects.unwrap_or(true);
        let mut builder = blocking::Client::builder().cookie_store(true);
        if let Some(t) = timeout_duration {
            builder = builder.timeout(t);
        }
        if !follow {
            builder = builder.redirect(reqwest::redirect::Policy::none());
        }
        let mut header_map = HeaderMap::new();
        if let Some(dict) = default_headers {
            for (k, v) in dict.iter() {
                let key: String = k.extract()?.to_lowercase();
                let value: String = v.extract()?;
                let header_name = HeaderName::from_bytes(key.trim().as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = HeaderValue::from_str(value.trim())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                header_map.insert(header_name, header_value);
            }
        }
        let client = builder.build().map_err(|e| PyException::new_err(e.to_string()))?;
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

    /// Getter for base_url.
    #[getter]
    fn base_url(&self) -> PyResult<Option<String>> {
        Ok(self.base_url.clone())
    }

    /// Getter for timeout in seconds.
    #[getter]
    fn timeout(&self) -> PyResult<Option<f64>> {
        Ok(self.timeout.map(|d| d.as_secs_f64()))
    }

    /// Getter for follow_redirects.
    #[getter]
    fn follow_redirects(&self) -> PyResult<bool> {
        Ok(self.follow_redirects)
    }

    /// Getter for default_headers.
    #[getter]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (key, value) in self.default_headers.iter() {
            let key_str = key.as_str().to_lowercase();
            let value_str = value.to_str().unwrap_or("");
            dict.set_item(key_str, value_str)?;
        }
        Ok(dict)
    }

    /// Perform a synchronous GET request.
    #[pyo3(signature = (url, params=None, headers=None))]
    fn get(
        &mut self,
        py: Python<'_>,
        url: String,
        params: Option<&Bound<'_, PyAny>>,
        headers: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<String> {
        let full_url = if let Some(base) = &self.base_url {
            if url.starts_with("http") {
                url
            } else {
                format!("{}{}", base, url)
            }
        } else {
            url
        };

        let mut req = self.inner.get(&full_url);
        if let Some(py_params) = params {
            let params_map: HashMap<String, String> = from_pyobject(py_params.clone())?;
            req = req.query(&params_map);
        }
        let mut header_map = self.default_headers.clone();
        if let Some(py_headers) = headers {
            let headers_map: HashMap<String, String> = from_pyobject(py_headers.clone())?;
            for (k, v) in headers_map {
                let header_name = HeaderName::from_bytes(k.as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = HeaderValue::from_str(&v)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                header_map.insert(header_name, header_value);
            }
        }
        req = req.headers(header_map);
        let resp = req.send().map_err(|e| PyException::new_err(e.to_string()))?;
        let status_code = resp.status().as_u16();
        self.last_response = Some(Py::new(py, LastResponse { status_code })?);
        if let Some(cookies) = resp.headers().get_all(SET_COOKIE) {
            for cookie in cookies.iter() {
                if let Ok(cookie_str) = cookie.to_str() {
                    if let Some((name, value)) = parse_set_cookie(cookie_str) {
                        self.cookies.insert(name, value);
                    }
                }
            }
        }
        let text = resp.text().map_err(|e| PyException::new_err(e.to_string()))?;
        Ok(text)
    }

    /// Perform a synchronous POST request.
    #[pyo3(signature = (url, data=None, json=None, headers=None))]
    fn post(
        &mut self,
        py: Python<'_>,
        url: String,
        data: Option<&Bound<'_, PyAny>>,
        json: Option<&Bound<'_, PyAny>>,
        headers: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<String> {
        let full_url = if let Some(base) = &self.base_url {
            if url.starts_with("http") {
                url
            } else {
                format!("{}{}", base, url)
            }
        } else {
            url
        };

        let mut req = self.inner.post(&full_url);
        let mut header_map = self.default_headers.clone();
        if let Some(py_headers) = headers {
            let headers_map: HashMap<String, String> = from_pyobject(py_headers.clone())?;
            for (k, v) in headers_map {
                let header_name = HeaderName::from_bytes(k.as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = HeaderValue::from_str(&v)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                header_map.insert(header_name, header_value);
            }
        }
        req = req.headers(header_map);
        if let Some(py_json) = json {
            let json_value: serde_json::Value = from_pyobject(py_json.clone())?;
            req = req.json(&json_value);
        } else if let Some(py_data) = data {
            let form_data: HashMap<String, String> = from_pyobject(py_data.clone())?;
            req = req.form(&form_data);
        }
        let resp = req.send().map_err(|e| PyException::new_err(e.to_string()))?;
        let status_code = resp.status().as_u16();
        self.last_response = Some(Py::new(py, LastResponse { status_code })?);
        if let Some(set_cookie) = resp.headers().get(SET_COOKIE) {
            if let Ok(cookie_str) = set_cookie.to_str() {
                if let Some((name, value)) = parse_set_cookie(cookie_str) {
                    self.cookies.insert(name, value);
                }
            }
        }
        let text = resp.text().map_err(|e| PyException::new_err(e.to_string()))?;
        Ok(text)
    }

    /// Return stored cookies as a Python dictionary.
    #[getter]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (k, v) in &self.cookies {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }

    /// Getter for the last response (exposed as `_last_response`).
    #[getter("_last_response")]
    fn last_response_py<'py>(&self, py: Python<'py>) -> PyResult<Option<Py<LastResponse>>> {
        Ok(self.last_response.as_ref().map(|p| p.clone_ref(py)))
    }
}

// ...existing code...

#[pyclass]
#[derive(Clone)]
struct AsyncClient {
    inner: reqwest::Client,
    base_url: Option<String>,
    timeout: Option<Duration>,
    follow_redirects: bool,
    default_headers: HeaderMap,
    cookies: Arc<Mutex<HashMap<String, String>>>,
    last_response: Arc<Mutex<Option<Py<LastResponse>>>>,
}

#[pymethods]
impl AsyncClient {
    /// Create a new asynchronous Client.
    #[new]
    #[pyo3(signature = (base_url=None, timeout=None, follow_redirects=None, default_headers=None))]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<&Bound<PyDict>>,
    ) -> PyResult<Self> {
        let timeout_duration = timeout.map(Duration::from_secs_f64);
        let follow = follow_redirects.unwrap_or(true);
        let mut builder = reqwest::Client::builder();
        if let Some(t) = timeout_duration {
            builder = builder.timeout(t);
        }
        if !follow {
            builder = builder.redirect(reqwest::redirect::Policy::none());
        }
        let mut header_map = HeaderMap::new();
        if let Some(dict) = default_headers {
            for (k, v) in dict.iter() {
                let key: String = k.extract()?;
                let value: String = v.extract()?;
                let header_name = HeaderName::from_bytes(key.trim().as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = HeaderValue::from_str(value.trim())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                header_map.insert(header_name, header_value);
            }
        }
        let client =
            builder.build().map_err(|e| PyException::new_err(e.to_string()))?;
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

    /// Getter for base_url.
    #[getter]
    fn base_url(&self) -> PyResult<Option<String>> {
        Ok(self.base_url.clone())
    }

    /// Getter for timeout in seconds.
    #[getter]
    fn timeout(&self) -> PyResult<Option<f64>> {
        Ok(self.timeout.map(|d| d.as_secs_f64()))
    }

    /// Getter for follow_redirects.
    #[getter]
    fn follow_redirects(&self) -> PyResult<bool> {
        Ok(self.follow_redirects)
    }

    /// Getter for default headers.
    #[getter]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        for (key, value) in self.default_headers.iter() {
            let key_str = key.as_str();
            let value_str = value.to_str().unwrap_or("");
            dict.set_item(key_str, value_str)?;
        }
        Ok(dict)
    }

    /// Perform an asynchronous GET request.
    #[pyo3(name = "get", signature = (url, params=None, headers=None))]
    fn get<'py>(
        &self,
        py: Python<'py>,
        url: String,
        params: Option<&Bound<PyAny>>,
        headers: Option<&Bound<PyAny>>,
    ) -> PyResult<Bound<'py, PyAny>> {
        let params_map = match params {
            Some(p) => Some(from_pyobject::<HashMap<String, String>, PyAny>(p.clone())?),
            None => None,
        };
        let headers_map = match headers {
            Some(h) => Some(from_pyobject::<HashMap<String, String>, PyAny>(h.clone())?),
            None => None,
        };
        let client = self.clone();
        let url = url.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            let full_url = if let Some(base) = &client.base_url {
                if url.starts_with("http") {
                    url.clone()
                } else {
                    format!("{}{}", base, url)
                }
            } else {
                url.clone()
            };

            let mut req = client.inner.get(&full_url);
            if let Some(params_map) = params_map {
                req = req.query(&params_map);
            }
            let mut header_map = client.default_headers.clone();
            if let Some(headers_map) = headers_map {
                for (k, v) in headers_map {
                    let header_name = HeaderName::from_bytes(k.as_bytes())
                        .map_err(|e| PyValueError::new_err(e.to_string()))?;
                    let header_value = HeaderValue::from_str(&v)
                        .map_err(|e| PyValueError::new_err(e.to_string()))?;
                    header_map.insert(header_name, header_value);
                }
            }
            req = req.headers(header_map);
            let resp = req.send()
                .await
                .map_err(|e| PyException::new_err(e.to_string()))?;
            let status_code = resp.status().as_u16();

            {
                Python::with_gil(|py| {
                    let lr = Py::new(py, LastResponse { status_code })?;
                    let mut last_response_lock = client.last_response.lock().unwrap();
                    *last_response_lock = Some(lr);
                    Ok::<_, PyErr>(())
                })?;
            }

            if let Some(cookies) = resp.headers().get_all(SET_COOKIE) {
                for cookie in cookies.iter() {
                    if let Ok(cookie_str) = cookie.to_str() {
                        if let Some((name, value)) = parse_set_cookie(cookie_str) {
                            let mut cookies_lock = client.cookies.lock().unwrap();
                            cookies_lock.insert(name, value);
                        }
                    }
                }
            }

            let text = resp.text()
                .await
                .map_err(|e| PyException::new_err(e.to_string()))?;
            Ok(text)
        })
    }

    /// Perform an asynchronous POST request.
    #[pyo3(name = "post", signature = (url, data=None, json=None, headers=None))]
    fn post<'py>(
        &self,
        py: Python<'py>,
        url: String,
        data: Option<&Bound<PyAny>>,
        json: Option<&Bound<PyAny>>,
        headers: Option<&Bound<PyAny>>,
    ) -> PyResult<Bound<'py, PyAny>> {
        // Convert Python objects into pure Rust types before entering the async block.
        let headers_converted: Option<HashMap<String, String>> = if let Some(py_headers) = headers {
            Some(Python::with_gil(|_py| from_pyobject(py_headers.clone()))
                .map_err(|e| PyException::new_err(e.to_string()))?)
        } else {
            None
        };
        let json_converted: Option<serde_json::Value> = if let Some(py_json) = json {
            Some(Python::with_gil(|_py| from_pyobject(py_json.clone()))?)
        } else {
            None
        };
        let data_converted: Option<HashMap<String, String>> = if let Some(py_data) = data {
            Some(Python::with_gil(|_py| from_pyobject(py_data.clone()))?)
        } else {
            None
        };

        pyo3_async_runtimes::tokio::future_into_py(py, {
            let client = self.clone();
            // Only Send types are captured here.
            async move {
                let full_url = if let Some(base) = &client.base_url {
                    if url.starts_with("http") {
                        url.clone()
                    } else {
                        format!("{}{}", base, url)
                    }
                } else {
                    url.clone()
                };

                let mut req = client.inner.post(&full_url);
                let mut header_map = client.default_headers.clone();
                if let Some(headers_map) = headers_converted {
                    for (k, v) in headers_map {
                        let header_name = HeaderName::from_bytes(k.as_bytes())
                            .map_err(|e| PyValueError::new_err(e.to_string()))?;
                        let header_value = HeaderValue::from_str(&v)
                            .map_err(|e| PyValueError::new_err(e.to_string()))?;
                        header_map.insert(header_name, header_value);
                    }
                }
                req = req.headers(header_map);
                if let Some(json_value) = json_converted {
                    req = req.json(&json_value);
                } else if let Some(form_data) = data_converted {
                    req = req.form(&form_data);
                }
                let resp = req.send()
                    .await
                    .map_err(|e| PyException::new_err(e.to_string()))?;
                let status_code = resp.status().as_u16();

                // Wrap GIL work inside spawn_blocking so that our async future remains Send.
                tokio::task::spawn_blocking({
                    let client = client.clone();
                    move || {
                        Python::with_gil(|py| {
                            let lr = Py::new(py, LastResponse { status_code })?;
                            let mut last_response_lock = client.last_response.lock().unwrap();
                            *last_response_lock = Some(lr);
                            Ok::<(), PyErr>(())
                        })
                    }
                })
                .await
                .map_err(|e| PyException::new_err(e.to_string()))??;

                if let Some(set_cookie) = resp.headers().get(SET_COOKIE) {
                    if let Ok(cookie_str) = set_cookie.to_str() {
                        if let Some((name, value)) = parse_set_cookie(cookie_str) {
                            let mut cookies_lock = client.cookies.lock().unwrap();
                            cookies_lock.insert(name, value);
                        }
                    }
                }

                let text = resp.text()
                    .await
                    .map_err(|e| PyException::new_err(e.to_string()))?;
                Ok(text)
            }
        })
    }

    /// Return stored cookies as a Python dictionary.
    #[getter]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        let dict = PyDict::new(py);
        let cookies_lock = self.cookies.lock().unwrap();
        for (k, v) in cookies_lock.iter() {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }

    /// Getter for the last response (exposed as "_last_response").
    #[getter("_last_response")]
    fn last_response_py<'py>(&self, py: Python<'py>) -> PyResult<Option<Py<LastResponse>>> {
        let last_response_lock = self.last_response.lock().unwrap();
        if let Some(ref lr) = *last_response_lock {
            Ok(Some(lr.clone_ref(py)))
        } else {
            Ok(None)
        }
    }
}

// ...existing code...

#[pymodule]
fn httpr(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_class::<AsyncClient>()?;
    Ok(())
}
