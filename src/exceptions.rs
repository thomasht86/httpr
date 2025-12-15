use pyo3::create_exception;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;

// Base exception - HTTPError
create_exception!(httpr, HTTPError, PyException, "Base class for all httpr exceptions.");

// RequestError - base for all request exceptions
create_exception!(httpr, RequestError, HTTPError, "Base class for all exceptions that may occur when issuing a `.request()`.");

// TransportError - base for transport-level errors
create_exception!(httpr, TransportError, RequestError, "Base class for all exceptions that occur at the level of the Transport API.");

// NetworkError - base for network-related errors  
create_exception!(httpr, NetworkError, TransportError, "The base class for network-related errors.");

// TimeoutException - base for timeout errors
create_exception!(httpr, TimeoutException, TransportError, "The base class for timeout errors.");

// ProtocolError - base for protocol violations
create_exception!(httpr, ProtocolError, TransportError, "The protocol was violated.");

// StreamError - base for stream-related errors
create_exception!(httpr, StreamError, PyException, "The base class for stream exceptions.");

// Specific timeout exceptions
create_exception!(httpr, ConnectTimeout, TimeoutException, "Timed out while connecting to the host.");
create_exception!(httpr, ReadTimeout, TimeoutException, "Timed out while receiving data from the host.");
create_exception!(httpr, WriteTimeout, TimeoutException, "Timed out while sending data to the host.");
create_exception!(httpr, PoolTimeout, TimeoutException, "Timed out waiting to acquire a connection from the pool.");

// Specific network exceptions
create_exception!(httpr, ConnectError, NetworkError, "Failed to establish a connection.");
create_exception!(httpr, ReadError, NetworkError, "Failed to receive data from the network.");
create_exception!(httpr, WriteError, NetworkError, "Failed to send data through the network.");
create_exception!(httpr, CloseError, NetworkError, "Failed to close a connection.");

// Protocol exceptions
create_exception!(httpr, LocalProtocolError, ProtocolError, "A protocol was violated by the client.");
create_exception!(httpr, RemoteProtocolError, ProtocolError, "The protocol was violated by the server.");

// Other request errors
create_exception!(httpr, UnsupportedProtocol, TransportError, "Attempted to make a request to an unsupported protocol.");
create_exception!(httpr, ProxyError, TransportError, "An error occurred while establishing a proxy connection.");
create_exception!(httpr, TooManyRedirects, RequestError, "Too many redirects.");
create_exception!(httpr, HTTPStatusError, HTTPError, "The response had an error HTTP status of 4xx or 5xx.");
create_exception!(httpr, DecodingError, RequestError, "Decoding of the response failed, due to a malformed encoding.");

// Stream exceptions
create_exception!(httpr, StreamConsumed, StreamError, "Attempted to read or stream content, but the content has already been consumed.");
create_exception!(httpr, ResponseNotRead, StreamError, "Attempted to access streaming response content, without having called `read()`.");
create_exception!(httpr, RequestNotRead, StreamError, "Attempted to access streaming request content, without having called `read()`.");
create_exception!(httpr, StreamClosed, StreamError, "Attempted to read or stream response content, but the request has been closed.");

// Other exceptions
create_exception!(httpr, InvalidURL, PyException, "URL is improperly formed or cannot be parsed.");
create_exception!(httpr, CookieConflict, PyException, "Attempted to lookup a cookie by name, but multiple cookies existed.");

/// Helper function to convert reqwest errors to appropriate httpr exceptions
pub fn map_reqwest_error(err: reqwest::Error) -> PyErr {
    // Check timeout first
    if err.is_timeout() {
        // Try to determine if it's connect, read, or write timeout
        let err_str = err.to_string().to_lowercase();
        if err_str.contains("connect") {
            return ConnectTimeout::new_err(err.to_string());
        } else if err_str.contains("read") || err_str.contains("recv") {
            return ReadTimeout::new_err(err.to_string());
        } else if err_str.contains("write") || err_str.contains("send") {
            return WriteTimeout::new_err(err.to_string());
        }
        // Default to read timeout for generic timeouts
        return ReadTimeout::new_err(err.to_string());
    }
    
    // Check for connection errors
    if err.is_connect() {
        return ConnectError::new_err(err.to_string());
    }
    
    // Check for redirect errors
    if err.is_redirect() {
        return TooManyRedirects::new_err(err.to_string());
    }
    
    // Check for decode errors
    if err.is_decode() {
        return DecodingError::new_err(err.to_string());
    }
    
    // Check for request errors (builder errors, body errors)
    if err.is_request() || err.is_body() {
        return RequestError::new_err(err.to_string());
    }
    
    // Check for status errors (4xx, 5xx)
    if err.is_status() {
        return HTTPStatusError::new_err(err.to_string());
    }
    
    // Default to generic RequestError for unknown errors
    RequestError::new_err(err.to_string())
}

