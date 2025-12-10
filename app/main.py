from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.config import settings
from app.core.middleware import firewall_middleware
from app.api.v1.management import router as management_router
from app.services.db_logger import init_db
import os

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered API Firewall for semantic threat detection.",
    version="1.0.0"
)

app.include_router(management_router)

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    import os
    path = "app/templates/index.html"
    print(f"Landing page requested. Current dir: {os.getcwd()}, Looking for: {path}")
    if not os.path.exists(path):
        print(f"File not found at {path}")
        return "<h1>File not found</h1>"
    with open(path, "r") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    with open("app/templates/dashboard.html", "r") as f:
        return f.read()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.middleware("http")
async def add_firewall_middleware(request: Request, call_next):
    return await firewall_middleware(request, call_next)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "env": settings.APP_ENV,
        "service": settings.APP_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
