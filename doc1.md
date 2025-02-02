Title: Developer Interface - HTTPX

URL Source: https://www.python-httpx.org/api/

Markdown Content:
Helper Functions
----------------

Note

Only use these functions if you're testing HTTPX in a console or making a small number of requests. Using a `Client` will enable HTTP/2 and connection pooling for more efficient and long-lived connections.

`httpx.**request**`(_method_, _url_, _\*_, _params=None_, _content=None_, _data=None_, _files=None_, _json=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _timeout=Timeout(timeout=5.0)_, _follow\_redirects=False_, _verify=True_, _trust\_env=True_)

Sends an HTTP request.

**Parameters:**

*   **method** - HTTP method for the new `Request` object: `GET`, `OPTIONS`, `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
*   **url** - URL for the new `Request` object.
*   **params** - _(optional)_ Query parameters to include in the URL, as a string, dictionary, or sequence of two-tuples.
*   **content** - _(optional)_ Binary content to include in the body of the request, as bytes or a byte iterator.
*   **data** - _(optional)_ Form data to include in the body of the request, as a dictionary.
*   **files** - _(optional)_ A dictionary of upload files to include in the body of the request.
*   **json** - _(optional)_ A JSON serializable object to include in the body of the request.
*   **headers** - _(optional)_ Dictionary of HTTP headers to include in the request.
*   **cookies** - _(optional)_ Dictionary of Cookie items to include in the request.
*   **auth** - _(optional)_ An authentication class to use when sending the request.
*   **proxy** - _(optional)_ A proxy URL where all the traffic should be routed.
*   **timeout** - _(optional)_ The timeout configuration to use when sending the request.
*   **follow\_redirects** - _(optional)_ Enables or disables HTTP redirects.
*   **verify** - _(optional)_ Either `True` to use an SSL context with the default CA bundle, `False` to disable verification, or an instance of `ssl.SSLContext` to use a custom context.
*   **trust\_env** - _(optional)_ Enables or disables usage of environment variables for configuration.

**Returns:** `Response`

Usage:

```
>>>importhttpx
>>>response=httpx.request('GET','https://httpbin.org/get')
>>>response
<Response[200OK]>
```

`httpx.**get**`(_url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends a `GET` request.

**Parameters**: See `httpx.request`.

Note that the `data`, `files`, `json` and `content` parameters are not available on this function, as `GET` requests should not include a request body.

`httpx.**options**`(_url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends an `OPTIONS` request.

**Parameters**: See `httpx.request`.

Note that the `data`, `files`, `json` and `content` parameters are not available on this function, as `OPTIONS` requests should not include a request body.

`httpx.**head**`(_url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends a `HEAD` request.

**Parameters**: See `httpx.request`.

Note that the `data`, `files`, `json` and `content` parameters are not available on this function, as `HEAD` requests should not include a request body.

`httpx.**post**`(_url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends a `POST` request.

**Parameters**: See `httpx.request`.

`httpx.**put**`(_url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends a `PUT` request.

**Parameters**: See `httpx.request`.

`httpx.**patch**`(_url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _verify=True_, _timeout=Timeout(timeout=5.0)_, _trust\_env=True_)

Sends a `PATCH` request.

**Parameters**: See `httpx.request`.

`httpx.**delete**`(_url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _follow\_redirects=False_, _timeout=Timeout(timeout=5.0)_, _verify=True_, _trust\_env=True_)

Sends a `DELETE` request.

**Parameters**: See `httpx.request`.

Note that the `data`, `files`, `json` and `content` parameters are not available on this function, as `DELETE` requests should not include a request body.

`httpx.**stream**`(_method_, _url_, _\*_, _params=None_, _content=None_, _data=None_, _files=None_, _json=None_, _headers=None_, _cookies=None_, _auth=None_, _proxy=None_, _timeout=Timeout(timeout=5.0)_, _follow\_redirects=False_, _verify=True_, _trust\_env=True_)

Alternative to `httpx.request()` that streams the response body instead of loading it into memory at once.

**Parameters**: See `httpx.request`.

See also: [Streaming Responses](https://www.python-httpx.org/quickstart#streaming-responses)

`Client`
--------

_class_ `httpx.**Client**`(_\*_, _auth=None_, _params=None_, _headers=None_, _cookies=None_, _verify=True_, _cert=None_, _trust\_env=True_, _http1=True_, _http2=False_, _proxy=None_, _mounts=None_, _timeout=Timeout(timeout=5.0)_, _follow\_redirects=False_, _limits=Limits(max\_connections=100, max\_keepalive\_connections=20, keepalive\_expiry=5.0)_, _max\_redirects=20_, _event\_hooks=None_, _base\_url=''_, _transport=None_, _default\_encoding='utf-8'_)

An HTTP client, with connection pooling, HTTP/2, redirects, cookie persistence, etc.

It can be shared between threads.

Usage:

```
>>> client = httpx.Client()
>>> response = client.get('https://example.org')
```

**Parameters:**

*   **auth** - _(optional)_ An authentication class to use when sending requests.
*   **params** - _(optional)_ Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.
*   **headers** - _(optional)_ Dictionary of HTTP headers to include when sending requests.
*   **cookies** - _(optional)_ Dictionary of Cookie items to include when sending requests.
*   **verify** - _(optional)_ Either `True` to use an SSL context with the default CA bundle, `False` to disable verification, or an instance of `ssl.SSLContext` to use a custom context.
*   **http2** - _(optional)_ A boolean indicating if HTTP/2 support should be enabled. Defaults to `False`.
*   **proxy** - _(optional)_ A proxy URL where all the traffic should be routed.
*   **timeout** - _(optional)_ The timeout configuration to use when sending requests.
*   **limits** - _(optional)_ The limits configuration to use.
*   **max\_redirects** - _(optional)_ The maximum number of redirect responses that should be followed.
*   **base\_url** - _(optional)_ A URL to use as the base when building request URLs.
*   **transport** - _(optional)_ A transport class to use for sending requests over the network.
*   **trust\_env** - _(optional)_ Enables or disables usage of environment variables for configuration.
*   **default\_encoding** - _(optional)_ The default encoding to use for decoding response text, if no charset information is included in a response Content-Type header. Set to a callable for automatic character set detection. Default: "utf-8".

`**headers**`

HTTP headers to include when sending requests.

`**cookies**`

Cookie values to include when sending requests.

`**params**`

Query parameters to include in the URL when sending requests.

`**auth**`

Authentication class used when none is passed at the request-level.

See also [Authentication](https://www.python-httpx.org/quickstart/#authentication).

`**request**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Build and send a request.

