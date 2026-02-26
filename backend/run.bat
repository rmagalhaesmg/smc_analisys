@echo off
REM Script para iniciar o SMC Web App (Windows)

echo.
echo ============================================================
echo SMC - Sistema de Monitoramento Continuo de Mercado v2.3
echo Web App Backend
echo ============================================================
echo.

REM Verificar se venv existe
if not exist "venv" (
    echo Criando virtual environment...
    python -m venv venv
)

REM Ativar venv
call venv\Scripts\activate.bat

REM Instalar dependências
echo.
echo Verificando/atualizando dependências...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Verificar .env
if not exist ".env" (
    echo.
    echo [AVISO] Arquivo .env não encontrado!
    echo Copiando .env.example para .env
    copy .env.example .env
    echo.
    echo Por favor, edite o arquivo .env com suas credenciais:
    echo - TELEGRAM_BOT_TOKEN
    echo - SENDGRID_API_KEY
    echo - TWILIO_ACCOUNT_SID
    echo - OPENAI_API_KEY
    echo.
)

REM Iniciar servidor
echo.
echo ============================================================
echo Iniciando servidor FastAPI em http://localhost:8000
echo API Docs automaticamente em http://localhost:8000/docs
echo ============================================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Desativar venv ao fechar
call venv\Scripts\deactivate.bat
