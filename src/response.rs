use crate::utils::{get_encoding_from_content, get_encoding_from_case_insensitive_headers};
use anyhow::{anyhow, Result};
use encoding_rs::Encoding;
use foldhash::fast::RandomState;
use html2text::{
    from_read, from_read_with_decorator,
    render::{RichDecorator, TrivialDecorator},
};
use indexmap::IndexMap;
use pyo3::{prelude::*, types::PyBytes, IntoPyObject};
use pythonize::pythonize;
use serde_json::from_slice;

/// A struct representing an HTTP response.
///
/// This struct provides methods to access various parts of an HTTP response, such as headers, cookies, status code, and the response body.
/// It also supports decoding the response body as text or JSON, with the ability to specify the character encoding.
#[pyclass]
#[derive(Clone)]
pub struct CaseInsensitiveHeaderMap {
    headers: IndexMap<String, String, RandomState>,
    lowercase_map: IndexMap<String, String, RandomState>,
}

#[pymethods]
impl CaseInsensitiveHeaderMap {
    #[new]
    fn new() -> Self {
        CaseInsensitiveHeaderMap {
            headers: IndexMap::with_hasher(RandomState::default()),
            lowercase_map: IndexMap::with_hasher(RandomState::default()),
        }
    }

    fn __getitem__(&self, key: String) -> PyResult<String> {
        let lower_key = key.to_lowercase();
        if let Some(original_key) = self.lowercase_map.get(&lower_key) {
            if let Some(value) = self.headers.get(original_key) {
                return Ok(value.clone());
            }
        }
        Err(pyo3::exceptions::PyKeyError::new_err(format!("Header key '{}' not found", key)))
    }

    fn __contains__(&self, key: String) -> bool {
        self.lowercase_map.contains_key(&key.to_lowercase())
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<PyAny>> {
        let iter = slf.headers.keys().cloned().collect::<Vec<_>>();
        Python::with_gil(|py| {
            let iter_obj = iter.into_pyobject(py)?;
            let iter_method = iter_obj.getattr("__iter__")?;
            let py_iter = iter_method.call0()?;
            Ok(py_iter.into())
        })
    }

    fn items(&self) -> Vec<(String, String)> {
        self.headers.clone().into_iter().collect()
    }

    fn keys(&self) -> Vec<String> {
        self.headers.keys().cloned().collect()
    }

    fn values(&self) -> Vec<String> {
        self.headers.values().cloned().collect()
    }

    #[pyo3(signature = (key, default=None))]
    fn get(&self, key: String, default: Option<String>) -> String {
        let lower_key = key.to_lowercase();
        if let Some(original_key) = self.lowercase_map.get(&lower_key) {
            if let Some(value) = self.headers.get(original_key) {
                return value.clone();
            }
        }
        default.unwrap_or_default()
    }
}

impl CaseInsensitiveHeaderMap {
    // Public constructor for Rust code
    pub fn create() -> Self {
        CaseInsensitiveHeaderMap {
            headers: IndexMap::with_hasher(RandomState::default()),
            lowercase_map: IndexMap::with_hasher(RandomState::default()),
        }
    }

    // Helper method to insert a header
    pub fn insert(&mut self, key: String, value: String) {
        let lower_key = key.to_lowercase();
        self.lowercase_map.insert(lower_key, key.clone());
        self.headers.insert(key, value);
    }

    // Helper method to build from an IndexMap
    pub fn from_indexmap(map: IndexMap<String, String, RandomState>) -> Self {
        let mut headers_map = CaseInsensitiveHeaderMap::create();
        for (key, value) in map {
            headers_map.insert(key, value);
        }
        headers_map
    }
    
    // Public method to check if a header exists
    pub fn contains_key(&self, key: &str) -> bool {
        self.lowercase_map.contains_key(&key.to_lowercase())
    }
    
    // Public method to get a header value
    pub fn get_value(&self, key: &str) -> Option<String> {
        let lower_key = key.to_lowercase();
        if let Some(original_key) = self.lowercase_map.get(&lower_key) {
            if let Some(value) = self.headers.get(original_key) {
                return Some(value.clone());
            }
        }
        None
    }
}

#[pyclass]
pub struct Response {
    #[pyo3(get)]
    pub content: Py<PyBytes>,
    #[pyo3(get)]
    pub cookies: IndexMap<String, String, RandomState>,
    #[pyo3(get, set)]
    pub encoding: String,
    #[pyo3(get)]
    pub headers: CaseInsensitiveHeaderMap,
    #[pyo3(get)]
    pub status_code: u16,
    #[pyo3(get)]
    pub url: String,
}

#[pymethods]
impl Response {
    #[getter]
    fn get_encoding(&mut self, py: Python) -> Result<&String> {
        if !self.encoding.is_empty() {
            return Ok(&self.encoding);
        }
        self.encoding = get_encoding_from_case_insensitive_headers(&self.headers)
            .or_else(|| get_encoding_from_content(self.content.as_bytes(py)))
            .unwrap_or_else(|| "utf-8".to_string());
        Ok(&self.encoding)
    }

    #[getter]
    fn text(&mut self, py: Python) -> Result<String> {
        // If self.encoding is empty, call get_encoding to populate self.encoding
        if self.encoding.is_empty() {
            self.get_encoding(py)?;
        }

        // Convert Py<PyBytes> to &[u8]
        let raw_bytes = self.content.as_bytes(py);

        // Release the GIL here because decoding can be CPU-intensive
        py.allow_threads(|| {
            let encoding = Encoding::for_label(self.encoding.as_bytes())
                .ok_or_else(|| anyhow!("Unsupported charset: {}", self.encoding))?;
            let (decoded_str, detected_encoding, _) = encoding.decode(raw_bytes);

            // Update self.encoding based on the detected encoding
            if self.encoding != detected_encoding.name() {
                self.encoding = detected_encoding.name().to_string();
            }

            Ok(decoded_str.to_string())
        })
    }

    fn json(&mut self, py: Python) -> Result<PyObject> {
        let json_value: serde_json::Value = from_slice(self.content.as_bytes(py))?;
        let result = pythonize(py, &json_value)
            .map_err(|e| anyhow!("Failed to convert JSON to Python object: {}", e))?
            .unbind();
        Ok(result)
    }

    #[getter]
    fn text_markdown(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text = py.allow_threads(|| from_read(raw_bytes, 100))?;
        Ok(text)
    }

    #[getter]
    fn text_plain(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text =
            py.allow_threads(|| from_read_with_decorator(raw_bytes, 100, TrivialDecorator::new()))?;
        Ok(text)
    }

    #[getter]
    fn text_rich(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text =
            py.allow_threads(|| from_read_with_decorator(raw_bytes, 100, RichDecorator::new()))?;
        Ok(text)
    }
}
