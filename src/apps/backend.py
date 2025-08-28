from fastapi import FastAPI
from src.api.auth.endpoints import router as auth_router


app = FastAPI()
app.include_router(router=auth_router, prefix="/api/v1")