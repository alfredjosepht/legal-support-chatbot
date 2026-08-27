@echo off
REM Quick start script for Legal Support Chatbot (Windows)

echo Starting Legal Support Chatbot...
echo.

REM Start backend
echo Starting backend on port 8000...
start /B python -m uvicorn app:app --reload --port 8000
echo   Backend starting...

REM Start frontend
echo Starting frontend on port 3001...
cd frontend
start /B cmd /c "set PORT=3001 && npm start"
cd ..

echo.
echo Legal Support Chatbot is starting!
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3001
echo.
pause
