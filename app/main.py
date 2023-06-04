import sqlalchemy
from core.models import database, DATABASE_URL, metadata, create_roles, with_connect
from endpoints.user import user_route
from endpoints.video import video_router
from endpoints.admin import admin_route
from fastapi.middleware.cors import CORSMiddleware
import fastapi_jsonrpc as jsonrpc
import asyncio

app = jsonrpc.API(
    title='Video Hosting'
)

app.state.database = database

app.bind_entrypoint(user_route)
app.bind_entrypoint(video_router)
app.bind_entrypoint(admin_route)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://127.0.0.1'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.on_event('startup')
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
# asyncio.run(with_connect(create_roles))
