"""
CHECKLIST DE IMPLEMENTAÇÃO - Passo a Passo

Use este checklist para colocar o SMC Web App em produção.
"""

# ============================================================================
# FASE 1: SETUP INICIAL (30 min)
# ============================================================================

"""
□ 1.1 Verificar Python instalado
   → Abrir PowerShell e digitar: python --version
   → Deve retornar Python 3.10+

□ 1.2 Clonar/extrair projeto
   → Já está em: c:/Users/Usuário/Documents/smc_analysys
   → Verificar que existe pasta: backend/

□ 1.3 Executar instalação
   → Windows: Executar backend\run.bat
   → Linux/Mac: chmod +x backend/run.sh && ./backend/run.sh
   → Aguardar conclusão (2-5 minutos)

□ 1.4 Verificar instalação
   → Abrir browser: http://localhost:8000
   → Deve exibir: {"name": "SMC Web App v1.0", ...}
   → Acessar docs: http://localhost:8000/docs

□ 1.5 Criar arquivo .env
   → Copiar backend\\.env.example → backend\\.env
   → Editar arquivo conforme seção abaixo
"""

# ============================================================================
# FASE 2: CONFIGURAÇÃO DE CREDENCIAIS (45 min)
# ============================================================================

"""
ARQUIVO: backend/.env

□ 2.1 Telegram (RECOMENDADO)
   Passos:
   1. Abrir Telegram e procurar por @BotFather
   2. Digitar /start
   3. Digitar /newbot
   4. Fornecer nome do bot (ex: "meu_bot_smc")
   5. Fornecer username (ex: "meu_bot_smc_123bot")
   6. Copiar TOKEN fornecido (formato: 123456:ABC-DEF...)
   
   No arquivo .env:
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
   
   7. Enviar /start para seu bot
   8. Obter seu Chat ID:
      → Abrir https://api.telegram.org/bot{SEU_TOKEN}/getUpdates
      → Procurar "id" em "from" (seu Chat ID)
      → Exemplo: 123456789
   
   No arquivo .env:
   TELEGRAM_CHAT_IDS=123456789,987654321  # Você + outra pessoa? Seperado por vírgula

□ 2.2 Email via SendGrid (OPCIONAL)
   Passos (se quiser receber análises pro email):
   1. Ir para sendgrid.com
   2. Criar conta free
   3. Acessar API Keys
   4. Criar nova chave com permissão "Mail Send"
   5. Copiar chave (formato: SG.xxx...)
   
   No arquivo .env:
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
   SENDGRID_FROM_EMAIL=alerts@seu-dominio.com
   SENDGRID_RECIPIENTS=seu.email@gmail.com,outro@email.com

□ 2.3 WhatsApp via Twilio (OPCIONAL)
   Passos (se quiser WhatsApp):
   1. Ir para twilio.com
   2. Criar conta (free com crédito)
   3. Obter Account SID e Auth Token
   4. Configurar número Twilio
   
   No arquivo .env:
   TWILIO_ACCOUNT_SID=ACxxxxx...
   TWILIO_AUTH_TOKEN=xxxxx...
   TWILIO_FROM_NUMBER=+55119999999  # Número Twilio
   TWILIO_TO_NUMBERS=+5511988888888  # Seu WhatsApp

□ 2.4 OpenAI/ChatGPT (OPCIONAL)
   Passos (para análise com IA):
   1. Ir para openai.com/api
   2. Fazer login
   3. Acessar Account → API keys
   4. Criar nova chave (formato: sk-...)
   
   No arquivo .env:
   OPENAI_API_KEY=sk-xxxxxxxxxxxxx
   OPENAI_MODEL=gpt-4

□ 2.5 Parâmetros SMC
   No arquivo .env:
   
   # Tipo de ativo que está analisando
   SMC_TIPO_ATIVO=1  # 1=WIN (recomendado para começar)
   
   # Timeframe base em minutos
   SMC_TF_BASE_MINUTOS=5  # 5 min recomendado
   
   # Modo de operação
   SMC_MODO_OPERACAO=2  # 1=Conservative, 2=Normal (recommended), 3=Aggressive
   
   # Ativar/desativar features
   SMC_ALERTING_ENABLED=true
   SMC_ML_REFINEMENT=true
   SMC_LLM_ANALYSIS=true

□ 2.6 Validar .env
   → Arquivo deve ter todas as variáveis preenchidas
   → As opcionais (Email, WhatsApp, OpenAI) podem ficar vazias
   → Salvar arquivo e fechar
"""

# ============================================================================
# FASE 3: TESTE BÁSICO (15 min)
# ============================================================================