/// Helper function to convert anyhow errors to appropriate httpr exceptions
pub fn map_anyhow_error(err: anyhow::Error) -> PyErr {
    // First, try to downcast to reqwest::Error if possible
    if let Some(reqwest_err) = err.downcast_ref::<reqwest::Error>() {
        return map_reqwest_error_ref(reqwest_err);
    }
    
    let err_str = err.to_string().to_lowercase();
    
    // Check for URL-related errors
    if err_str.contains("url") || err_str.contains("uri") {
        return InvalidURL::new_err(err.to_string());
    }
    
    // Check for timeout errors
    if err_str.contains("timeout") || err_str.contains("timed out") || err_str.contains("operation timed out") {
        if err_str.contains("connect") {
            return ConnectTimeout::new_err(err.to_string());
        } else if err_str.contains("read") || err_str.contains("recv") {
            return ReadTimeout::new_err(err.to_string());
        } else if err_str.contains("write") || err_str.contains("send") {
            return WriteTimeout::new_err(err.to_string());
        }
        return ReadTimeout::new_err(err.to_string());
    }
    
    // Check for connection errors
    if err_str.contains("connect") || err_str.contains("connection") || err_str.contains("dns error") {
        return ConnectError::new_err(err.to_string());
    }
    
    // Check for file/IO errors
    if err_str.contains("no such file") || err_str.contains("not found") {
        return RequestError::new_err(err.to_string());
    }
    
    // Check for proxy errors
    if err_str.contains("proxy") {
        return ProxyError::new_err(err.to_string());
    }
    
    // Check for SSL/TLS errors
    if err_str.contains("ssl") || err_str.contains("tls") || err_str.contains("certificate") {
        return ConnectError::new_err(err.to_string());
    }
    
    // Default to generic RequestError
    RequestError::new_err(err.to_string())
}

/// Helper function to convert reqwest error references to appropriate httpr exceptions
fn map_reqwest_error_ref(err: &reqwest::Error) -> PyErr {
    // Check timeout first
    if err.is_timeout() {
        // Try to determine if it's connect, read, or write timeout
        let err_str = err.to_string().to_lowercase();
        if err_str.contains("connect") {
            return ConnectTimeout::new_err(err.to_string());
        } else if err_str.contains("read") || err_str.contains("recv") {
            return ReadTimeout::new_err(err.to_string());
        } else if err_str.contains("write") || err_str.contains("send") {
            return WriteTimeout::new_err(err.to_string());
        }
        // Default to read timeout for generic timeouts
        return ReadTimeout::new_err(err.to_string());
    }
    
    // Check for connection errors
    if err.is_connect() {
        return ConnectError::new_err(err.to_string());
    }
    
    // Check for redirect errors
    if err.is_redirect() {
        return TooManyRedirects::new_err(err.to_string());
    }
    
    // Check for decode errors
    if err.is_decode() {
        return DecodingError::new_err(err.to_string());
    }
    
    // Check for request errors (builder errors, body errors)
    if err.is_request() || err.is_body() {
        return RequestError::new_err(err.to_string());
    }
    
    // Check for status errors (4xx, 5xx)
    if err.is_status() {
        return HTTPStatusError::new_err(err.to_string());
    }
    
    // Default to generic RequestError for unknown errors
    RequestError::new_err(err.to_string())
}

/// Register all exception types with the Python module
pub fn register_exceptions(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Base exceptions
    m.add("HTTPError", m.py().get_type::<HTTPError>())?;
    m.add("RequestError", m.py().get_type::<RequestError>())?;
    m.add("TransportError", m.py().get_type::<TransportError>())?;
    m.add("NetworkError", m.py().get_type::<NetworkError>())?;
    m.add("TimeoutException", m.py().get_type::<TimeoutException>())?;
    m.add("ProtocolError", m.py().get_type::<ProtocolError>())?;
    m.add("StreamError", m.py().get_type::<StreamError>())?;
    
    // Timeout exceptions
    m.add("ConnectTimeout", m.py().get_type::<ConnectTimeout>())?;
    m.add("ReadTimeout", m.py().get_type::<ReadTimeout>())?;
    m.add("WriteTimeout", m.py().get_type::<WriteTimeout>())?;
    m.add("PoolTimeout", m.py().get_type::<PoolTimeout>())?;
    
    // Network exceptions
    m.add("ConnectError", m.py().get_type::<ConnectError>())?;
    m.add("ReadError", m.py().get_type::<ReadError>())?;
    m.add("WriteError", m.py().get_type::<WriteError>())?;
    m.add("CloseError", m.py().get_type::<CloseError>())?;
    
    // Protocol exceptions
    m.add("LocalProtocolError", m.py().get_type::<LocalProtocolError>())?;
    m.add("RemoteProtocolError", m.py().get_type::<RemoteProtocolError>())?;
    
    // Other transport/request exceptions
    m.add("UnsupportedProtocol", m.py().get_type::<UnsupportedProtocol>())?;
    m.add("ProxyError", m.py().get_type::<ProxyError>())?;
    m.add("TooManyRedirects", m.py().get_type::<TooManyRedirects>())?;
    m.add("HTTPStatusError", m.py().get_type::<HTTPStatusError>())?;
    m.add("DecodingError", m.py().get_type::<DecodingError>())?;
    
    // Stream exceptions
    m.add("StreamConsumed", m.py().get_type::<StreamConsumed>())?;
    m.add("ResponseNotRead", m.py().get_type::<ResponseNotRead>())?;
    m.add("RequestNotRead", m.py().get_type::<RequestNotRead>())?;
    m.add("StreamClosed", m.py().get_type::<StreamClosed>())?;
    
    // Other exceptions
    m.add("InvalidURL", m.py().get_type::<InvalidURL>())?;
    m.add("CookieConflict", m.py().get_type::<CookieConflict>())?;
    
    Ok(())
}
