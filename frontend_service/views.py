import importlib
import typing
import databases
from starlette.applications import Starlette
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from starlette.background import BackgroundTasks
from starlette.endpoints import HTTPEndpoint
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from frontend_service import settings 

app = Starlette()
app.debug = settings.DEBUG

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

async def build_response(coroutine:typing.Awaitable, status_code:int=400)->JSONResponse:
    result = await coroutine
    if result.errors:
        return JSONResponse({"status": False, **result.errors}, status_code=400)
    return JSONResponse({"status": True, "data": result.data})


@app.route("/")
class Homepage(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse(f"Hello, world!")
