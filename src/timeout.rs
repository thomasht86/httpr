//! Request timeouts.
//!
//! A client's `timeout` (default 30 s, `None` disables it; a request may
//! override it) bounds how long httpr waits for the server to make progress,
//! not how long a whole request may take: it applies to the wait for the
//! response headers and then to the wait for each chunk of the body, and it is
//! reset by every chunk that arrives. A stream that keeps delivering data is
//! never cut off by it, which is what `httpx` does and what SSE and long
//! downloads over a default client need (issue #81).
//!
//! The timeout is applied here, around the crate's own await points, instead
//! of through `reqwest::ClientBuilder::timeout`, for two reasons: reqwest's
//! is a total deadline that also kills a live streaming body, and it is baked
//! into the built client, so `client.timeout = ...` could not change it.
//! Everything reads `RClient::timeout` at request time instead.

use std::fmt;
use std::future::Future;
use std::time::Duration;

use bytes::Bytes;
use pyo3::exceptions::PyValueError;
use pyo3::PyResult;

/// Converts a timeout in seconds, as given from Python, into a `Duration`.
/// `None` means no timeout. Negative or NaN values are rejected.
pub fn duration(seconds: Option<f64>) -> PyResult<Option<Duration>> {
    seconds
        .map(|s| {
            Duration::try_from_secs_f64(s).map_err(|_| {
                PyValueError::new_err(format!(
                    "timeout must be a non-negative number of seconds or None, got {s}"
                ))
            })
        })
        .transpose()
}

/// What the client was waiting for when the timeout elapsed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Phase {
    /// Connecting, sending the request and waiting for the response headers.
    Headers,
    /// Waiting for the next chunk of the response body.
    Body,
}

/// The error a timed-out wait resolves to. `map_anyhow_error` turns it into
/// `httpr.ReadTimeout`.
#[derive(Debug)]
pub struct TimedOut {
    pub phase: Phase,
    pub after: Duration,
}

impl fmt::Display for TimedOut {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let waiting_for = match self.phase {
            Phase::Headers => "the response headers",
            Phase::Body => "the next chunk of the response body",
        };
        write!(
            f,
            "timed out after {} s waiting for {waiting_for}",
            self.after.as_secs_f64()
        )
    }
}

impl std::error::Error for TimedOut {}

/// Awaits `fut`, failing with `TimedOut` if it takes longer than `timeout`.
pub async fn with_timeout<T, F>(
    timeout: Option<Duration>,
    phase: Phase,
    fut: F,
) -> anyhow::Result<T>
where
    F: Future<Output = reqwest::Result<T>>,
{
    match timeout {
        None => fut.await.map_err(anyhow::Error::new),
        Some(after) => match tokio::time::timeout(after, fut).await {
            Ok(result) => result.map_err(anyhow::Error::new),
            Err(_) => Err(anyhow::Error::new(TimedOut { phase, after })),
        },
    }
}

/// The next chunk of the body, or `None` at its end; times out if the server
/// sends nothing for `timeout`.
pub async fn next_chunk(
    resp: &mut reqwest::Response,
    timeout: Option<Duration>,
) -> anyhow::Result<Option<Bytes>> {
    with_timeout(timeout, Phase::Body, resp.chunk()).await
}

/// The whole remaining body, read chunk by chunk so that the timeout is
/// per chunk rather than for the whole transfer. Without a timeout this is
/// `Response::bytes()`; with one it costs the same: a single-chunk body is
/// returned as is, several chunks are concatenated once.
pub async fn read_body(
    mut resp: reqwest::Response,
    timeout: Option<Duration>,
) -> anyhow::Result<Bytes> {
    if timeout.is_none() {
        return resp.bytes().await.map_err(anyhow::Error::new);
    }
    let mut chunks: Vec<Bytes> = Vec::new();
    let mut total = 0;
    while let Some(chunk) = next_chunk(&mut resp, timeout).await? {
        total += chunk.len();
        chunks.push(chunk);
    }
    Ok(match chunks.len() {
        0 => Bytes::new(),
        1 => chunks.pop().unwrap_or_default(),
        _ => {
            let mut buf = Vec::with_capacity(total);
            for chunk in &chunks {
                buf.extend_from_slice(chunk);
            }
            Bytes::from(buf)
        }
    })
}
