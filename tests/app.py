from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.requests import Request

async def homepage(request: Request):
    return PlainTextResponse("Hello, world!")

app = Starlette(routes=[Route("/", homepage)])
