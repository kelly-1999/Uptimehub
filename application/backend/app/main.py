from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.monitors import router as monitors_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(health_router)
app.include_router(monitors_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "environment": settings.environment,
    }
