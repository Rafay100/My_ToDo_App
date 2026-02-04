# Startup Guide

## Running the Application

To run this application successfully, you need to start both the backend and frontend servers.

### 1. Start the Backend Server

Navigate to the backend directory and start the server:

```bash
cd backend
python -m uvicorn src.main:app --host localhost --port 8000 --reload
```

Keep this terminal window open as the backend needs to remain running.

### 2. Start the Frontend Server

In a new terminal window, navigate to the frontend directory and start the server:

```bash
cd frontend
npm run dev
```

### 3. Access the Application

Open your browser and go to `http://localhost:3000` to access the application.

## Troubleshooting

### "Failed to fetch" Error

If you encounter a "Failed to fetch" error during signup or any other API call:

1. Verify that the backend server is running on `http://localhost:8000`
2. Check that the backend is accessible by visiting `http://localhost:8000/health`
3. Make sure the `NEXT_PUBLIC_API_URL` in your frontend `.env.local` file is set to `http://localhost:8000`

### Environment Variables

Make sure your `frontend/.env.local` file contains:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

And your `backend/.env` file contains the required environment variables (SECRET_KEY, DATABASE_URL, etc.).

## Common Issues

- **Backend not running**: The most common cause of "Failed to fetch" errors
- **Wrong API URL**: Ensure frontend is pointing to the correct backend URL
- **Port conflicts**: Make sure ports 8000 (backend) and 3000 (frontend) are available