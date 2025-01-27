#![allow(non_local_definitions)]

use std::collections::HashMap;
use std::time::{Duration, Instant};
use pyo3::prelude::*;
use reqwest::{Client as ReqwestClient, blocking, Method, header};
use pyo3::exceptions::PyValueError;
use pyo3::{Python, types::PyAnyMethods};
use serde_pyobject::to_pyobject;


#[pyclass]
struct Response {
    status_code: u16,
    reason_phrase: String,
    headers: HashMap<String, String>,
    content: Vec<u8>,
    elapsed: f64,
}

#[pymethods]
impl Response {
    #[getter]
    fn status_code(&self) -> u16 {
        self.status_code
    }

    #[getter]
    fn reason_phrase(&self) -> String {
        self.reason_phrase.clone()
    }

    #[getter]
    fn headers(&self) -> HashMap<String, String> {
        self.headers.clone()
    }

    #[getter]
    fn text(&self) -> PyResult<String> {
        String::from_utf8(self.content.clone())
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    #[getter]
    fn json<'a>(&self, py: Python<'a>) -> PyResult<&'a PyAny> {
        let json_value: serde_json::Value = serde_json::from_slice(&self.content)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        to_pyobject(py, &json_value).map(|b| b.into_gil_ref().into())
    }

    #[getter]
    fn elapsed(&self) -> f64 {
        self.elapsed
    }
}

/// A synchronous HTTP client with configuration options
#[pyclass]
struct Client {
    client: blocking::Client,
    base_url: Option<String>,
    timeout: Option<u64>,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
}

#[pymethods]
impl Client {
    #[getter]
    fn base_url(&self) -> Option<String> {
        self.base_url.clone()
    }

    #[getter]
    fn timeout(&self) -> Option<u64> {
        self.timeout
    }

    #[getter]
    fn follow_redirects(&self) -> bool {
        self.follow_redirects
    }

    #[getter]
    fn default_headers(&self) -> HashMap<String, String> {
        self.default_headers.clone()
    }

    /// Create a new Client instance with configuration
    #[new]
    #[pyo3(signature = (base_url=None, timeout=None, follow_redirects=None, default_headers=None))]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<HashMap<String, String>>,
    ) -> PyResult<Self> {
        let mut client_builder = blocking::Client::builder();
        
        if let Some(timeout_secs) = timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(timeout_secs));
        }
        
        if follow_redirects.unwrap_or(false) {
            client_builder = client_builder.redirect(reqwest::redirect::Policy::limited(10));
        } else {
            client_builder = client_builder.redirect(reqwest::redirect::Policy::none());
        }

        let client = client_builder.build()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(Client {
            client,
            base_url,
            timeout: timeout.map(|t| t as u64),
            follow_redirects: follow_redirects.unwrap_or(false),
            default_headers: default_headers.unwrap_or_else(HashMap::new),
        })
    }

    fn request(
        &self,
        method: &str,
        url: &str,
        params: Option<HashMap<String, String>>,
        headers: Option<HashMap<String, String>>,
        content: Option<Vec<u8>>,
        data: Option<HashMap<String, String>>,
        json: Option<&PyAny>,
    ) -> PyResult<Response> {
        let method = Method::from_bytes(method.as_bytes())
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        
        let mut request = self.client.request(method, url);

        if let Some(params) = params {
            request = request.query(&params);
        }

        if let Some(headers) = headers {
            let mut header_map = header::HeaderMap::new();
            for (k, v) in headers {
                header_map.insert(
                    header::HeaderName::from_bytes(k.as_bytes())
                        .map_err(|e| PyValueError::new_err(e.to_string()))?,
                    header::HeaderValue::from_str(&v)
                        .map_err(|e| PyValueError::new_err(e.to_string()))?,
                );
            }
            request = request.headers(header_map);
        }

        if let Some(content) = content {
            request = request.body(content);
        }

        if let Some(data) = data {
            request = request.form(&data);
        }

        if let Some(json_data) = json {
            let json_value = json_data.extract::<serde_json::Value>()?;
            request = request.json(&json_value);
        }

        let start = Instant::now();
        let response = request
            .send()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;
        
        let status = response.status();
        let headers: HashMap<String, String> = response
            .headers()
            .iter()
            .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
            .collect();
        
        let content = response
            .bytes()
            .map_err(|e| PyValueError::new_err(e.to_string()))?
            .to_vec();

        Ok(Response {
            status_code: status.as_u16(),
            reason_phrase: status.canonical_reason().unwrap_or("").to_string(),
            headers,
            content,
            elapsed: start.elapsed().as_secs_f64(),
        })
    }

    /// Send a GET request to the specified URL
    #[pyo3(text_signature = "(self, url, *, params=None, headers=None)")]
    fn get(
        &self,
        url: &str,
        params: Option<HashMap<String, String>>,
        headers: Option<HashMap<String, String>>,
    ) -> PyResult<Response> {
        self.request("GET", url, params, headers, None, None, None)
    }
}

/// An asynchronous HTTP client
#[pyclass]
struct AsyncClient {
    client: ReqwestClient,
    base_url: Option<String>,
    timeout: Option<u64>,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
}

#[pymethods]
impl AsyncClient {
    /// Create a new AsyncClient instance
    #[new]
    #[pyo3(text_signature = "(*, base_url=None, timeout=30, follow_redirects=False, default_headers=None)")]
    fn new(
        base_url: Option<String>,
        timeout: Option<f64>,
        follow_redirects: Option<bool>,
        default_headers: Option<HashMap<String, String>>,
    ) -> PyResult<Self> {
        let mut client_builder = ReqwestClient::builder();
        
        if let Some(timeout_secs) = timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(timeout_secs));
        }
        
        if follow_redirects.unwrap_or(false) {
            client_builder = client_builder.redirect(reqwest::redirect::Policy::limited(10));
        } else {
            client_builder = client_builder.redirect(reqwest::redirect::Policy::none());
        }

        let client = client_builder.build()
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(AsyncClient {
            client,
            base_url,
            timeout: timeout.map(|t| t as u64),
            follow_redirects: follow_redirects.unwrap_or(false),
            default_headers: default_headers.unwrap_or_else(HashMap::new),
        })
    }

    /// Send an asynchronous GET request to the specified URL
    ///
    /// Args:
    ///     url (str): The URL to send the request to
    ///
    /// Returns:
    ///     str: The response text
    ///
    /// This method must be awaited.
    #[pyo3(signature = (url))]
    fn get<'a>(&self, py: Python<'a>, url: &str) -> PyResult<&'a PyAny> {
        let client = self.client.clone();
        let url = url.to_string();
        
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let start = Instant::now();
            let response = client.get(&url)
                .send()
                .await
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            
            let status = response.status();
            let headers: HashMap<String, String> = response
                .headers()
                .iter()
                .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
                .collect();
            
            let content = response.bytes()
                .await
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            
            Ok(Response {
                status_code: status.as_u16(),
                reason_phrase: status.canonical_reason().unwrap_or("").to_string(),
                headers,
                content: content.to_vec(),
                elapsed: start.elapsed().as_secs_f64(),
            })
        })
    }
}

/// A Python library for making HTTP requests using reqwest
#[pymodule]
fn httpr(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_class::<AsyncClient>()?;
    Ok(())
}
