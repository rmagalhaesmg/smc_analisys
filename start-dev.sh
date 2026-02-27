#!/bin/bash
# Quick Start Script - Frontend + Backend Integration
# Execute este script para iniciar frontend e backend simultaneamente

echo "🚀 Iniciando SMC SaaS - Frontend + Backend"
echo "=========================================="

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/3]${NC} Verificando ambiente..."

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js não encontrado. Instale em: https://nodejs.org${NC}"
    exit 1
fi

# Verificar se Python está instalado
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python não encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Ambiente verificado${NC}"

# Iniciar Backend
echo -e "\n${BLUE}[2/3]${NC} Iniciando Backend (porta 8000)..."
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend iniciado (PID: $BACKEND_PID)${NC}"

# Aguardar um pouco para o backend iniciar
sleep 3

# Iniciar Frontend
echo -e "\n${BLUE}[3/3]${NC} Iniciando Frontend (porta 3000)..."
cd ../frontend
npm start &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend iniciado (PID: $FRONTEND_PID)${NC}"

echo -e "\n${GREEN}=========================================="
echo -e "🎉 Sistema iniciado com sucesso!${NC}"
echo -e "${GREEN}=========================================="
echo -e "\n📱 URLs de acesso:"
echo -e "  Frontend:        ${BLUE}http://localhost:3000${NC}"
echo -e "  Backend API:     ${BLUE}http://127.0.0.1:8000${NC}"
echo -e "  API Docs:        ${BLUE}http://127.0.0.1:8000/docs${NC}"

echo -e "\n${YELLOW}💡 Para parar:${NC}"
echo -e "  kill $BACKEND_PID  # Parar backend"
echo -e "  kill $FRONTEND_PID # Parar frontend"

# Manter script rodando
wait
