# SMC Web App - README

## Sistema de Monitoramento Contínuo (SMC) - Web App v2.3

Um web app robusto e inteligente que transforma o indicador SMC do Neológica em um sistema profissional de análise técnica com:

- ✅ **Análise Multimodular SMC**: HFZ, FBI, DTM, SDA, MTV
- ✅ **Ingestão de Dados**: CSV, API, RTD, DLL
- ✅ **Notificações Multi-Canal**: Telegram, Email, WhatsApp
- ✅ **IA/LLM Integrada**: OpenAI GPT para análise contextual
- ✅ **Machine Learning**: Aprendizado contínuo e refinamento de sinais
- ✅ **Interface REST API**: FastAPI com documentação automática

## Instalação

### 1. Pré-requisitos
- Python 3.10+
- pip

### 2. Setup do Projeto

```bash
cd backend
python -m venv venv

# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar Credenciais

```bash
cp .env.example .env
# Editar .env e adicionar suas credenciais
```

Credenciais necessárias:

**Telegram:**
- Criar bot em @BotFather (t.me/BotFather)
- Obter token do bot
- Obter Chat ID: envie mensagem para bot e acesse `https://api.telegram.org/bot{TOKEN}/getUpdates`

**Email (SendGrid):**
- Criar conta em sendgrid.com
- Gerar API key

**WhatsApp (Twilio):**
- Criar conta em twilio.com
- Obter Account SID, Auth Token, número Twilio

**OpenAI (LLM):**
- Criar chave de API em openai.com
- Copiar chave sk-...

## Execução

### Iniciar Server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Acessar: `http://localhost:8000/docs` (Swagger UI)

### Processar CSV de Dados

```bash
# Fazer upload de arquivo CSV com dados de candles
curl -X POST \"http://localhost:8000/data/upload-csv\" \\
  -H \"accept: application/json\" \\
  -H \"Content-Type: multipart/form-data\" \\
  -F \"file=@seu_arquivo.csv\"
```

Formato esperado do CSV:
```
timestamp,open,high,low,close,volume,trades,aggression_buy,aggression_sell
2024-02-26 09:30:00,100.00,101.50,99.50,100.75,1000000,5000,600000,400000
2024-02-26 09:35:00,100.75,102.00,100.50,101.50,1200000,5200,700000,500000
```

### Analisar Candle Individual

```bash
curl -X POST \"http://localhost:8000/analyze/candle\" \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"timestamp\": \"2024-02-26 12:00:00\",
    \"open\": 100.50,
    \"high\": 102.00,
    \"low\": 100.00,
    \"close\": 101.50,
    \"volume\": 1500000,
    \"trades\": 5500,
    \"aggression_buy\": 800000,
    \"aggression_sell\": 700000
  }'
```

### Configurar Notificações

```bash
curl -X POST \"http://localhost:8000/notifications/configure\" \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"telegram_token\": \"seu_token\",
    \"telegram_chat_ids\": [\"123456789\"],
    \"email_to\": [\"seu_email@example.com\"],
    \"sendgrid_key\": \"sua_chave_sg\"
  }'
```

### Testar Notificações

```bash
curl -X POST \"http://localhost:8000/notifications/test\" \\
  -H \"Content-Type: application/json\" \\
  -d '{
    \"channels\": [\"telegram\", \"email\", \"whatsapp\"]
  }'
```

### Treinar Modelo ML

```bash
curl -X POST \"http://localhost:8000/ml/train\" \\
  -H \"Content-Type: application/json\"
```
## Validação Profit × App

Após exportar os resultados do indicador NTSL no Profit (CSV) e obter
saída equivalente do backend (usando `GET /signals/history` ou o CSV de
processamento), execute o utilitário de validação:

```bash
cd backend
python -m validation.compare profit_output.csv app_output.csv -o report_folder
```

O relatório gerado contém:

* `comparison_full.csv` – tabela completa com métricas lado a lado
* `failures.csv` – apenas os candles que violaram os critérios
* `divergences.png` – gráfico mostrando Profit vs App para cada score
* `report.txt` – resumo estatístico (média, máximos, contagem de erros)

Critérios de divergência:

* métricas numéricas até 2% de diferença são aceitáveis
* regime divergente ⇒ **erro**
* trap flag divergente ⇒ **erro crítico**
* recomendação oposta ⇒ **erro crítico**
## Estrutura do Projeto

```
backend/
├── app/
│   ├── modules/          # Módulos SMC (HFZ, FBI, DTM, SDA, MTV)
│   ├── notifications/    # Sistema de notificações
│   ├── data_ingestion/   # Ingestão de dados
│   ├── ai_ml/           # IA/ML e LLM
│   ├── config.py        # Configurações
│   └── __init__.py
├── main.py              # Aplicação FastAPI
├── requirements.txt     # Dependências
├── .env.example        # Template de configuração
└── README.md           # Este arquivo
```

