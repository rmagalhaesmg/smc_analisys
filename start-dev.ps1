# Quick Start Script - Frontend + Backend Integration (Windows PowerShell)
# Execute este script para iniciar frontend e backend simultaneamente
# Uso: .\start-dev.ps1

Write-Host "🚀 Iniciando SMC SaaS - Frontend + Backend" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Verificar diretório
if (-not (Test-Path ".\frontend") -or -not (Test-Path ".\backend")) {
    Write-Host "❌ Execute este script na raiz do projeto (smc_analysys)" -ForegroundColor Red
    exit 1
}

Write-Host "`n[1/2] Iniciando Backend (http://127.0.0.1:8000)..." -ForegroundColor Blue

# Iniciar Backend em uma nova janela do cmd
Start-Process cmd -ArgumentList "/K", "cd /d c:\Users\Usuário\Documents\smc_analysys\backend && .venv\Scripts\python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000" 
Write-Host "✅ Backend iniciado" -ForegroundColor Green

# Aguardar um pouco para o backend iniciar
Start-Sleep -Seconds 3

Write-Host "`n[2/2] Iniciando Frontend (http://localhost:3000)..." -ForegroundColor Blue

# Iniciar Frontend em uma nova janela do cmd
Start-Process cmd -ArgumentList "/K", "cd /d c:\Users\Usuário\Documents\smc_analysys\frontend && npm start"
Write-Host "✅ Frontend iniciado" -ForegroundColor Green

Write-Host "`n==========================================" -ForegroundColor Green
Write-Host "🎉 Sistema iniciado com sucesso!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📱 URLs de acesso:" -ForegroundColor Yellow
Write-Host "  Frontend:        http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend API:     http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  API Docs:        http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Dicas:" -ForegroundColor Yellow
Write-Host "  • Frontend e Backend abriram em janelas separadas"
Write-Host "  • Feche as janelas para parar o servico"
Write-Host "  • Verificar arquivo INTEGRACAO_FRONTEND.md para mais detalhes"
Write-Host ""

Write-Host "✨ Concluido!" -ForegroundColor Green
