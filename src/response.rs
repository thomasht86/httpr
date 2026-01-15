// Allow await_holding_lock because we use a single-threaded Tokio runtime
// and the MutexGuards are intentionally held across block_on calls
#![allow(clippy::await_holding_lock)]

use crate::exceptions::{StreamClosed, StreamConsumed};
use crate::utils::{get_encoding_from_case_insensitive_headers, get_encoding_from_content};
use crate::RUNTIME;
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
use std::sync::{Arc, Mutex};

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
        Err(pyo3::exceptions::PyKeyError::new_err(format!(
            "Header key '{}' not found",
            key
        )))
    }

    fn __contains__(&self, key: String) -> bool {
        self.lowercase_map.contains_key(&key.to_lowercase())
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<PyAny>> {
        let iter = slf.headers.keys().cloned().collect::<Vec<_>>();
        Python::attach(|py| {
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
        py.detach(|| {
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

    fn json(&mut self, py: Python) -> Result<Py<PyAny>> {
        // Check if Content-Type is application/cbor
        let content_type = self.headers.get("content-type".to_string(), None);

        if content_type.to_lowercase().contains("application/cbor") {
            // Deserialize as CBOR
            let cbor_value: serde_json::Value =
                serde_cbor_2::from_reader(self.content.as_bytes(py))
                    .map_err(|e| anyhow!("Failed to deserialize CBOR: {}", e))?;
            let result = pythonize(py, &cbor_value)
                .map_err(|e| anyhow!("Failed to convert CBOR to Python object: {}", e))?
                .unbind();
            Ok(result)
        } else {
            // Deserialize as JSON (default)
            let json_value: serde_json::Value = from_slice(self.content.as_bytes(py))?;
            let result = pythonize(py, &json_value)
                .map_err(|e| anyhow!("Failed to convert JSON to Python object: {}", e))?
                .unbind();
            Ok(result)
        }
    }

    fn cbor(&mut self, py: Python) -> Result<Py<PyAny>> {
        let cbor_value: serde_json::Value = serde_cbor_2::from_reader(self.content.as_bytes(py))
            .map_err(|e| anyhow!("Failed to deserialize CBOR: {}", e))?;
        let result = pythonize(py, &cbor_value)
            .map_err(|e| anyhow!("Failed to convert CBOR to Python object: {}", e))?
            .unbind();
        Ok(result)
    }

    #[getter]
    fn text_markdown(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text = py.detach(|| from_read(raw_bytes, 100))?;
        Ok(text)
    }

    #[getter]
    fn text_plain(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text =
            py.detach(|| from_read_with_decorator(raw_bytes, 100, TrivialDecorator::new()))?;
        Ok(text)
    }

    #[getter]
    fn text_rich(&mut self, py: Python) -> Result<String> {
        let raw_bytes = self.content.bind(py).as_bytes();
        let text = py.detach(|| from_read_with_decorator(raw_bytes, 100, RichDecorator::new()))?;
        Ok(text)
    }
}

/// A streaming HTTP response that allows iterating over chunks of data.
///
/// This struct holds the reqwest Response and provides methods to iterate over
/// the response body in chunks without buffering the entire response in memory.
#[pyclass]
pub struct StreamingResponse {
    response: Arc<Mutex<Option<reqwest::Response>>>,
    #[pyo3(get)]
    pub cookies: IndexMap<String, String, RandomState>,
    #[pyo3(get)]
    pub headers: CaseInsensitiveHeaderMap,
    #[pyo3(get)]
    pub status_code: u16,
    #[pyo3(get)]
    pub url: String,
    closed: Arc<Mutex<bool>>,
    consumed: Arc<Mutex<bool>>,
    encoding: Arc<Mutex<Option<String>>>,
}

impl StreamingResponse {
    /// Create a new StreamingResponse from a reqwest::Response
    pub fn new(
        response: reqwest::Response,
        cookies: IndexMap<String, String, RandomState>,
        headers: CaseInsensitiveHeaderMap,
        status_code: u16,
        url: String,
    ) -> Self {
        StreamingResponse {
            response: Arc::new(Mutex::new(Some(response))),
            cookies,
            headers,
            status_code,
            url,
            closed: Arc::new(Mutex::new(false)),
            consumed: Arc::new(Mutex::new(false)),
            encoding: Arc::new(Mutex::new(None)),
        }
    }

    fn check_state(&self) -> PyResult<()> {
        let closed = self.closed.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        if *closed {
            return Err(StreamClosed::new_err("Response stream has been closed"));
        }

        let consumed = self.consumed.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        if *consumed {
            return Err(StreamConsumed::new_err(
                "Response stream has already been consumed",
            ));
        }
        Ok(())
    }

    fn get_encoding_internal(&self) -> String {
        // Check if encoding is already cached
        if let Ok(encoding_guard) = self.encoding.lock() {
            if let Some(ref enc) = *encoding_guard {
                return enc.clone();
            }
        }

        // Try to detect encoding from headers
        let encoding = get_encoding_from_case_insensitive_headers(&self.headers)
            .unwrap_or_else(|| "utf-8".to_string());

        // Cache the encoding
        if let Ok(mut encoding_guard) = self.encoding.lock() {
            *encoding_guard = Some(encoding.clone());
        }

        encoding
    }
}

#[pymethods]
impl StreamingResponse {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&self, py: Python) -> PyResult<Option<Py<PyBytes>>> {
        self.check_state()?;

        let response_arc = Arc::clone(&self.response);
        let consumed_arc = Arc::clone(&self.consumed);

        // Release GIL while fetching the next chunk
        let result = py.detach(|| {
            RUNTIME.block_on(async {
                let mut response_guard = response_arc
                    .lock()
                    .map_err(|e| anyhow::anyhow!("Failed to acquire response lock: {}", e))?;

                if let Some(ref mut resp) = *response_guard {
                    match resp.chunk().await {
                        Ok(Some(chunk)) => Ok(Some(chunk)),
                        Ok(None) => {
                            // Stream exhausted, mark as consumed
                            if let Ok(mut consumed) = consumed_arc.lock() {
                                *consumed = true;
                            }
                            Ok(None)
                        }
                        Err(e) => Err(anyhow::anyhow!("Error reading chunk: {}", e)),
                    }
                } else {
                    // Response already taken, mark as consumed
                    if let Ok(mut consumed) = consumed_arc.lock() {
                        *consumed = true;
                    }
                    Ok(None)
                }
            })
        });

        match result {
            Ok(Some(chunk)) => Ok(Some(PyBytes::new(py, &chunk).unbind())),
            Ok(None) => Ok(None),
            Err(e) => Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
        }
    }

    /// Iterate over the response body as bytes chunks.
    ///
    /// Yields chunks of bytes as they are received from the server.
    /// The chunk size is determined by the server and network conditions.
    ///
    /// # Example
    /// ```python
    /// with client.stream("GET", url) as response:
    ///     for chunk in response.iter_bytes():
    ///         process(chunk)
    /// ```
    fn iter_bytes(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    /// Iterate over the response body as text chunks.
    ///
    /// Decodes each chunk using the response's encoding (from Content-Type header
    /// or defaulting to UTF-8).
    ///
    /// # Example
    /// ```python
    /// with client.stream("GET", url) as response:
    ///     for text in response.iter_text():
    ///         print(text)
    /// ```
    fn iter_text(&self, _py: Python) -> PyResult<TextIterator> {
        self.check_state()?;
        Ok(TextIterator {
            response: Arc::clone(&self.response),
            closed: Arc::clone(&self.closed),
            consumed: Arc::clone(&self.consumed),
            encoding: self.get_encoding_internal(),
        })
    }

    /// Iterate over the response body line by line.
    ///
    /// Decodes the response and yields complete lines (including newline characters).
    ///
    /// # Example
    /// ```python
    /// with client.stream("GET", url) as response:
    ///     for line in response.iter_lines():
    ///         print(line.strip())
    /// ```
    fn iter_lines(&self, _py: Python) -> PyResult<LineIterator> {
        self.check_state()?;
        Ok(LineIterator {
            response: Arc::clone(&self.response),
            closed: Arc::clone(&self.closed),
            consumed: Arc::clone(&self.consumed),
            encoding: self.get_encoding_internal(),
            buffer: String::new(),
        })
    }

    /// Read the entire response body into memory.
    ///
    /// This consumes the stream and returns all remaining bytes.
    /// After calling this method, the stream cannot be iterated again.
    ///
    /// # Example
    /// ```python
    /// with client.stream("GET", url) as response:
    ///     if response.status_code == 200:
    ///         content = response.read()
    /// ```
    fn read(&self, py: Python) -> PyResult<Py<PyBytes>> {
        self.check_state()?;

        let response_arc = Arc::clone(&self.response);
        let consumed_arc = Arc::clone(&self.consumed);

        let result = py.detach(|| {
            RUNTIME.block_on(async {
                let mut response_guard = response_arc
                    .lock()
                    .map_err(|e| anyhow::anyhow!("Failed to acquire response lock: {}", e))?;

                if let Some(resp) = response_guard.take() {
                    let bytes = resp
                        .bytes()
                        .await
                        .map_err(|e| anyhow::anyhow!("Error reading response body: {}", e))?;

                    // Mark as consumed
                    if let Ok(mut consumed) = consumed_arc.lock() {
                        *consumed = true;
                    }

                    Ok(bytes)
                } else {
                    Err(anyhow::anyhow!("Response already consumed"))
                }
            })
        });

        match result {
            Ok(bytes) => Ok(PyBytes::new(py, &bytes).unbind()),
            Err(e) => Err(StreamConsumed::new_err(e.to_string())),
        }
    }

    /// Close the streaming response and release resources.
    ///
    /// After closing, no more data can be read from the stream.
    /// This is automatically called when using the stream as a context manager.
    fn close(&self) -> PyResult<()> {
        let mut closed = self.closed.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        *closed = true;

        // Drop the response to release resources
        let mut response = self.response.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        *response = None;

        Ok(())
    }

    /// Check if the stream has been closed.
    #[getter]
    fn is_closed(&self) -> PyResult<bool> {
        let closed = self.closed.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        Ok(*closed)
    }

    /// Check if the stream has been fully consumed.
    #[getter]
    fn is_consumed(&self) -> PyResult<bool> {
        let consumed = self.consumed.lock().map_err(|e| {
            pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
        })?;
        Ok(*consumed)
    }
}

/// Iterator for text chunks
#[pyclass]
pub struct TextIterator {
    response: Arc<Mutex<Option<reqwest::Response>>>,
    closed: Arc<Mutex<bool>>,
    consumed: Arc<Mutex<bool>>,
    encoding: String,
}

#[pymethods]
impl TextIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&self, py: Python) -> PyResult<Option<String>> {
        // Check closed state
        {
            let closed = self.closed.lock().map_err(|e| {
                pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
            })?;
            if *closed {
                return Err(StreamClosed::new_err("Response stream has been closed"));
            }
        }

        let response_arc = Arc::clone(&self.response);
        let consumed_arc = Arc::clone(&self.consumed);
        let encoding_name = self.encoding.clone();

        let result = py.detach(|| {
            RUNTIME.block_on(async {
                let mut response_guard = response_arc
                    .lock()
                    .map_err(|e| anyhow::anyhow!("Failed to acquire response lock: {}", e))?;

                if let Some(ref mut resp) = *response_guard {
                    match resp.chunk().await {
                        Ok(Some(chunk)) => {
                            // Decode the chunk using the encoding
                            let encoding = Encoding::for_label(encoding_name.as_bytes())
                                .unwrap_or(encoding_rs::UTF_8);
                            let (decoded, _, _) = encoding.decode(&chunk);
                            Ok(Some(decoded.to_string()))
                        }
                        Ok(None) => {
                            if let Ok(mut consumed) = consumed_arc.lock() {
                                *consumed = true;
                            }
                            Ok(None)
                        }
                        Err(e) => Err(anyhow::anyhow!("Error reading chunk: {}", e)),
                    }
                } else {
                    if let Ok(mut consumed) = consumed_arc.lock() {
                        *consumed = true;
                    }
                    Ok(None)
                }
            })
        });

        match result {
            Ok(opt) => Ok(opt),
            Err(e) => Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
        }
    }
}

/// Iterator for lines
#[pyclass]
pub struct LineIterator {
    response: Arc<Mutex<Option<reqwest::Response>>>,
    closed: Arc<Mutex<bool>>,
    consumed: Arc<Mutex<bool>>,
    encoding: String,
    buffer: String,
}

#[pymethods]
impl LineIterator {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self, py: Python) -> PyResult<Option<String>> {
        // Check closed state
        {
            let closed = self.closed.lock().map_err(|e| {
                pyo3::exceptions::PyRuntimeError::new_err(format!("Failed to acquire lock: {}", e))
            })?;
            if *closed {
                return Err(StreamClosed::new_err("Response stream has been closed"));
            }
        }

        // First check if we have a complete line in the buffer
        if let Some(newline_pos) = self.buffer.find('\n') {
            let line = self.buffer[..=newline_pos].to_string();
            self.buffer = self.buffer[newline_pos + 1..].to_string();
            return Ok(Some(line));
        }

        let response_arc = Arc::clone(&self.response);
        let consumed_arc = Arc::clone(&self.consumed);
        let encoding_name = self.encoding.clone();

        loop {
            let result = py.detach(|| {
                RUNTIME.block_on(async {
                    let mut response_guard = response_arc
                        .lock()
                        .map_err(|e| anyhow::anyhow!("Failed to acquire response lock: {}", e))?;

                    if let Some(ref mut resp) = *response_guard {
                        match resp.chunk().await {
                            Ok(Some(chunk)) => {
                                let encoding = Encoding::for_label(encoding_name.as_bytes())
                                    .unwrap_or(encoding_rs::UTF_8);
                                let (decoded, _, _) = encoding.decode(&chunk);
                                Ok(Some(decoded.to_string()))
                            }
                            Ok(None) => {
                                if let Ok(mut consumed) = consumed_arc.lock() {
                                    *consumed = true;
                                }
                                Ok(None)
                            }
                            Err(e) => Err(anyhow::anyhow!("Error reading chunk: {}", e)),
                        }
                    } else {
                        if let Ok(mut consumed) = consumed_arc.lock() {
                            *consumed = true;
                        }
                        Ok(None)
                    }
                })
            });

            match result {
                Ok(Some(text)) => {
                    self.buffer.push_str(&text);

                    // Check if we now have a complete line
                    if let Some(newline_pos) = self.buffer.find('\n') {
                        let line = self.buffer[..=newline_pos].to_string();
                        self.buffer = self.buffer[newline_pos + 1..].to_string();
                        return Ok(Some(line));
                    }
                    // Continue reading if no newline found
                }
                Ok(None) => {
                    // Stream ended, return remaining buffer if not empty
                    if !self.buffer.is_empty() {
                        let remaining = std::mem::take(&mut self.buffer);
                        return Ok(Some(remaining));
                    }
                    return Ok(None);
                }
                Err(e) => return Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
            }
        }
    }
}
