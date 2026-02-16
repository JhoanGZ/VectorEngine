from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(title="VectorEngine")

app.include_router(router)
