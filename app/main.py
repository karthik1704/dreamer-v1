from fastapi import FastAPI

from routers import users
app = FastAPI(title="Dreamer Acadamy V1", version="0.1.0")


app.include_router(users.router)
