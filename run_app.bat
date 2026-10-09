@echo off
echo ===================================================
echo   CatalogCraft AI - Launching Full-Stack Platform
echo ===================================================
echo.
echo Starting FastAPI Backend on port 8000...
start "CatalogCraft Backend (FastAPI)" cmd /k "cd backend && call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo Starting React Vite Frontend on port 5173...
start "CatalogCraft Frontend (React+Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   Services are running!
echo   - Frontend Studio: http://localhost:5173
echo   - Backend Swagger API: http://127.0.0.1:8000/docs
echo ===================================================
pause
