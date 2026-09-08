//! Client lifecycle (issue #88): what it takes for `close()` to actually
//! release a connection pool.
//!
//! Dropping a `reqwest::Client` drops its pool, but that alone does not close
//! any socket. Every pooled connection lives in a task on the single-threaded
//! `RUNTIME`, and those tasks only run inside `block_on`, so the hang-up a
//! dropped pool hands them sits unobserved until something drives the runtime.
//! [`settle_dropped_pool`] does that driving: a handful of scheduler turns, all
//! deterministic and microseconds long.
//!
//! The one thing turns alone cannot finish is a connect that is still pending.
//! When requests overlap, hyper races a fresh connect against the idle-pool
//! checkout and, if the checkout wins, keeps the connect running in the
//! background so the socket is not wasted. That future owns a strong handle to
//! the pool and needs real I/O (a SYN-ACK, a TLS handshake) to resolve, which
//! against a remote host can take longer than any wait `close()` could
//! reasonably impose. Instead of waiting, the pool's connector is wrapped in
//! [`CancelConnectsLayer`], and `close()` cancels every pending connect the
//! moment nothing else is using the client. Cancelled connects resolve on the
//! next scheduler turn, drop their pool handle, and the pool goes away.
//!
//! [`ClientState`] ties this together and is shared, via `Arc`, between an
//! `RClient` and the requests it has in flight. In-flight requests hold their
//! own `reqwest::Client` clone and finish normally when the client is closed
//! underneath them; the last one to finish is the one that really drops the
//! pool, so it performs the release.
//!
//! A client that never started a request has nothing to release: its pool
//! holds no connection and its connector has no connect pending, so closing
//! or dropping it skips the whole procedure.

use std::fmt;
use std::future::Future;
use std::pin::Pin;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex, MutexGuard};
use std::task::{Context, Poll};

use tokio_util::sync::CancellationToken;
use tower::{Layer, Service};

use crate::RUNTIME;

type BoxError = Box<dyn std::error::Error + Send + Sync>;

/// Scheduler turns given to the runtime after a pool is dropped. A cancelled
/// connect, the pool handle it releases, and the connection tasks that then
/// shut their sockets down form a short wake-up chain; each turn advances
/// every task that is ready, and the tokio I/O driver is polled between turns.
///
/// Every wake in that chain happens on this thread and lands in the run queue,
/// so the first turn already drains the whole chain; a plain `shutdown()` on a
/// TCP socket needs no I/O readiness. The remaining turns are margin for a
/// shutdown that does (a TLS close_notify or HTTP/2 GOAWAY that hits a full
/// send buffer). Keep this small: each turn costs a driver poll, which is a
/// syscall (~13 µs on macOS), and this runs on every `close()`, `__exit__` and
/// drop of a client that has sent at least one request. 32 turns made a
/// create-request-close cycle twice as slow.
const SETTLE_SCHEDULER_TURNS: usize = 4;

/// Drive `RUNTIME` so a just-dropped connection pool actually releases its
/// sockets. Call with the GIL released where possible; it never blocks on I/O.
///
/// If another thread currently holds the runtime's scheduler core (it is
/// inside `block_on` for a request), this completes without driving any
/// task, and that thread's scheduler closes the sockets instead.
pub fn settle_dropped_pool() {
    RUNTIME.block_on(async {
        for _ in 0..SETTLE_SCHEDULER_TURNS {
            tokio::task::yield_now().await;
        }
    })
}

/// Everything an `RClient` and its in-flight requests share about the pool.
pub struct ClientState {
    /// `None` once `close()` has been called. Dropping the `reqwest::Client`
    /// drops the client's own handle to its pool.
    client: Mutex<Option<reqwest::Client>>,
    /// Requests currently running: inside `request()`, or a `StreamingResponse`
    /// that has not been closed yet.
    in_flight: AtomicUsize,
    /// Whether any request was ever started. Until then the pool cannot hold a
    /// connection or a pending connect, so there is nothing to release.
    used: AtomicBool,
    /// Cancels every connect still pending in the pool's connector.
    connects: CancellationToken,
}

impl ClientState {
    /// Wrap a freshly built client. `connects` must be the token its
    /// [`CancelConnectsLayer`] was created from.
    pub fn new(client: reqwest::Client, connects: CancellationToken) -> Arc<Self> {
        Arc::new(ClientState {
            client: Mutex::new(Some(client)),
            in_flight: AtomicUsize::new(0),
            used: AtomicBool::new(false),
            connects,
        })
    }

    /// The layer to install on any `reqwest::ClientBuilder` whose client will
    /// live in this state, so `close()` can cancel its pending connects.
    pub fn connector_layer(&self) -> CancelConnectsLayer {
        CancelConnectsLayer(self.connects.clone())
    }

