#![allow(non_local_definitions)]

use pyo3::prelude::*;
use reqwest::{Client as ReqwestClient, blocking};
use pyo3::exceptions::PyValueError;

/// A synchronous HTTP client
#[pyclass]
struct Client {
    client: blocking::Client,
}

#[pymethods]
impl Client {
    /// Create a new Client instance
    #[new]
    #[pyo3(text_signature = "()")]
    fn new() -> Self {
        Client {
            client: blocking::Client::new(),
        }
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
}

#[pymethods]
impl AsyncClient {
    /// Create a new AsyncClient instance
    #[new]
    #[pyo3(text_signature = "()")]
    fn new() -> Self {
        AsyncClient {
            client: ReqwestClient::new(),
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
