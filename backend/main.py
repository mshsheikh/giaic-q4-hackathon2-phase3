"""
Main FastAPI application for the Todo AI Chatbot
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import BackendConfig
from routers.chat_router import router as chat_router
from routers.auth_router import router as auth_router
from database.connection import create_db_and_tables
import uvicorn
import logging
import traceback

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("todo-api")


# Create the FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for the Todo AI Chatbot system",
    version="1.0.0"
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    # do not include full secrets in this response
    return JSONResponse(status_code=500, content={"error":"internal_server_error","message":"An internal server error occurred"})

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


# Initialize database tables on startup
@app.on_event("startup")
async def on_startup():
    """
    Initialize database tables when the application starts.
    """
    create_db_and_tables()


# Add a health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "service": "Todo AI Chatbot API"}

# Add a test endpoint for dev and fetch testing
@app.get("/api/test")
async def test_endpoint():
    """
    Test endpoint for development and fetch testing.
    """
    return {"status": "ok"}

# Add a root endpoint
@app.get("/")
async def root():
    """
    Root endpoint to verify the API is accessible.
    """
    return {"message": "Welcome to the Todo AI Chatbot API", "status": "running"}


def run_server():
    """
    Run the FastAPI server using uvicorn.
    """
    config = BackendConfig()

    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.DEBUG
    )


if __name__ == "__main__":
    run_server()