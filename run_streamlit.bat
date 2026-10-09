@echo off
echo ===================================================
echo   CatalogCraft AI - Streamlit Executive Dashboard
echo ===================================================
echo.
echo NOTE: The primary full-stack React 19 studio runs on http://localhost:5173
echo       (Launch the full platform via run_app.bat)
echo.
echo Starting Streamlit Executive Dashboard on http://localhost:8501...
cd backend
call .venv\Scripts\activate
streamlit run streamlit_app.py
pause