"""
□ 3.1 Iniciar servidor
   → Abrir PowerShell na pasta backend
   → Digitar: python -m uvicorn main:app --reload
   → Deve exibir: "Uvicorn running on http://127.0.0.1:8000"

□ 3.2 Acessar Swagger UI
   → Abrir browser: http://localhost:8000/docs
   → Deve carregar página interativa com todos os endpoints

□ 3.3 Testar endpoint simples
   → Na página Swagger, procurar por: GET /health
   → Clicar em "Try it out"
   → Clicar em "Execute"
   → Deve retornar: {"status": "healthy", ...}

□ 3.4 Testar análise de candle
   → Procurar: POST /analyze/candle
   → Clicar em "Try it out"
   → Copiar JSON abaixo em "Request body":
   
   {
     "timestamp": "2024-02-26 09:30:00",
     "open": 127850,
     "high": 128200,
     "low": 127700,
     "close": 128100,
     "volume": 1200000,
     "trades": 4850
   }
   
   → Clicar "Execute"
   → Deve retornar análise completa com score, recomendação, etc.

□ 3.5 Verificar notificações (opcional)
   → Procurar: POST /notifications/test
   → Clicar "Execute"
   → Deve receber mensagem no Telegram em poucos segundos!
   
   Se recebeu: ✓ Notificações funcionando
   Se não recebeu: 
   - Verificar se TELEGRAM_BOT_TOKEN está correto em .env
   - Verificar se TELEGRAM_CHAT_IDS está correto
   - Reiniciar servidor (Ctrl+C e rodar novamente)
"""

# ============================================================================
# FASE 4: TESTE COM DADOS REAIS (30 min)
# ============================================================================

"""
□ 4.1 Preparar dados
   → Você tem dois formatos:
   
   Opção A: Usar arquivo de exemplo (RECOMENDADO para começar)
   → Arquivo já existe: backend/example_data.csv
   → Contém 30 candles WIN@H25 de fevereiro de 2024
   
   Opção B: Usar seus dados
   → Preparar CSV com colunas: timestamp,open,high,low,close,volume,trades
   → Salvar em: backend/seu_arquivo.csv

□ 4.2 Upload do arquivo
   → Abrir Swagger: http://localhost:8000/docs
   → Procurar: POST /data/upload-csv
   → Clicar "Try it out"
   → Usuario: Choose file → Selecionar example_data.csv (ou seu arquivo)
   → Clicar "Execute"
   → Aguardar processamento (2-5 seg)

□ 4.3 Verificar resultados
   → Deve retornar:
     {
       "file_name": "example_data.csv",
       "total_candles": 30,
       "processed": 30,
       "generated_signals": 5,
       "avg_score": 68.2,
       "top_signal": {...}
     }

□ 4.4 Consultar sinais gerados
   → Procurar: GET /signals/history
   → Clicar "Try it out"
   → Parâmetros: limit=10, min_score=70
   → Clicar "Execute"
   → Deve listar os sinais processados com análise completa

□ 4.5 Exportar resultados
   → No seu terminal (PowerShell), navegar até backend/
   → Digitar: python
   → Colar código abaixo:
   
   import requests
   import pandas as pd
   
   response = requests.get("http://localhost:8000/signals/history?limit=100")
   signals = response.json()
   
   df = pd.DataFrame([
       {
           'timestamp': s['timestamp'],
           'score': s['final_score'],
           'recommendation': s['recommendation'],
           'confluencia': s['signals']['confluencia'],
           'hfz': s['signals']['hfz_score'],
           'mtv': s['signals']['mtv_score']
       }
       for s in signals
   ])
   
   df.to_csv('resultados_analise.csv', index=False)
   print("✓ Salvo em: resultados_analise.csv")
   
   → Sair do Python: exit()
   → Arquivo estará em: backend/resultados_analise.csv
"""

# ============================================================================
# FASE 5: INTEGRAÇÃO COM DADOS LIVE (Escolha UMA opção)
# ============================================================================

"""
OPÇÃO A: Usar API de Broker (RECOMENDADO - Melhor compatibilidade)
─────────────────────────────────────────────────────────────────

□ 5A.1 Obter API Key do seu broker
   → Se usa Neológica: solicitar API key em suporte
   → Se usa Profit: usar RTD (veja próxima opção)
   → Se usa MetaTrader: usar arquivo NEOLOGICA_INTEGRATION.py

□ 5A.2 Testar conexão
   → Abrir arquivo: backend/NEOLOGICA_INTEGRATION.py
   → Seção "NeologicaAPIIntegration" (primeiras ~100 linhas)
   → Copiar código de exemplo
   → Adaptar sua API key
   → Executar para testar

□ 5A.3 Integrar no seu código
   → Seu código deve continuously fazer:
   
   candle_data = await api.fetch_candle("WIN@H25", timeframe=5)
   response = requests.post("http://localhost:8000/analyze/candle", 
                            json=candle_data)
   
   → Sistema vai analisar e enviar alertas automaticamente


OPÇÃO B: Usar RTD do Profit (WINDOWS ONLY - Real-time mais rápido)
──────────────────────────────────────────────────────────────────

□ 5B.1 Verificar Profit instalado
   → Ter Profit terminal aberto
   → COM deve estar ativado em Profit

□ 5B.2 Usar integração RTD
   → Ver arquivo: backend/NEOLOGICA_INTEGRATION.py
   → Seção "ProfitRTDIntegration"
   → Código exemplo:
   
   rtd = ProfitRTDIntegration()
   if rtd.connect_rtd():
       price = rtd.get_price("WIN@H25")
       print(f"Preço atual: {price}")
   
   → Preferir RTD para trading real (menor latência)


OPÇÃO C: Usar DLL/Conexão Nativa (AVANÇADO)
──────────────────────────────────────────────

□ 5C.1 Preparar DLL
   → Ver arquivo: backend/NEOLOGICA_INTEGRATION.py
   → Seção "NeologicaDLLIntegration"
   → Executar apenas se familiarizado com ctypes/DLL
"""

