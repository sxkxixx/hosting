from fastapi import FastAPI
import uvicorn
from user.models import Role, User
from database import db
from user.api import user_route
from template_route.template_route import template_route

app = FastAPI(
    title='Video Hosting'
)
app.include_router(user_route)
app.include_router(template_route)


@app.get('/')
async def render_home_page():
    return {'page': 'home'}


if __name__ == "__main__":
    db.connect()
    db.create_tables([Role, User])
    uvicorn.run(app, host="127.0.0.1", port=8000)
