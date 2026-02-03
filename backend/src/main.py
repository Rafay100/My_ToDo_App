from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api import todos, auth
from src.api.chat_endpoint import router as chat_router
from src.services.database_service import create_db_and_tables

app = FastAPI(title="Todo AI Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001",
        "http://localhost:3002", "http://127.0.0.1:3002",
        "https://frontend-silk-theta-40.vercel.app",
        "https://frontend-gwhyg6h8u-rafays-projects-66b7ce12.vercel.app",
        "https://my-to-do-hl66a01o3-rafays-projects-66b7ce12.vercel.app",  # Production frontend
        "https://*.vercel.app",  # Allow all Vercel preview deployments
        "http://127.0.0.1:8000",  # Local backend
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)},
    )

app.include_router(todos.router, prefix="/api/v1")
app.include_router(auth.router)
app.include_router(chat_router)  # Include the chat router for AI functionality

@app.get("/")
def read_root():
    return {"message": "Welcome to Evolution of Todo AI Chatbot API"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
