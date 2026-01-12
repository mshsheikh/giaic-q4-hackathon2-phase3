"""
Main FastAPI application for the Todo AI Chatbot
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import BackendConfig
from .routers.chat_router import router as chat_router
from .routers.auth_router import router as auth_router
import uvicorn


# Create the FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for the Todo AI Chatbot system",
    version="1.0.0"
)

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

# Add a health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "service": "Todo AI Chatbot API"}

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
        "backend.main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.DEBUG
    )


if __name__ == "__main__":
    run_server()