## Módulos SMC

### HFZ (Microestrutura e Fluxo)
Analisa:
- Delta suavizado (volume agressivo)
- Frequência de trades
- Absorção de volume
- Imbalance de compra/venda
- Pressão líquida

### FBI (Zonas Institucionais)
Analisa:
- Identificação de zonas (suporte/resistência)
- Força de zonas
- Contato com zonas próximas
- Reação em zonas críticas

### DTM (Validação)
Detecta:
- Armadilhas (false breakouts)
- Falhas de continuidade
- Eficiência de deslocamento
- Renovação real de volume

### SDA (Regime de Mercado)
Classifica:
- Tendência (confirmação em movimento)
- Lateralização (consolidação)
- Transição (mudança de regime)
- Volatilidade e fases do movimento

### MTV (Confluência Multi-TF)
Analisa:
- Alinhamento entre 5 timeframes (Semanal, Diário, 240min, 60min, TF base)
- Pesos dinâmicos por regime
- Detecção de divergências confirmadas
- Sugestão automática de tamanho Renko

## Sinais Gerados

Cada análise gera um sinal com:

- **type**: buy_signal, sell_signal, neutral, warning
- **score**: 0-100 (quanto maior, mais forte o sinal)
- **price**: Preço atual
- **regime**: Tendência, Lateral ou Transição
- **confluence_level**: 0-3 (0=nenhuma, 3=total)
- **renko_suggestion**: Tamanho sugerido para análise Renko
- **session**: Sessão de mercado atual
- **hfz_score, fbi_score, dtm_score, sda_score, mtv_score**: Scores individuais dos módulos
- **warnings**: Lista de avisos (armadilhas, divergências, etc)
- **llm_analysis**: Análise contextual fornecida pela IA (se configurada)

## Alertas

Alertas são enviados quando:
- Score > 60 com confluência forte
- Armadilha detectada com intensidade alta
- Divergência confirmada entre timeframes
- Exaustão de movimento detectada

Canais de notificação:
1. **Telegram**: Mensagens formatadas em HTML
2. **Email**: Emails em HTML com detalhes completos
3. **WhatsApp**: Mensagens curtas e objetivas para avisos críticos

## Machine Learning

O sistema aprende continuamente:

1. **Treinamento**: Após 10+ sinais com outcomes conhecidos
2. **Features**: HFZ, FBI, DTM, SDA, MTV, Confluência, Volatilidade, Volume
3. **Predição**: Refinamento automático de scores baseado em histórico
4. **Ajuste**: Fatores de ajuste por tipo de sinal e nível de confluência

## IA/LLM

Integração com OpenAI GPT para:

1. **Análise Contextual**: Interpretação de sinais com contexto de mercado
2. **Avaliação de Trades**: Feedback para aprendizado contínuo
3. **Recomendações**: Sugestões de SL/TP baseadas em análise
4. **Identificação de Padrões**: MLLDetecção de padrões recorrentes

## API Endpoints

### Análise
- `POST /analyze/candle` - Analisar um candle
- `GET /signals/history` - Histórico de sinais

### Dados
- `POST /data/upload-csv` - Fazer upload de CSV
- `POST /data/api-stream` - Conectar a API externa

### Notificações
- `POST /notifications/configure` - Configurar canais
- `POST /notifications/test` - Testar notificações

### ML/IA
- `GET /ml/model-status` - Status do modelo
- `POST /ml/train` - Treinar modelo

### Sistema
- `GET /` - Informações da aplicação
- `GET /health` - Health check
- `GET /settings` - Configurações ativas

## Troubleshooting

### Erro: "Telegram não configurado"
- Verifique `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_IDS` no `.env`

### Erro: "Email não configurado"
- Configure `SENDGRID_API_KEY` e `EMAIL_TO_ADDRESSES`

### Erro: "LLM não configurado"
- Adicionar `OPENAI_API_KEY` para ativar análise com IA

### CSV não processa
- Verifique se tem colunas: timestamp, open, high, low, close, volume
- Formato de timestamp: YYYY-MM-DD HH:MM:SS

## Roadmap

- [ ] Interface Web Admin (dashboard)
- [ ] Streaming em tempo real via WebSocket
- [ ] Integração com mais brokers (native RTD)
- [ ] Backtesting engine
- [ ] Risk management automático
- [ ] Database (PostgreSQL) para histórico
- [ ] Mobile app (iOS/Android)
- [ ] Cache distribuído (Redis)
- [ ] Clustering de análises

## License

Proprietary - SMC Web App v2.3

## Suporte

Para suporte, entre em contato ou abra uma issue no repositório.

---

**SMC - Sistema de Monitoramento Contínuo de Mercado v2.3**
Desenvolvido com análise profissional e IA integrada.
