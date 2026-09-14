import logging
import time

from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from app.api.health import router as health_router
from app.api.monitors import router as monitors_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)


configure_logging()

logger = logging.getLogger("uptimehub.api")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(health_router)
app.include_router(monitors_router)


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    start_time = time.perf_counter()

    logger.info(
        "request_started method=%s path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)

    except Exception:
        duration = time.perf_counter() - start_time

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            path=request.url.path,
            status_code="500",
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            path=request.url.path,
        ).observe(duration)

        logger.exception(
            "request_failed method=%s path=%s duration_seconds=%.4f",
            request.method,
            request.url.path,
            duration,
        )

        raise

    duration = time.perf_counter() - start_time

    HTTP_REQUESTS_TOTAL.labels(
        method=request.method,
        path=request.url.path,
        status_code=str(response.status_code),
    ).inc()

    HTTP_REQUEST_DURATION_SECONDS.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration)

    logger.info(
        "request_completed method=%s path=%s "
        "status_code=%s duration_seconds=%.4f",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "environment": settings.environment,
    }