Equivalent to:

```
request = client.build_request(...)
response = client.send(request, ...)
```

See `Client.build_request()`, `Client.send()` and [Merging of configuration](https://www.python-httpx.org/advanced/clients/#merging-of-configuration) for how the various parameters are merged with client-level configuration.

`**get**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `GET` request.

**Parameters**: See `httpx.request`.

`**head**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `HEAD` request.

**Parameters**: See `httpx.request`.

`**options**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send an `OPTIONS` request.

**Parameters**: See `httpx.request`.

`**post**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `POST` request.

**Parameters**: See `httpx.request`.

`**put**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `PUT` request.

**Parameters**: See `httpx.request`.

`**patch**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `PATCH` request.

**Parameters**: See `httpx.request`.

`**delete**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `DELETE` request.

**Parameters**: See `httpx.request`.

`**stream**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Alternative to `httpx.request()` that streams the response body instead of loading it into memory at once.

**Parameters**: See `httpx.request`.

See also: [Streaming Responses](https://www.python-httpx.org/quickstart#streaming-responses)

`**build_request**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _timeout=_, _extensions=None_)

Build and return a request instance.

*   The `params`, `headers` and `cookies` arguments are merged with any values set on the client.
*   The `url` argument is merged with any `base_url` set on the client.

See also: [Request instances](https://www.python-httpx.org/advanced/clients/#request-instances)

`**send**`(_self_, _request_, _\*_, _stream=False_, _auth=_, _follow\_redirects=_)

Send a request.

The request is sent as-is, unmodified.

Typically you'll want to build one with `Client.build_request()` so that any client-level configuration is merged into the request, but passing an explicit `httpx.Request()` is supported as well.

See also: [Request instances](https://www.python-httpx.org/advanced/clients/#request-instances)

`**close**`(_self_)

Close transport and proxies.

`AsyncClient`
-------------

_class_ `httpx.**AsyncClient**`(_\*_, _auth=None_, _params=None_, _headers=None_, _cookies=None_, _verify=True_, _cert=None_, _http1=True_, _http2=False_, _proxy=None_, _mounts=None_, _timeout=Timeout(timeout=5.0)_, _follow\_redirects=False_, _limits=Limits(max\_connections=100, max\_keepalive\_connections=20, keepalive\_expiry=5.0)_, _max\_redirects=20_, _event\_hooks=None_, _base\_url=''_, _transport=None_, _trust\_env=True_, _default\_encoding='utf-8'_)

An asynchronous HTTP client, with connection pooling, HTTP/2, redirects, cookie persistence, etc.

It can be shared between tasks.

Usage:

```
>>> async with httpx.AsyncClient() as client:
>>>     response = await client.get('https://example.org')
```

**Parameters:**

*   **auth** - _(optional)_ An authentication class to use when sending requests.
*   **params** - _(optional)_ Query parameters to include in request URLs, as a string, dictionary, or sequence of two-tuples.
*   **headers** - _(optional)_ Dictionary of HTTP headers to include when sending requests.
*   **cookies** - _(optional)_ Dictionary of Cookie items to include when sending requests.
*   **verify** - _(optional)_ Either `True` to use an SSL context with the default CA bundle, `False` to disable verification, or an instance of `ssl.SSLContext` to use a custom context.
*   **http2** - _(optional)_ A boolean indicating if HTTP/2 support should be enabled. Defaults to `False`.
*   **proxy** - _(optional)_ A proxy URL where all the traffic should be routed.
*   **timeout** - _(optional)_ The timeout configuration to use when sending requests.
*   **limits** - _(optional)_ The limits configuration to use.
*   **max\_redirects** - _(optional)_ The maximum number of redirect responses that should be followed.
*   **base\_url** - _(optional)_ A URL to use as the base when building request URLs.
*   **transport** - _(optional)_ A transport class to use for sending requests over the network.
*   **trust\_env** - _(optional)_ Enables or disables usage of environment variables for configuration.
*   **default\_encoding** - _(optional)_ The default encoding to use for decoding response text, if no charset information is included in a response Content-Type header. Set to a callable for automatic character set detection. Default: "utf-8".

`**headers**`

HTTP headers to include when sending requests.

`**cookies**`

Cookie values to include when sending requests.

`**params**`

Query parameters to include in the URL when sending requests.

`**auth**`

Authentication class used when none is passed at the request-level.

See also [Authentication](https://www.python-httpx.org/quickstart/#authentication).

_async_ `**request**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Build and send a request.

Equivalent to:

```
request = client.build_request(...)
response = await client.send(request, ...)
```

See `AsyncClient.build_request()`, `AsyncClient.send()` and [Merging of configuration](https://www.python-httpx.org/advanced/clients/#merging-of-configuration) for how the various parameters are merged with client-level configuration.

_async_ `**get**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `GET` request.

**Parameters**: See `httpx.request`.

_async_ `**head**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `HEAD` request.

**Parameters**: See `httpx.request`.

_async_ `**options**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send an `OPTIONS` request.

**Parameters**: See `httpx.request`.

_async_ `**post**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `POST` request.

**Parameters**: See `httpx.request`.

_async_ `**put**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `PUT` request.

**Parameters**: See `httpx.request`.

_async_ `**patch**`(_self_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `PATCH` request.

**Parameters**: See `httpx.request`.

_async_ `**delete**`(_self_, _url_, _\*_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Send a `DELETE` request.

**Parameters**: See `httpx.request`.

`**stream**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _auth=_, _follow\_redirects=_, _timeout=_, _extensions=None_)

Alternative to `httpx.request()` that streams the response body instead of loading it into memory at once.

**Parameters**: See `httpx.request`.

See also: [Streaming Responses](https://www.python-httpx.org/quickstart#streaming-responses)

`**build_request**`(_self_, _method_, _url_, _\*_, _content=None_, _data=None_, _files=None_, _json=None_, _params=None_, _headers=None_, _cookies=None_, _timeout=_, _extensions=None_)

Build and return a request instance.

*   The `params`, `headers` and `cookies` arguments are merged with any values set on the client.
*   The `url` argument is merged with any `base_url` set on the client.

See also: [Request instances](https://www.python-httpx.org/advanced/clients/#request-instances)

_async_ `**send**`(_self_, _request_, _\*_, _stream=False_, _auth=_, _follow\_redirects=_)

Send a request.

The request is sent as-is, unmodified.

Typically you'll want to build one with `AsyncClient.build_request()` so that any client-level configuration is merged into the request, but passing an explicit `httpx.Request()` is supported as well.

See also: [Request instances](https://www.python-httpx.org/advanced/clients/#request-instances)

_async_ `**aclose**`(_self_)

Close transport and proxies.

`Response`
----------

_An HTTP response._

*   `def __init__(...)`
*   `.status_code` - **int**
*   `.reason_phrase` - **str**
*   `.http_version` - `"HTTP/2"` or `"HTTP/1.1"`
*   `.url` - **URL**
*   `.headers` - **Headers**
*   `.content` - **bytes**
*   `.text` - **str**
*   `.encoding` - **str**
*   `.is_redirect` - **bool**
*   `.request` - **Request**
*   `.next_request` - **Optional\[Request\]**
*   `.cookies` - **Cookies**
*   `.history` - **List\[Response\]**
*   `.elapsed` - **[timedelta](https://docs.python.org/3/library/datetime.html)**
*   The amount of time elapsed between sending the request and calling `close()` on the corresponding response received for that request. [total\_seconds()](https://docs.python.org/3/library/datetime.html#datetime.timedelta.total_seconds) to correctly get the total elapsed seconds.
*   `def .raise_for_status()` - **Response**
*   `def .json()` - **Any**
*   `def .read()` - **bytes**
*   `def .iter_raw([chunk_size])` - **bytes iterator**
*   `def .iter_bytes([chunk_size])` - **bytes iterator**
*   `def .iter_text([chunk_size])` - **text iterator**
*   `def .iter_lines()` - **text iterator**
*   `def .close()` - **None**
*   `def .next()` - **Response**
*   `def .aread()` - **bytes**
*   `def .aiter_raw([chunk_size])` - **async bytes iterator**
*   `def .aiter_bytes([chunk_size])` - **async bytes iterator**
*   `def .aiter_text([chunk_size])` - **async text iterator**
*   `def .aiter_lines()` - **async text iterator**
*   `def .aclose()` - **None**
*   `def .anext()` - **Response**

`Request`
---------

_An HTTP request. Can be constructed explicitly for more control over exactly what gets sent over the wire._

```
>>> request = httpx.Request("GET", "https://example.org", headers={'host': 'example.org'})
>>> response = client.send(request)
```

*   `def __init__(method, url, [params], [headers], [cookies], [content], [data], [files], [json], [stream])`
*   `.method` - **str**
*   `.url` - **URL**
*   `.content` - **byte**, **byte iterator**, or **byte async iterator**
*   `.headers` - **Headers**
*   `.cookies` - **Cookies**

`URL`
-----

_A normalized, IDNA supporting URL._

```
>>> url = URL("https://example.org/")
>>> url.host
'example.org'
```

*   `def __init__(url, **kwargs)`
*   `.scheme` - **str**
*   `.authority` - **str**
*   `.host` - **str**
*   `.port` - **int**
*   `.path` - **str**
*   `.query` - **str**
*   `.raw_path` - **str**
*   `.fragment` - **str**
*   `.is_ssl` - **bool**
*   `.is_absolute_url` - **bool**
*   `.is_relative_url` - **bool**
*   `def .copy_with([scheme], [authority], [path], [query], [fragment])` - **URL**

_A case-insensitive multi-dict._

```
>>> headers = Headers({'Content-Type': 'application/json'})
>>> headers['content-type']
'application/json'
```

*   `def __init__(self, headers, encoding=None)`
*   `def copy()` - **Headers**

`Cookies`
---------

_A dict-like cookie store._

```
>>> cookies = Cookies()
>>> cookies.set("name", "value", domain="example.org")
```

*   `def __init__(cookies: [dict, Cookies, CookieJar])`
*   `.jar` - **CookieJar**
*   `def extract_cookies(response)`
*   `def set_cookie_header(request)`
*   `def set(name, value, [domain], [path])`
*   `def get(name, [domain], [path])`
*   `def delete(name, [domain], [path])`
*   `def clear([domain], [path])`
*   _Standard mutable mapping interface_
