#![allow(non_local_definitions)]

use std::collections::HashMap;
use std::time::Duration;
use pyo3::prelude::*;
use reqwest::{Client as ReqwestClient, blocking};
use pyo3::exceptions::PyValueError;

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
    /// Create a new Client instance with configuration
    #[new]
    #[pyo3(text_signature = "(*, base_url=None, timeout=30, follow_redirects=False, default_headers=None)")]
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

    /// Send a GET request to the specified URL
    ///
    /// Args:
    ///     url (str): The URL to send the request to
    ///
    /// Returns:
    ///     str: The response text
    #[pyo3(text_signature = "(self, url)")]
    fn get(&self, url: &str) -> PyResult<String> {
        self.client
            .get(url)
            .send()
            .map_err(|e| PyValueError::new_err(e.to_string()))?
            .text()
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }
}

/// An asynchronous HTTP client
#[pyclass]
struct AsyncClient {
    client: ReqwestClient,
    follow_redirects: bool,
}

#[pymethods]
impl AsyncClient {
    /// Create a new AsyncClient instance
    #[new]
    #[pyo3(text_signature = "(*, follow_redirects=False)")]
    fn new(follow_redirects: Option<bool>) -> Self {
        let client = ReqwestClient::builder()
            .redirect(if follow_redirects.unwrap_or(false) {
                reqwest::redirect::Policy::limited(10)
            } else {
                reqwest::redirect::Policy::none()
            })
            .build()
            .unwrap();

        AsyncClient {
            client,
            follow_redirects: follow_redirects.unwrap_or(false),
        }
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
    #[pyo3(text_signature = "(self, url)")]
    fn get<'a>(&self, py: Python<'a>, url: &str) -> PyResult<&'a PyAny> {
        let client = self.client.clone();
        let url = url.to_string();
        
        pyo3_asyncio::tokio::future_into_py(py, async move {
            match client.get(&url).send().await {
                Ok(resp) => match resp.text().await {
                    Ok(text) => Ok(text),
                    Err(e) => Err(PyValueError::new_err(e.to_string()))
                },
                Err(e) => Err(PyValueError::new_err(e.to_string()))
            }
        })
    }
}

/// A Python library for making HTTP requests using reqwest
#[pymodule]
fn httpr(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("Client", py.get_type::<Client>())?;
    m.add("AsyncClient", py.get_type::<AsyncClient>())?;
    Ok(())
}
