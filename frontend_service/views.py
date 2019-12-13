import importlib
import typing

from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse

from frontend_service import service_layer, settings

app = Starlette()
app.debug = settings.DEBUG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)


def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({"status": False, "msg": str(exc)}, status_code=403)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


@app.exception_handler(403)
async def not_authorized(request, exc):
    return JSONResponse(
        {"status": False, "msg": "Not Authorized"}, status_code=exc.status_code
    )


async def build_response(
    coroutine: typing.Awaitable, status_code: int = 400
) -> JSONResponse:
    result = await coroutine
    if result.errors:
        return JSONResponse({"status": False, **result.errors}, status_code=400)
    return JSONResponse({"status": True, "data": result.data})


@app.route("/")
async def home(request: Request):
    return JSONResponse({"hello": "world"})


@app.route("/regions/{country}", methods=["GET"])
async def fetch_regions(request: Request):
    country = request.path_params["country"]
    validate_config = bool(request.query_params.get("validate"))
    return await build_response(
        service_layer.fetch_regions(country, validate_config=validate_config)
    )


@app.route("/search/{search_token}", methods=["GET"])
async def tutor_search(request: Request):
    page = request.query_params.get("page") or 1
    search_token = request.path_params["search_token"]
    return await build_response(service_layer.tutor_search(search_token, page=page))
