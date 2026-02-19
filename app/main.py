import logging
import uuid
from fastapi import FastAPI, Request

from app.api.routes import router
from app.core.logging import setup_logging

# Initialize logging configuration
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="VectorEngine")

# -----------------------------
# Request ID Middleware
# -----------------------------
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info(
        "request_started request_id=%s path=%s",
        request_id,
        request.url.path,
    )

    response = await call_next(request)

    logger.info(
        "request_finished request_id=%s status_code=%d",
        request_id,
        response.status_code,
    )

    response.headers["X-Request-ID"] = request_id
    return response


# Register API routes
app.include_router(router)

logger.info("VectorEngine application started")
