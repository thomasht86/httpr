use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
    types::PyDict,
    PyObject, PyResult, Python
};
use pyo3_serde::from_pyany;
use pyo3_asyncio::tokio::future_into_py;
use reqwest::blocking::ClientBuilder as BlockingClientBuilder;
use reqwest::redirect::Policy as RedirectPolicy;
use reqwest::{Client as AsyncReqwestClient, ClientBuilder as AsyncClientBuilder};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[derive(Debug, Clone)]
struct ResponseMetadata {
    status_code: u16,
    headers: HashMap<String, String>,
}

/// Update the cookie store from any `Set-Cookie` headers.
fn update_cookies(
    cookie_store: &Mutex<HashMap<String, String>>,
    headers: &reqwest::header::HeaderMap,
) {
    for cookie_val in headers.get_all(reqwest::header::SET_COOKIE).iter() {
        if let Ok(cookie_str) = cookie_val.to_str() {
            if let Some((key, value)) = cookie_str.split(';').next().and_then(|s| s.split_once('=')) {
                let mut store = cookie_store.lock().unwrap();
                store.insert(key.trim().to_string(), value.trim().to_string());
            }
        }
    }
}

/// Naively check if a URL is absolute.
fn is_absolute_url(url: &str) -> bool {
    url.starts_with("http://") || url.starts_with("https://")
}

/// Synchronous HTTP client.
#[pyclass]
#[derive(Debug)]
struct Client {
    base_url: Option<String>,
    timeout: f64,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
    inner: reqwest::blocking::Client,
    cookies: Mutex<HashMap<String, String>>,
    last_response: Mutex<Option<ResponseMetadata>>,
}

