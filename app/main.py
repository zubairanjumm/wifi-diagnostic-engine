from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.diagnostics import router as diagnostics_router

app = FastAPI(
    title="WiFi Diagnostic Engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    diagnostics_router,
    prefix="/api",
)
