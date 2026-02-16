from fastapi import FastAPI
from app.api.routes import router
from app.core.logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="VectorEngine")

app.include_router(router)

logger.info("VectorEngine application started")
