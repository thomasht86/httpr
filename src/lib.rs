use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyDict;

use pyo3_asyncio::tokio as pyo3_tokio;
use reqwest::blocking::ClientBuilder as BlockingClientBuilder;
use reqwest::redirect::Policy as RedirectPolicy;
use reqwest::{Client as AsyncReqwestClient, ClientBuilder as AsyncClientBuilder};

use std::collections::HashMap;
use std::time::Duration;
use std::sync::{Arc, Mutex};

#[derive(Debug, Clone)]
struct ResponseMetadata {
    status_code: u16,
    headers: HashMap<String, String>,
}

/// A synchronous HTTP client.
#[pyclass]
#[derive(Debug)]
struct Client {
    base_url: Option<String>,
    timeout: f64,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
    inner: reqwest::blocking::Client,
    cookies: Mutex<reqwest::cookie::CookieStore>,
    last_response: Mutex<Option<ResponseMetadata>>,
}

#[pymethods]
impl Client {
    /// Create a new synchronous HTTP client.
    ///
    /// :param base_url: Optional base URL to prepend to relative paths.
    /// :param timeout: Timeout in seconds (float).
    /// :param follow_redirects: Whether to automatically follow 3xx redirects.
    /// :param default_headers: A dict of default headers.
    #[new]
    #[pyo3(signature = (
        base_url=None,
        timeout=10.0,
        follow_redirects=true,
        default_headers=None
    ))]
    fn new(
        base_url: Option<String>,
        timeout: f64,
        follow_redirects: bool,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        // Build the reqwest blocking client
        let mut builder = BlockingClientBuilder::new();

        // Timeout
        if timeout < 0.0 {
            return Err(PyValueError::new_err("timeout must be non-negative"));
        }
        builder = builder.timeout(Duration::from_secs_f64(timeout));

        // Redirects
        if !follow_redirects {
            builder = builder.redirect(RedirectPolicy::none());
        }

        // Default headers
        let mut headers_map = reqwest::header::HeaderMap::new();
        let mut header_store = HashMap::new();

        if let Some(py_dict) = default_headers {
            for (k, v) in py_dict {
                let key_str = k
                    .extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers keys must be strings"))?;
                let val_str = v
                    .extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers values must be strings"))?;

                let header_name = reqwest::header::HeaderName::from_bytes(key_str.as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = reqwest::header::HeaderValue::from_str(&val_str)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;

                headers_map.insert(header_name, header_value);
                header_store.insert(key_str, val_str);
            }
        }

        builder = builder.default_headers(headers_map);

        let final_client = builder
            .build()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to build client: {}", e)))?;

        Ok(Self {
            base_url,
            timeout,
            follow_redirects,
            default_headers: header_store,
            inner: final_client,
        })
    }

    /// Perform a GET request. Returns the response text as a string.
    ///
    /// :param url: Target URL (absolute or relative).
    /// :return: Response body text.
    #[pyo3(signature = (url))]
    fn get(&self, url: &str) -> PyResult<String> {
        // Construct final URL (handle base_url if present)
        let final_url = if is_absolute_url(url) {
            url.to_string()
        } else if let Some(base) = &self.base_url {
            if base.ends_with('/') {
                format!("{}{}", base, url)
            } else {
                format!("{}/{}", base, url)
            }
        } else {
            url.to_string()
        };

        // Send
        let resp = self
            .inner
            .get(&final_url)
            .send()
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

        let text = resp.text().map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
        Ok(text)
    }

    // ========== Python property getters so tests can verify config ==========

    #[getter]
    fn base_url(&self) -> Option<String> {
        self.base_url.clone()
    }

    #[getter]
    fn timeout(&self) -> f64 {
        self.timeout
    }

    #[getter]
    fn follow_redirects(&self) -> bool {
        self.follow_redirects
    }

    #[getter]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        for (k, v) in &self.default_headers {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

/// An asynchronous HTTP client.
#[pyclass]
#[derive(Clone, Debug)]
struct AsyncClient {
    base_url: Option<String>,
    timeout: f64,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
    inner: AsyncReqwestClient,
    cookies: reqwest::cookie::CookieStore,
    last_response: Arc<tokio::sync::Mutex<Option<ResponseMetadata>>>,
}

#[pymethods]
impl AsyncClient {
    /// Create a new asynchronous HTTP client.
    ///
    /// :param base_url: Optional base URL.
    /// :param timeout: Timeout in seconds (float).
    /// :param follow_redirects: Bool controlling 3xx behavior.
    /// :param default_headers: Dict of default headers.
    #[new]
    #[pyo3(signature = (
        base_url=None,
        timeout=10.0,
        follow_redirects=true,
        default_headers=None
    ))]
    fn new(
        base_url: Option<String>,
        timeout: f64,
        follow_redirects: bool,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        // Build async client
        let mut builder = AsyncClientBuilder::new();

        // Timeout
        if timeout < 0.0 {
            return Err(PyValueError::new_err("timeout must be non-negative"));
        }
        builder = builder.timeout(Duration::from_secs_f64(timeout));

        // Redirects
        if !follow_redirects {
            builder = builder.redirect(RedirectPolicy::none());
        }

        // Default headers
        let mut headers_map = reqwest::header::HeaderMap::new();
        let mut header_store = HashMap::new();

        if let Some(py_dict) = default_headers {
            for (k, v) in py_dict {
                let key_str = k
                    .extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers keys must be strings"))?;
                let val_str = v
                    .extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers values must be strings"))?;

                let header_name = reqwest::header::HeaderName::from_bytes(key_str.as_bytes())
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                let header_value = reqwest::header::HeaderValue::from_str(&val_str)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                headers_map.insert(header_name, header_value);
                header_store.insert(key_str, val_str);
            }
        }

        builder = builder.default_headers(headers_map);

        let final_client = builder
            .build()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to build async client: {}", e)))?;

        Ok(Self {
            base_url,
            timeout,
            follow_redirects,
            default_headers: header_store,
            inner: final_client,
        })
    }

    /// Perform an async GET request. Returns a Python awaitable that yields a string body.
    ///
    /// :param url: Target URL.
    /// :return: str with the response body.
    #[pyo3(signature = (url))]
    fn get<'a>(&'a self, py: Python<'a>, url: &str) -> PyResult<&'a PyAny> {
        let final_url = if is_absolute_url(url) {
            url.to_string()
        } else if let Some(base) = &self.base_url {
            if base.ends_with('/') {
                format!("{}{}", base, url)
            } else {
                format!("{}/{}", base, url)
            }
        } else {
            url.to_string()
        };

        let client = self.inner.clone();
        pyo3_tokio::future_into_py(py, async move {
            let resp = client
                .get(&final_url)
                .send()
                .await
                .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;

            let text = resp
                .text()
                .await
                .map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
            Ok(text)
        })
    }

    // ========== Python property getters ==========

    #[getter]
    fn base_url(&self) -> Option<String> {
        self.base_url.clone()
    }

    #[getter]
    fn timeout(&self) -> f64 {
        self.timeout
    }

    #[getter]
    fn follow_redirects(&self) -> bool {
        self.follow_redirects
    }

    #[getter]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        for (k, v) in &self.default_headers {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

/// Very naive function checking if a URL is absolute.
fn is_absolute_url(url: &str) -> bool {
    url.starts_with("http://") || url.starts_with("https://")
}

/// Define the Python module
#[pymodule]
fn httpr(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_class::<AsyncClient>()?;
    Ok(())
}
