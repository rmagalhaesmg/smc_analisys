#!/bin/bash
# Script para iniciar o SMC Web App (Linux/Mac)

echo ""
echo "============================================================"
echo "SMC - Sistema de Monitoramento Continuo de Mercado v2.3"
echo "Web App Backend"
echo "============================================================"
echo ""

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "Criando virtual environment..."
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências
echo ""
echo "Verificando/atualizando dependências..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# Verificar .env
if [ ! -f ".env" ]; then
    echo ""
    echo "[AVISO] Arquivo .env não encontrado!"
    echo "Copiando .env.example para .env"
    cp .env.example .env
    echo ""
    echo "Por favor, edite o arquivo .env com suas credenciais:"
    echo "- TELEGRAM_BOT_TOKEN"
    echo "- SENDGRID_API_KEY"
    echo "- TWILIO_ACCOUNT_SID"
    echo "- OPENAI_API_KEY"
    echo ""
fi

# Iniciar servidor
echo ""
echo "============================================================"
echo "Iniciando servidor FastAPI em http://localhost:8000"
echo "API Docs automaticamente em http://localhost:8000/docs"
echo "============================================================"
echo ""

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
