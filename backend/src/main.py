from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api import todos, auth

app = FastAPI(title="Evolution of Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001",
        "http://localhost:3002", "http://127.0.0.1:3002",
        "https://frontend-silk-theta-40.vercel.app",
        "https://frontend-gwhyg6h8u-rafays-projects-66b7ce12.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)},
    )

app.include_router(todos.router, prefix="/api/v1")
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Evolution of Todo API"}
