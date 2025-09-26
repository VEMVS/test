from fastapi import FastAPI
from .routers import notes, user, auth, url

app = FastAPI()

app.include_router(notes.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(url.router)