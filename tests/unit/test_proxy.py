"""Assigning `client.proxy` rebuilds the client but must keep every other setting (issue #84).

`client.proxy = None` is a rebuild without a proxy, so it exercises the same
code path as switching proxies while still letting the request reach httpbin.
"""

import pytest
import trustme

import httpr  # type: ignore


def test_proxy_setter_accepts_none_and_round_trips():
    client = httpr.Client()
    assert client.proxy is None
    client.proxy = "http://127.0.0.1:1"
    assert client.proxy == "http://127.0.0.1:1"
    client.proxy = None
    assert client.proxy is None


def test_proxy_setter_does_not_reread_env(monkeypatch):
    monkeypatch.setenv("HTTPR_PROXY", "http://from-env:8080")
    client = httpr.Client()
    assert client.proxy == "http://from-env:8080"
    client.proxy = None
    assert client.proxy is None


def test_switching_proxy_then_back_restores_direct_requests(base_url_ssl, ca_bundle):
    with httpr.Client(ca_cert_file=ca_bundle) as client:
        assert client.get(f"{base_url_ssl}/get").status_code == 200
        client.proxy = "http://127.0.0.1:1"  # nothing listens here
        with pytest.raises(httpr.RequestError):
            client.get(f"{base_url_ssl}/get")
        client.proxy = None
        assert client.get(f"{base_url_ssl}/get").status_code == 200


def test_verify_false_survives_rebuild(base_url_ssl):
    with httpr.Client(verify=False) as client:
        assert client.get(f"{base_url_ssl}/get").status_code == 200
        client.proxy = None
        assert client.get(f"{base_url_ssl}/get").status_code == 200


def test_verify_true_still_rejects_unknown_ca_after_rebuild(base_url_ssl):
    with httpr.Client() as client:
        client.proxy = None
        with pytest.raises(httpr.ConnectError):
            client.get(f"{base_url_ssl}/get")


def test_ca_bundle_survives_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(ca_cert_file=ca_bundle) as client:
        client.proxy = None
        assert client.get(f"{base_url_ssl}/get").status_code == 200


def test_follow_redirects_false_survives_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(follow_redirects=False, ca_cert_file=ca_bundle) as client:
        client.proxy = None
        response = client.get(f"{base_url_ssl}/redirect-to?url=/get")
        assert response.status_code == 302


def test_max_redirects_survives_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(max_redirects=2, ca_cert_file=ca_bundle) as client:
        client.proxy = None
        with pytest.raises(httpr.TooManyRedirects):
            client.get(f"{base_url_ssl}/redirect/5")
        assert client.get(f"{base_url_ssl}/redirect/2").status_code == 200


def test_https_only_survives_rebuild(base_url, base_url_ssl, ca_bundle):
    with httpr.Client(https_only=True, ca_cert_file=ca_bundle) as client:
        client.proxy = None
        with pytest.raises(httpr.RequestError):
            client.get(f"{base_url}/get")
        assert client.get(f"{base_url_ssl}/get").status_code == 200


def test_timeout_survives_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(timeout=0.5, ca_cert_file=ca_bundle) as client:
        client.proxy = None
        assert client.timeout == 0.5
        with pytest.raises(httpr.TimeoutException):
            client.get(f"{base_url_ssl}/delay/3")


def test_headers_survive_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(headers={"X-Static": "1"}, cookies={"c": "v"}, ca_cert_file=ca_bundle) as client:
        client.headers["X-Added"] = "2"
        client.proxy = None
        sent = client.get(f"{base_url_ssl}/headers").json()["headers"]
        assert sent["X-Static"] == "1"
        assert sent["X-Added"] == "2"
        assert sent["Cookie"] == "c=v"


def test_cookie_store_setting_survives_rebuild(base_url_ssl, ca_bundle):
    with httpr.Client(cookie_store=False, ca_cert_file=ca_bundle) as client:
        client.proxy = None
        client.get(f"{base_url_ssl}/cookies/set?k=v")
        assert client.get(f"{base_url_ssl}/cookies").json()["cookies"] == {}

    with httpr.Client(cookie_store=True, ca_cert_file=ca_bundle) as client:
        client.get(f"{base_url_ssl}/cookies/set?k=v")
        assert client.get(f"{base_url_ssl}/cookies").json()["cookies"] == {"k": "v"}
        client.proxy = None
        # the store belongs to the rebuilt client, so it starts empty
        assert client.get(f"{base_url_ssl}/cookies").json()["cookies"] == {}
        client.get(f"{base_url_ssl}/cookies/set?k=w")
        assert client.get(f"{base_url_ssl}/cookies").json()["cookies"] == {"k": "w"}


def test_client_identity_survives_rebuild(tmp_path):
    ca = trustme.CA()
    cert = ca.issue_cert("client.local")
    pem = cert.private_key_and_cert_chain_pem.bytes()
    pem_path = tmp_path / "client.pem"
    pem_path.write_bytes(pem)

    # Neither rebuild may fail or touch the filesystem again.
    client = httpr.Client(client_pem_data=pem)
    client.proxy = None
    client = httpr.Client(client_pem=str(pem_path))
    pem_path.unlink()
    client.proxy = None
    client.proxy = "http://127.0.0.1:1"


def test_proxy_setter_after_close_raises_client_closed():
    client = httpr.Client()
    client.close()
    with pytest.raises(httpr.ClientClosed):
        client.proxy = None
