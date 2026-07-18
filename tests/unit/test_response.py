import pytest

import httpr


def test_response_status_api(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle, follow_redirects=False)
    response = client.get(f"{base_url_ssl}/status/200")

    assert response.reason_phrase == "OK"
    assert response.is_success
    assert not response.is_informational
    assert not response.is_redirect
    assert not response.is_client_error
    assert not response.is_server_error
    assert not response.is_error
    assert not response.has_redirect_location
    assert response.raise_for_status() is response
    assert repr(response) == "<Response [200 OK]>"

    for status, attribute in [(404, "is_client_error"), (500, "is_server_error")]:
        response = client.get(f"{base_url_ssl}/status/{status}")
        assert getattr(response, attribute)
        assert response.is_error
        with pytest.raises(httpr.HTTPStatusError, match=str(status)):
            response.raise_for_status()


def test_response_redirect_status(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle, follow_redirects=False)
    response = client.get(f"{base_url_ssl}/redirect/1")

    assert response.is_redirect
    assert response.has_redirect_location
    with pytest.raises(httpr.HTTPStatusError, match="Redirect location"):
        response.raise_for_status()


def test_streaming_response_status_api(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle, follow_redirects=False)

    with client.stream("GET", f"{base_url_ssl}/status/200") as response:
        assert response.reason_phrase == "OK"
        assert response.is_success
        assert not response.is_informational
        assert not response.is_redirect
        assert not response.is_client_error
        assert not response.is_server_error
        assert not response.is_error
        assert not response.has_redirect_location
        assert response.raise_for_status() is response
        assert repr(response) == "<StreamingResponse [200 OK]>"

    for status, attribute in [(404, "is_client_error"), (500, "is_server_error")]:
        with client.stream("GET", f"{base_url_ssl}/status/{status}") as response:
            assert getattr(response, attribute)
            assert response.is_error
            with pytest.raises(httpr.HTTPStatusError, match=str(status)):
                response.raise_for_status()


def test_streaming_response_redirect_status(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle, follow_redirects=False)

    with client.stream("GET", f"{base_url_ssl}/redirect/1") as response:
        assert response.is_redirect
        assert response.has_redirect_location
        with pytest.raises(httpr.HTTPStatusError, match="Redirect location"):
            response.raise_for_status()