    /// The slot holding the client. A poisoned lock is recovered rather than
    /// reported: the only operations on it are `take`, `clone` and `replace`,
    /// none of which can leave the `Option` half-updated.
    fn slot(&self) -> MutexGuard<'_, Option<reqwest::Client>> {
        self.client.lock().unwrap_or_else(|e| e.into_inner())
    }

    /// Whether `close()` has been called.
    pub fn is_closed(&self) -> bool {
        self.slot().is_none()
    }

    /// Start a request: a handle to the underlying `reqwest::Client` plus the
    /// guard that counts the request as in flight, or `None` if the client is
    /// closed. Cloning the client is cheap (an `Arc` inside), and taking the
    /// clone up front is what lets a request survive a `close()` from another
    /// thread.
    pub fn begin_request(self: &Arc<Self>) -> Option<(reqwest::Client, InFlight)> {
        // Count first, then look: `close()` looks at the count only after it
        // has emptied the slot, so either it sees this request and leaves the
        // release to the guard, or this request finds the slot empty.
        self.in_flight.fetch_add(1, Ordering::SeqCst);
        self.used.store(true, Ordering::SeqCst);
        let guard = InFlight(Arc::clone(self));
        let client = self.slot().clone()?;
        Some((client, guard))
    }

    /// Swap in a rebuilt client (proxy change). The old pool is dropped and its
    /// idle connections released. Returns `false`, leaving `new` unused, if the
    /// client is closed.
    pub fn replace(&self, new: reqwest::Client) -> bool {
        let old = {
            let mut slot = self.slot();
            if slot.is_none() {
                return false;
            }
            slot.replace(new)
        };
        drop(old);
        if self.used.load(Ordering::SeqCst) {
            settle_dropped_pool();
        }
        true
    }

    /// Close the client. Returns `false` if it was already closed.
    pub fn close(&self) -> bool {
        let Some(client) = self.slot().take() else {
            return false;
        };
        drop(client);
        self.release_pool();
        true
    }

    /// The client's handle to the pool is gone; make sure the pool is too.
    fn release_pool(&self) {
        if !self.used.load(Ordering::SeqCst) {
            // No request ever ran: the pool has no connection and the connector
            // has nothing pending, so dropping the handle was the whole release.
            return;
        }
        if self.in_flight.load(Ordering::SeqCst) == 0 {
            // Nothing legitimate can still be connecting, so whatever the
            // connector has pending is a background connect holding the pool
            // alive. With requests in flight this is skipped: their connects
            // must not be interrupted, and the last of them to finish will
            // cancel instead (see `InFlight`).
            self.connects.cancel();
        }
        settle_dropped_pool();
    }
}

/// Counts a request as in flight for as long as it exists.
///
/// Dropping the last guard after the client was closed is the moment the pool
/// is really gone, so the drop performs the release `close()` had to skip.
pub struct InFlight(Arc<ClientState>);

impl Drop for InFlight {
    fn drop(&mut self) {
        let was_last = self.0.in_flight.fetch_sub(1, Ordering::SeqCst) == 1;
        if was_last && self.0.is_closed() {
            self.0.release_pool();
        }
    }
}

/// Tower layer that makes a connector's pending connects cancellable.
#[derive(Clone)]
pub struct CancelConnectsLayer(CancellationToken);

impl CancelConnectsLayer {
    /// `token` is what the owning [`ClientState`] cancels on close.
    pub fn new(token: CancellationToken) -> Self {
        CancelConnectsLayer(token)
    }
}

impl<S> Layer<S> for CancelConnectsLayer {
    type Service = CancelConnects<S>;

    fn layer(&self, inner: S) -> Self::Service {
        CancelConnects {
            inner,
            token: self.0.clone(),
        }
    }
}

/// Connector wrapper produced by [`CancelConnectsLayer`].
#[derive(Clone)]
pub struct CancelConnects<S> {
    inner: S,
    token: CancellationToken,
}

impl<S, Req> Service<Req> for CancelConnects<S>
where
    S: Service<Req, Error = BoxError>,
    S::Future: Send + 'static,
{
    type Response = S::Response;
    type Error = BoxError;
    type Future = Pin<Box<dyn Future<Output = Result<S::Response, BoxError>> + Send>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), BoxError>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Req) -> Self::Future {
        let connect = self.inner.call(req);
        let token = self.token.clone();
        Box::pin(async move {
            tokio::select! {
                biased;
                _ = token.cancelled() => Err(Box::new(ConnectCancelled) as BoxError),
                result = connect => result,
            }
        })
    }
}

/// Error a pending connect resolves with when its client is closed.
#[derive(Debug)]
struct ConnectCancelled;

impl fmt::Display for ConnectCancelled {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("connect cancelled: the client has been closed")
    }
}

impl std::error::Error for ConnectCancelled {}