# ============================================================================
# FASE 6: TREINAR MODELO ML (Após ~50+ sinais)
# ============================================================================

"""
□ 6.1 Aguardar histórico
   → Deixar sistema rodando e coletando sinais
   → Coletar pelo menos 50-100 sinais com outcomes
   → Vai levar alguns dias de trading

□ 6.2 Treinar modelo
   → Abrir Swagger: http://localhost:8000/docs
   → Procurar: POST /ml/train
   → Clicar "Execute"
   → Aguardar conclusão (~2-5 minutos)

□ 6.3 Verificar performance
   → Procurar: GET /ml/model-status
   → Clicar "Execute"
   → Verificar:
     - R² Score (> 0.7 é bom)
     - Feature Importance (qual métrica mais importante)
     - Win Rate por score (calibração do modelo)

□ 6.4 Usar modelo
   → Após treinamento, sistema automaticamente:
     - Refina scores com modelo ML
     - Aplica multiplicador adaptive baseado em histórico
     - Melhora precisa conforme mais trades completados
"""

# ============================================================================
# FASE 7: DEPLOY EM PRODUÇÃO (AVANÇADO)
# ============================================================================

"""
Para colocar o sistema 24/7 (sem deixar PowerShell aberto):

□ 7.1 Criar Windows Service (WINDOWS)
   → Usar: NSSM (Non-Sucking Service Manager)
   → Download: https://nssm.cc/download
   → Extrair e colocar nssm.exe no PATH
   → Digitar em PowerShell (Admin):
   
   nssm install SMCWebApp "C:/Python310/python.exe" ^
     "-m uvicorn main:app --host 0.0.0.0 --port 8000"
   
   nssm start SMCWebApp
   
   → Sistema será iniciado automaticamente ao ligar PC

□ 7.2 Usar Docker (MULTIPLATAFORMA)
   → Criar arquivo: backend/Dockerfile
   → Copiar conteúdo de exemplo:
   
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   
   → Buildar: docker build -t smc-app .
   → Rodar: docker run -p 8000:8000 --env-file .env smc-app

□ 7.3 Usar VPS Cloud (RECOMENDADO para produção)
   → Opções: AWS, Google Cloud, DigitalOcean, etc
   → Deploy é simples (git push + docker run)
   → Custa ~$5-10/mês
"""

# ============================================================================
# FASE 8: MONITORAMENTO & MANUTENÇÃO
# ============================================================================

"""
□ 8.1 Monitorar sinais diariamente
   → Acessar: http://localhost:8000/docs
   → GET /signals/history
   → Verificar score, recomendações, confluência
   → Correlacionar com preço real (foi acertado?)

□ 8.2 Log de alertas
   → Todos os sinais são salvos em histórico
   → Pode exportar em CSV para análise
   → Verificar falsos positivos/negativos

□ 8.3 Atualizar modelo ML
   → Toda semana depois de 50+ novos sinais
   → Re-treinar com: POST /ml/train
   → Modelo vai ficando mais preciso com tempo

□ 8.4 Ajustar parâmetros
   → Se falsos positivos: aumentar min_score_for_alert
   → Se perdendo bons sinais: diminuir min_score_for_alert
   → Editar em: /notifications/configure → alert_thresholds

□ 8.5 Backup de dados
   → Exportar sinais periodicamente:
     curl http://localhost:8000/signals/history?limit=10000 > backup.json
   → Guardar em local seguro
"""

# ============================================================================
# FASE FINAL: VALIDAÇÃO FUNCIONAL
# ============================================================================

"""
Checklist Final - Sistema está pronto quando:

□ Servidor inicia sem erros: ✓ python -m uvicorn main:app --reload
□ Swagger UI carrega: ✓ http://localhost:8000/docs
□ Health check funciona: ✓ GET /health → 200 OK
□ Candle pode ser analisado: ✓ POST /analyze/candle → score + recomendação
□ Arquivo CSV pode ser uploadado: ✓ POST /data/upload-csv → 30+ sinais
□ Notificações funcionam: ✓ POST /notifications/test → mensagem no Telegram
□ Histórico de sinais existe: ✓ GET /signals/history → 30+ sinais salvos
□ ML está pronto para treino: ✓ GET /ml/model-status → "model_trained": false
□ Configurações aparecem: ✓ GET /settings → JSON com todos os parâmetros

Se todos os itens acima têm ✓, seu sistema está 100% FUNCIONAL!

PRÓXIMO PASSO: Conectar dados reais (RTD/API) e começar a operar.
"""

print(__doc__)
