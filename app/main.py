from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from scalar_fastapi import get_scalar_api_reference
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import settings
from app.routes.auth_routes import auth_router
from app.routes.post_routes import posts_router
from app.routes.user_routes import users_router

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title=settings.APP_NAME,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(auth_router)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": settings.APP_NAME})


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        title=settings.APP_NAME,
        openapi_url=settings.OPENAPI_URL,
    )
