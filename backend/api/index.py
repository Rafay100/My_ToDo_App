from src.main import app

# Simple test endpoint for Vercel
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/")
def root():
    return {"message": "Welcome to Evolution of Todo API"}

# Export handler for Vercel
handler = app
