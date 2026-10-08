@echo off
echo ===================================================
echo   CatalogCraft AI - Launching Streamlit Dashboard
echo ===================================================
echo.
cd backend
call .venv\Scripts\activate
echo Starting Streamlit app on http://localhost:8501...
streamlit run streamlit_app.py
pause
