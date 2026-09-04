"""Regression tests for ca_cert_file scoping (GitHub issue #86).

``ca_cert_file`` used to be implemented by writing ``HTTPR_CA_BUNDLE`` into the
process-wide environment. The value outlived the client that set it, leaked into
child processes, and silently changed which CA roots every later client trusted.
These tests pin the corrected behaviour: the argument is scoped to one client,
the environment variable is honoured as a *default* only, and it is never written.
"""

import os
import subprocess
import sys

import pytest

import httpr


@pytest.fixture(autouse=True)
def _clean_ca_bundle_env(monkeypatch):
    """Start every test without HTTPR_CA_BUNDLE in the real process environment."""
    monkeypatch.delenv("HTTPR_CA_BUNDLE", raising=False)


def _child_env_value() -> str:
    """Return the HTTPR_CA_BUNDLE value seen by a fresh child process.

    ``os.environ`` in *this* process is a snapshot taken at import time, so it
    would not reflect a ``setenv`` done from Rust. A child process inherits the
    real process environment and is therefore the reliable observer.
    """
    out = subprocess.run(
        [sys.executable, "-c", "import os; print(repr(os.environ.get('HTTPR_CA_BUNDLE')))"],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def test_ca_cert_file_does_not_mutate_process_environment(ca_bundle):
    httpr.Client(ca_cert_file=ca_bundle)
    assert _child_env_value() == "None"


def test_failed_ca_cert_file_does_not_mutate_process_environment():
    with pytest.raises(httpr.RequestError):
        httpr.Client(ca_cert_file="/nonexistent/ca.pem")
    assert _child_env_value() == "None"


def test_invalid_ca_cert_file_does_not_break_later_clients():
    """A bad bundle on client A must not make an unconfigured client B fail."""
    with pytest.raises(httpr.RequestError):
        httpr.Client(ca_cert_file="/nonexistent/ca.pem")
    # Before the fix this raised "Failed to read CA certificates from /nonexistent/ca.pem".
    httpr.Client()


def test_valid_ca_cert_file_does_not_extend_trust_of_later_clients(base_url_ssl, ca_bundle):
    """Client A trusting a private CA must not make client B trust it too."""
    trusting = httpr.Client(ca_cert_file=ca_bundle)
    assert trusting.get(f"{base_url_ssl}/get").status_code == 200

    unconfigured = httpr.Client()
    with pytest.raises(httpr.ConnectError):
        unconfigured.get(f"{base_url_ssl}/get")


def test_env_var_is_still_honoured_as_default(monkeypatch, base_url_ssl, ca_bundle):
    monkeypatch.setenv("HTTPR_CA_BUNDLE", ca_bundle)
    assert httpr.Client().get(f"{base_url_ssl}/get").status_code == 200


def test_ca_cert_file_takes_precedence_over_env_var(monkeypatch, base_url_ssl, ca_bundle):
    monkeypatch.setenv("HTTPR_CA_BUNDLE", "/nonexistent/from-env.pem")
    client = httpr.Client(ca_cert_file=ca_bundle)
    assert client.get(f"{base_url_ssl}/get").status_code == 200
    # The explicit argument must not have been written back over the env var.
    assert os.environ["HTTPR_CA_BUNDLE"] == "/nonexistent/from-env.pem"
    assert _child_env_value() == "'/nonexistent/from-env.pem'"
