from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.routes.post_routes import posts_router
from app.routes.user_routes import users_router
from app.tasks.tasks import do_heavy_task
from app.utils.websocket import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.setup_redis()
    yield
    await manager.redis.close()


app = FastAPI(
    title=settings.APP_NAME,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)


app.include_router(users_router)
app.include_router(posts_router)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_client(f"Client {client_id} says: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)


@app.get("/")
async def read_root():
    do_heavy_task.delay("test")
    return {"message": "ok after CI/CD"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(
        title=settings.APP_NAME,
        openapi_url=settings.OPENAPI_URL,
    )
