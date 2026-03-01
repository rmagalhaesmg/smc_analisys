"""
SMC Web App - Guia Rápido de Setup

Este arquivo contém instruções passo a passo para colocar o sistema em produção.
"""

# ============================================================================
# PASSO 1: INSTALAÇÃO INICIAL
# ============================================================================

"""
Windows:
  1. Abrir PowerShell como Administrador
  2. Navegar até: c:/Users/Usuário/Documents/smc_analysys/backend
  3. Executar: .\\run.bat

Linux/Mac:
  1. Abrir Terminal
  2. Navegar até o diretório do projeto
  3. Executar: chmod +x run.sh && ./run.sh
"""

# ============================================================================
# PASSO 2: CONFIGURAR CREDENCIAIS
# ============================================================================

"""
Editar arquivo .env com:

1. TELEGRAM (Obrigatório para alertas)
   - Acessar @BotFather em Telegram
   - Criar novo bot
   - Copiar token para TELEGRAM_BOT_TOKEN
   - Seu Chat ID: enviar /start para bot e acessar:
     https://api.telegram.org/bot{TOKEN}/getUpdates
   - Copiar chat_id para TELEGRAM_CHAT_IDS

2. EMAIL (Opcional para alertas por email)
   - Criar conta em sendgrid.com
   - Gerar API Key
   - Copiar para SENDGRID_API_KEY

3. WHATSAPP (Opcional para alertas via WhatsApp)
   - Criar conta em twilio.com
   - Obter Account SID e Auth Token
   - Copiar para TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN

4. OpenAI/LLM (Opcional para análise com IA)
   - Criar chave em openai.com/api
   - Copiar chave sk-... para OPENAI_API_KEY

5. Parâmetros SMC
   - SMC_TIPO_ATIVO: 1=WIN, 2=WDO, 3=NASDAQ, 4=ES, 5=Ações, 6=Forex, 7=Cripto
   - SMC_TF_BASE_MINUTOS: Timeframe padrão (5min recomendado)
   - SMC_MODO_OPERACAO: 1=Conservador, 2=Normal, 3=Agressivo
"""

# ============================================================================
# PASSO 3: VERIFICAR INSTALAÇÃO
# ============================================================================

"""
Após iniciar o servidor, visitar:
  http://localhost:8000/docs

Você verá a documentação automática do Swagger com todos os endpoints.
"""

# ============================================================================
# PASSO 4: TESTAR COM ARQUIVO CSV
# ============================================================================

"""
Preparar arquivo CSV com formato:

timestamp,open,high,low,close,volume,trades,aggression_buy,aggression_sell
2024-02-26 09:30:00,127850.00,128200.00,127700.00,128100.00,1200000,4850,750000,450000
2024-02-26 09:35:00,128100.00,128550.00,128050.00,128400.00,1450000,5120,800000,650000
...

Opções para enviar:
1. Via Swagger: Acessar http://localhost:8000/docs -> POST /data/upload-csv
2. Via curl:
   curl -X POST \\
     -H "accept: application/json" \\
     -H "Content-Type: multipart/form-data" \\
     -F "file=@seu_arquivo.csv" \\
     http://localhost:8000/data/upload-csv

3. Via Python:
   import requests
   
   with open('seu_arquivo.csv', 'rb') as f:
       files = {'file': f}
       response = requests.post(
           'http://localhost:8000/data/upload-csv',
           files=files
       )
       print(response.json())
"""

# ============================================================================
# PASSO 5: INTEGRA COM NEOLÓGICA RTD
# ============================================================================

"""
Usar arquivo: NEOLOGICA_INTEGRATION.py

Exemplo básico:
```python
from NEOLOGICA_INTEGRATION import NeologicaAPIIntegration
import asyncio

async def main():
    api = NeologicaAPIIntegration(api_key="sua_chave_aqui")
    await api.connect()
    
    # Buscar dados continuamente
    while True:
        candle = await api.fetch_candle("WIN@H25", timeframe=5)
        
        # Enviar para análise
        import requests
        requests.post(
            "http://localhost:8000/analyze/candle",
            json=candle
        )
        
        await asyncio.sleep(5)

asyncio.run(main())
```

Para Profit/Windows RTD direto:
```python
from NEOLOGICA_INTEGRATION import ProfitRTDIntegration

rtd = ProfitRTDIntegration()
if rtd.connect_rtd():
    price = rtd.get_price("WIN@H25")
    print(f"Preço: {price}")
```
"""

# ============================================================================
# PASSO 6: MONITORAR ALERTAS
# ============================================================================

"""
Após configurar notificações, alertas serão enviados quando:

1. Score > 60 com confluência forte → Sinal de compra/venda
2. Armadilha detectada → Telegram e WhatsApp
3. Divergência confirmada → Email + Telegram
4. Exaustão de movimento → Aviso geral

Verificar histórico de sinais:
  GET http://localhost:8000/signals/history?limit=20

Testar notificações:
  curl -X POST http://localhost:8000/notifications/test
"""

# ============================================================================
# PASSO 7: TREINAR MODELO ML
# ============================================================================

"""
Após coletar ~50+ sinais com outcomes:

1. Treinar modelo:
   curl -X POST http://localhost:8000/ml/train

2. Verificar status:
   curl http://localhost:8000/ml/model-status

3. O modelo vai refinar automaticamente os scores baseado em:
   - Taxa de acerto histórica
   - Lucro por tipo de sinal
   - Nível de confluência
"""

# ============================================================================
# PASSO 8: USAR ANÁLISE LLM
# ============================================================================

"""
Com OpenAI configurado, cada sinal será analisado com:
- Confirmação de força do sinal
- Identificação de riscos
- Sugestões de SL e TP
- Análise contextual de mercado

Verificar análise em:
  GET http://localhost:8000/signals/history
  (campo 'llm_analysis' em cada sinal)
"""

# ============================================================================
# ENDPOINTS PRINCIPAIS
# ============================================================================

"""
ANÁLISE:
  POST /analyze/candle          → Analisar um candle
  GET /signals/history          → Histórico de sinais

DADOS:
  POST /data/upload-csv         → Fazer upload de CSV
  POST /data/api-stream         → Conectar API externa

NOTIFICAÇÕES:
  POST /notifications/configure → Configurar canais
  POST /notifications/test      → Testar notificações

ML/IA:
  GET /ml/model-status          → Status do modelo
  POST /ml/train                → Treinar modelo

SISTEMA:
  GET /                          → Info da aplicação
  GET /health                    → Health check
  GET /settings                  → Configurações ativas
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Erro 1: "Telegram não configurado"
  → Verificar se TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_IDS estão em .env

Erro 2: "Connection refused localhost:8000"
  → Servidor não iniciado. Executar run.bat/run.sh

Erro 3: "Invalid CSV columns"
  → Arquivo CSV deve ter: timestamp,open,high,low,close,volume,trades,aggression_buy,aggression_sell

Erro 4: "OpenAI API error"
  → Verificar OPENAI_API_KEY válida ou remover para desabilitar LLM

Erro 5: "Porta 8000 já em uso"
  → Alterar na linha: uvicorn main:app --port 9000
"""

# ============================================================================
# PRÓXIMOS PASSOS
# ============================================================================

"""
1. ✅ Setup básico completo
2. □ Integrar dados históricos (CSV large)
3. □ Conectar ao Neológica RTD em tiempo real
4. □ Treinar modelo ML com dados de operações
5. □ Análise contínua com LLM
6. □ Dashboard web (frontend)
7. □ Backtesting e otimização de parâmetros
"""

print(__doc__)
