# Quick start script for Legal Support Chatbot (PowerShell)
$ErrorActionPreference = "Continue"

Write-Host "🚀 Starting Legal Support Chatbot..." -ForegroundColor Cyan

# Start backend
Write-Host "Starting backend on port 8000..." -ForegroundColor Yellow
Start-Process -NoNewWindow python -ArgumentList "-m", "uvicorn", "app:app", "--reload", "--port", "8000"

# Start frontend
Write-Host "Starting frontend on port 3001..." -ForegroundColor Yellow
Push-Location frontend
$env:PORT = "3001"
Start-Process -NoNewWindow npm -ArgumentList "start"
Pop-Location

Write-Host ""
Write-Host "🎉 Legal Support Chatbot is starting!" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3001" -ForegroundColor White
