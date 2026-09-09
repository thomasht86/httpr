# AsyncClient

The asynchronous HTTP client for use with asyncio.

::: httpr.AsyncClient
    options:
      members:
        - __init__
        - request
        - get
        - head
        - options
        - delete
        - post
        - put
        - patch
        - stream
        - aclose
      show_root_heading: true
      show_root_full_path: false
      heading_level: 2

::: httpr.AsyncStreamingResponse
    options:
      members:
        - aiter_bytes
        - aiter_text
        - aiter_lines
        - aread
        - aclose
        - raise_for_status
      show_root_heading: true
      show_root_full_path: false
      heading_level: 2