#[pymethods]
impl Client {
    // Provide a Python signature so that default values for all parameters are unambiguous.
    #[new]
    #[pyo3(signature = (base_url=None, timeout=10.0, follow_redirects=True, default_headers=None))]
    fn new(
        base_url: Option<String>,
        timeout: f64,
        follow_redirects: bool,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        if timeout < 0.0 {
            return Err(PyValueError::new_err("timeout must be non-negative"));
        }
        let mut builder = BlockingClientBuilder::new();
        builder = builder.timeout(Duration::from_secs_f64(timeout));
        if !follow_redirects {
            builder = builder.redirect(RedirectPolicy::none());
        }
        let mut headers_map = reqwest::header::HeaderMap::new();
        let mut header_store = HashMap::new();
        if let Some(py_dict) = default_headers {
            for (k, v) in py_dict {
                let key_str = k.extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers keys must be strings"))?;
                let val_str = v.extract::<String>()
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
        let final_client = builder.build()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to build client: {}", e)))?;
        Ok(Self {
            base_url,
            timeout,
            follow_redirects,
            default_headers: header_store,
            inner: final_client,
            cookies: Mutex::new(HashMap::new()),
            last_response: Mutex::new(None),
        })
    }

    #[pyo3(signature = (url, params=None, headers=None))]
    fn get(&self, url: &str, params: Option<&PyDict>, headers: Option<&PyDict>) -> PyResult<String> {
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

        let mut request = self.inner.get(&final_url);
        if let Some(py_params) = params {
            let mut param_map = HashMap::new();
            for (k, v) in py_params {
                let key = k.extract::<String>()?;
                let value = v.extract::<String>()?;
                param_map.insert(key, value);
            }
            request = request.query(&param_map);
        }
        if let Some(py_headers) = headers {
            for (k, v) in py_headers {
                let key_str = k.extract::<String>()?;
                let val_str = v.extract::<String>()?;
                request = request.header(key_str, val_str);
            }
        }
        let resp = request.send().map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
        let meta = ResponseMetadata {
            status_code: resp.status().as_u16(),
            headers: resp.headers().iter()
                .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
                .collect(),
        };
        {
            let mut lr = self.last_response.lock().unwrap();
            *lr = Some(meta);
        }
        update_cookies(&self.cookies, resp.headers());
        resp.text().map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    #[pyo3(signature = (url, data=None, json=None, params=None, headers=None))]
    fn post(
        &self,
        url: &str,
        data: Option<&PyDict>,
        json: Option<&PyAny>,
        params: Option<&PyDict>,
        headers: Option<&PyDict>,
    ) -> PyResult<String> {
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

        let mut request = self.inner.post(&final_url);
        if let Some(py_params) = params {
            let mut param_map = HashMap::new();
            for (k, v) in py_params {
                let key = k.extract::<String>()?;
                let value = v.extract::<String>()?;
                param_map.insert(key, value);
            }
            request = request.query(&param_map);
        }
        if let Some(py_headers) = headers {
            for (k, v) in py_headers {
                let key_str = k.extract::<String>()?;
                let val_str = v.extract::<String>()?;
                request = request.header(key_str, val_str);
            }
        }
        if let Some(form_data) = data {
            let mut form_map = HashMap::new();
            for (k, v) in form_data {
                let key = k.extract::<String>()?;
                let value = v.extract::<String>()?;
                form_map.insert(key, value);
            }
            request = request.form(&form_map);
        } else if let Some(json_obj) = json {
            // Use pyo3_serde to convert the PyAny into a serde_json::Value.
            let json_value = from_pyany(json_obj)
                .map_err(|e| PyValueError::new_err(e.to_string()))?;
            request = request.json(&json_value);
        }
        let resp = request.send().map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
        let meta = ResponseMetadata {
            status_code: resp.status().as_u16(),
            headers: resp.headers().iter()
                .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
                .collect(),
        };
        {
            let mut lr = self.last_response.lock().unwrap();
            *lr = Some(meta);
        }
        update_cookies(&self.cookies, resp.headers());
        resp.text().map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    // Property getters.
    #[getter]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        let store = self.cookies.lock().unwrap();
        for (k, v) in &*store {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }

    #[getter(_last_response)]
    fn last_response_py(&self, py: Python) -> PyResult<Option<PyObject>> {
        let lr = self.last_response.lock().unwrap();
        if let Some(meta) = &*lr {
            let dict = PyDict::new(py);
            dict.set_item("status_code", meta.status_code)?;
            dict.set_item("headers", &meta.headers)?;
            Ok(Some(dict.to_object(py)))
        } else {
            Ok(None)
        }
    }

    #[pyo3(get)]
    fn base_url(&self) -> Option<String> {
        self.base_url.clone()
    }

    #[pyo3(get)]
    fn timeout(&self) -> f64 {
        self.timeout
    }

    #[pyo3(get)]
    fn follow_redirects(&self) -> bool {
        self.follow_redirects
    }

    #[pyo3(get)]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        for (k, v) in &self.default_headers {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

/// Asynchronous HTTP client.
#[pyclass]
#[derive(Debug, Clone)]
struct AsyncClient {
    base_url: Option<String>,
    timeout: f64,
    follow_redirects: bool,
    default_headers: HashMap<String, String>,
    inner: AsyncReqwestClient,
    cookies: Arc<Mutex<HashMap<String, String>>>,
    last_response: Arc<Mutex<Option<ResponseMetadata>>>,
}

#[pymethods]
impl AsyncClient {
    #[new]
    #[pyo3(signature = (base_url=None, timeout=10.0, follow_redirects=True, default_headers=None))]
    fn new(
        base_url: Option<String>,
        timeout: f64,
        follow_redirects: bool,
        default_headers: Option<&PyDict>,
    ) -> PyResult<Self> {
        if timeout < 0.0 {
            return Err(PyValueError::new_err("timeout must be non-negative"));
        }
        let mut builder = AsyncClientBuilder::new();
        builder = builder.timeout(Duration::from_secs_f64(timeout));
        if !follow_redirects {
            builder = builder.redirect(RedirectPolicy::none());
        }
        let mut headers_map = reqwest::header::HeaderMap::new();
        let mut header_store = HashMap::new();
        if let Some(py_dict) = default_headers {
            for (k, v) in py_dict {
                let key_str = k.extract::<String>()
                    .map_err(|_| PyValueError::new_err("default_headers keys must be strings"))?;
                let val_str = v.extract::<String>()
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
        let final_client = builder.build()
            .map_err(|e| PyRuntimeError::new_err(format!("Failed to build async client: {}", e)))?;
        Ok(Self {
            base_url,
            timeout,
            follow_redirects,
            default_headers: header_store,
            inner: final_client,
            cookies: Arc::new(Mutex::new(HashMap::new())),
            last_response: Arc::new(Mutex::new(None)),
        })
    }

    #[pyo3(signature = (url, params=None, headers=None))]
    fn get<'a>(
        &'a self,
        py: Python<'a>,
        url: &str,
        params: Option<&PyDict>,
        headers: Option<&PyDict>,
    ) -> PyResult<&'a PyAny> {
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
        let cookies_store = self.cookies.clone();
        let last_response = self.last_response.clone();
        let params_map = if let Some(py_params) = params {
            let mut map = HashMap::new();
            for (k, v) in py_params {
                map.insert(k.extract::<String>()?, v.extract::<String>()?);
            }
            Some(map)
        } else {
            None
        };
        let headers_map = if let Some(py_headers) = headers {
            let mut map = HashMap::new();
            for (k, v) in py_headers {
                map.insert(k.extract::<String>()?, v.extract::<String>()?);
            }
            Some(map)
        } else {
            None
        };
        pyo3_tokio::future_into_py(py, async move {
            let mut request = client.get(&final_url);
            if let Some(ref params) = params_map {
                request = request.query(params);
            }
            if let Some(ref headers) = headers_map {
                for (k, v) in headers {
                    request = request.header(k, v);
                }
            }
            let resp = request.send().await.map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
            let meta = ResponseMetadata {
                status_code: resp.status().as_u16(),
                headers: resp.headers().iter()
                    .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
                    .collect(),
            };
            {
                let mut lr = last_response.lock().unwrap();
                *lr = Some(meta);
            }
            update_cookies(&*cookies_store, resp.headers());
            let text = resp.text().await.map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
            Ok(text)
        })
    }

    #[pyo3(signature = (url, data=None, json=None, params=None, headers=None))]
    fn post<'a>(
        &'a self,
        py: Python<'a>,
        url: &str,
        data: Option<&PyDict>,
        json: Option<&PyAny>,
        params: Option<&PyDict>,
        headers: Option<&PyDict>,
    ) -> PyResult<&'a PyAny> {
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
        let cookies_store = self.cookies.clone();
        let last_response = self.last_response.clone();
        let params_map = if let Some(py_params) = params {
            let mut map = HashMap::new();
            for (k, v) in py_params {
                map.insert(k.extract::<String>()?, v.extract::<String>()?);
            }
            Some(map)
        } else {
            None
        };
        let headers_map = if let Some(py_headers) = headers {
            let mut map = HashMap::new();
            for (k, v) in py_headers {
                map.insert(k.extract::<String>()?, v.extract::<String>()?);
            }
            Some(map)
        } else {
            None
        };
        pyo3_tokio::future_into_py(py, async move {
            let mut request = client.post(&final_url);
            if let Some(ref params) = params_map {
                request = request.query(params);
            }
            if let Some(ref headers) = headers_map {
                for (k, v) in headers {
                    request = request.header(k, v);
                }
            }
            if let Some(form_data) = data {
                let mut map = HashMap::new();
                for (k, v) in form_data {
                    map.insert(k.extract::<String>()?, v.extract::<String>()?);
                }
                request = request.form(&map);
            } else if let Some(json_obj) = json {
                let json_value = from_pyany(json_obj)
                    .map_err(|e| PyValueError::new_err(e.to_string()))?;
                request = request.json(&json_value);
            }
            let resp = request.send().await.map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
            let meta = ResponseMetadata {
                status_code: resp.status().as_u16(),
                headers: resp.headers().iter()
                    .map(|(k, v)| (k.to_string(), v.to_str().unwrap_or("").to_string()))
                    .collect(),
            };
            {
                let mut lr = last_response.lock().unwrap();
                *lr = Some(meta);
            }
            update_cookies(&*cookies_store, resp.headers());
            let text = resp.text().await.map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
            Ok(text)
        })
    }

    #[pyo3(get)]
    fn cookies<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        let store = self.cookies.lock().unwrap();
        for (k, v) in &*store {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }

    #[pyo3(get, name = "_last_response")]
    fn last_response_py(&self, py: Python) -> PyResult<Option<PyObject>> {
        let lr = self.last_response.lock().unwrap();
        if let Some(meta) = &*lr {
            let dict = PyDict::new(py);
            dict.set_item("status_code", meta.status_code)?;
            dict.set_item("headers", &meta.headers)?;
            Ok(Some(dict.to_object(py)))
        } else {
            Ok(None)
        }
    }

    #[pyo3(get)]
    fn base_url(&self) -> Option<String> {
        self.base_url.clone()
    }

    #[pyo3(get)]
    fn timeout(&self) -> f64 {
        self.timeout
    }

    #[pyo3(get)]
    fn follow_redirects(&self) -> bool {
        self.follow_redirects
    }

    #[pyo3(get)]
    fn default_headers<'py>(&self, py: Python<'py>) -> PyResult<&'py PyDict> {
        let dict = PyDict::new(py);
        for (k, v) in &self.default_headers {
            dict.set_item(k, v)?;
        }
        Ok(dict)
    }
}

#[pymodule]
fn httpr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_class::<AsyncClient>()?;
    Ok(())
}
