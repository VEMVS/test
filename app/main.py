from fastapi import FastAPI
from .routers import notes, user

app = FastAPI()

app.include_router(notes.router)
app.include_router(user.router)