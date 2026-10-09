from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router

app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator powered by Google Gemini",
    version="2.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)
