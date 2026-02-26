"""
API ENDPOINTS - Referência Rápida
SMC Web App - Análise com Machine Learning e Notificações

Base URL: http://localhost:8000
Documentação Interativa: http://localhost:8000/docs (Swagger UI)
"""

# ============================================================================
# ANÁLISE - Endpoints principais
# ============================================================================

"""
1. POST /analyze/candle
   Descrição: Analisar um único candle e gerar sinal
   
   Entrada (JSON):
   {
       "timestamp": "2024-02-26 09:30:00",
       "open": 127850.00,
       "high": 128200.00,
       "low": 127700.00,
       "close": 128100.00,
       "volume": 1200000,
       "trades": 4850,
       "aggression_buy": 750000,      # Opcional
       "aggression_sell": 450000      # Opcional
   }
   
   Saída (JSON):
   {
       "timestamp": "2024-02-26 09:30:00",
       "final_score": 72,              # 0-100
       "signals": {
           "hfz_score": 65,            # Microestrutura
           "fbi_score": 58,            # Zonas institucionais
           "dtm_score": 80,            # Armadilhas
           "sda_score": 70,            # Regime
           "mtv_score": 75,            # Multi-timeframe
           "confluencia": 3,           # 0=nenhuma, 1=estrutural, 2=tendência, 3=total
           "mlm_refined_score": 74,    # Ajustado por ML
           "llm_analysis": "Sinal forte de compra..."
       },
       "recommendation": "BUY",        # BUY, SELL, HOLD, WAIT
       "alerts_sent": ["telegram", "email"],
       "suggested_sl": 127200.00,
       "suggested_tp": 129100.00,
       "reasoning": "Confluência de 3 timeframes, HFZ agressivo, FBI em zona forte"
   }
   
   cURL:
   curl -X POST http://localhost:8000/analyze/candle \\
     -H "Content-Type: application/json" \\
     -d @- << 'EOF'
   {
     "timestamp": "2024-02-26 09:30:00",
     "open": 127850, "high": 128200, "low": 127700,
     "close": 128100, "volume": 1200000, "trades": 4850
   }
   EOF
"""

# ============================================================================
# DADOS - Ingestão múltiplas fontes
# ============================================================================

"""
2. POST /data/upload-csv
   Descrição: Upload de arquivo CSV e processamento em background
   
   Entrada: arquivo CSV multipart
   Formato esperado:
     timestamp,open,high,low,close,volume,trades,aggression_buy,aggression_sell
     2024-02-26 09:30:00,127850,128200,127700,128100,1200000,4850,750000,450000
   
   Saída (JSON):
   {
       "file_name": "dados_fevereiro.csv",
       "total_candles": 125,
       "processed": 125,
       "generated_signals": 23,
       "avg_score": 65.4,
       "top_signal": {
           "timestamp": "2024-02-26 14:15:00",
           "score": 89,
           "recommendation": "BUY"
       },
       "processing_time_seconds": 12.5
   }
   
   PowerShell:
   $filePath = "C:\\seu_arquivo.csv"
   $url = "http://localhost:8000/data/upload-csv"
   $file = Get-Item $filePath
   
   $curl = curl.exe -X POST \\
     -F "file=@$filePath" \\
     $url
"""

"""
3. POST /data/api-stream
   Descrição: Conectar a uma API externa para stream de dados
   
   Entrada (JSON):
   {
       "api_url": "https://api.seu-broker.com/candles",
       "symbol": "WIN@H25",
       "timeframe": 5,
       "api_key": "sua_chave_api",
       "update_interval_seconds": 5
   }
   
   Saída (JSON):
   {
       "connection_id": "stream-abc123",
       "symbol": "WIN@H25",
       "status": "connected",
       "data_points_received": 142,
       "last_update": "2024-02-26 14:35:00",
       "connected_since": "2024-02-26 09:00:00"
   }
   
   Parar stream (necessário invocar separadamente):
   DELETE /data/api-stream/stream-abc123
"""

# ============================================================================
# NOTIFICAÇÕES - Configuração e teste
# ============================================================================

"""
4. POST /notifications/configure
   Descrição: Configurar canais de notificação em runtime
   
   Entrada (JSON):
   {
       "telegram": {
           "enabled": true,
           "bot_token": "123456:ABC...",
           "chat_ids": ["123456789", "987654321"]
       },
       "email": {
           "enabled": true,
           "api_key": "SG.xxx...",
           "from_address": "alerts@seu-dominio.com",
           "recipients": ["seu@email.com"]
       },
       "whatsapp": {
           "enabled": true,
           "account_sid": "ACxxx...",
           "auth_token": "xxx...",
           "from_number": "+5511999999999",
           "to_numbers": ["+5511988888888"]
       },
       "alert_thresholds": {
           "min_score_for_alert": 65,
           "alert_on_trap_detected": true,
           "alert_on_divergence": true,
           "alert_on_exhaustion": true
       }
   }
   
   Saída (JSON):
   {
       "telegram_configured": true,
       "email_configured": true,
       "whatsapp_configured": false,
       "test_status": "Aguardando teste",
       "last_updated": "2024-02-26 14:30:00"
   }
"""

"""
5. POST /notifications/test
   Descrição: Enviar mensagem de teste a todos os canais configurados
   
   Entrada: Vazia (usa configuração atual)
   
   Saída (JSON):
   {
       "telegram": {
           "status": "sent",
           "message_id": "12345",
           "timestamp": "2024-02-26 14:31:00"
       },
       "email": {
           "status": "sent",
           "message_id": "msg_abc123",
           "timestamp": "2024-02-26 14:31:01"
       },
       "whatsapp": {
           "status": "not_configured",
           "error": null
       }
   }
   
   cURL:
   curl -X POST http://localhost:8000/notifications/test
"""

# ============================================================================
# SINAIS - Histórico e análise
# ============================================================================

"""
6. GET /signals/history
   Descrição: Recuperar histórico de sinais gerados
   
   Parâmetros Query:
   - limit (padrão: 20): Número máximo de sinais a retornar
   - offset (padrão: 0): Paginação
   - min_score (padrão: 0): Filtrar por score mínimo
   - recommendation (padrão: all): Filtrar por BUY/SELL/HOLD/WAIT
   
   Exemplo: /signals/history?limit=10&min_score=70&recommendation=BUY
   
   Saída (JSON array):
   [
       {
           "id": "sig_001",
           "timestamp": "2024-02-26 14:30:00",
           "final_score": 85,
           "recommendation": "BUY",
           "signals": {
               "hfz_score": 80,
               "fbi_score": 75,
               "dtm_score": 90,
               "sda_score": 85,
               "mtv_score": 88,
               "confluencia": 3,
               "mlm_refined_score": 86
           },
           "alerts_sent": ["telegram", "email"],
           "llm_analysis": "Movimento de breakout confirmado com confluência...",
           "outcome": {
               "final": true,
               "result": "WIN",
               "profit_pips": 45,
               "profit_percent": 3.2
           },
           "created_at": "2024-02-26 14:30:00",
           "updated_at": "2024-02-26 15:15:00"
       },
       ...
   ]
   
   cURL:
   curl "http://localhost:8000/signals/history?limit=10&min_score=70"
"""

# ============================================================================
# MACHINE LEARNING - Treinamento e status
# ============================================================================

"""
7. GET /ml/model-status
   Descrição: Verificar status e métricas do modelo ML
   
   Entrada: Vazia
   
   Saída (JSON):
   {
       "model_trained": true,
       "training_date": "2024-02-25 10:30:00",
       "training_samples": 156,
       "model_type": "RandomForest",
       "feature_importance": {
           "hfz_score": 0.28,       # Impacto de cada métrica
           "mtv_score": 0.25,
           "confluencia": 0.20,
           "fbi_score": 0.15,
           "dtm_score": 0.08,
           "volume_trend": 0.04
       },
       "performance_metrics": {
           "mean_absolute_error": 4.3,
           "r2_score": 0.78,
           "cross_validation_score": 0.76
       },
       "adaptive_refinement": {
           "enabled": true,
           "signals_analyzed": 156,
           "win_rate_by_score": {
               "20-40": 0.35,
               "40-60": 0.52,
               "60-80": 0.78,
               "80-100": 0.92
           },
           "current_multiplier": 1.05  # Ajuste aplicado aos scores
       }
   }
   
   cURL:
   curl http://localhost:8000/ml/model-status
"""

"""
8. POST /ml/train
   Descrição: Treinar ou retreinar modelo com dados mais recentes
   
   Entrada (JSON):
   {
       "min_samples": 50,           # Mínimo de sinais para treino
       "test_split": 0.2,           # 20% para validação
       "force_retrain": false       # Ignorar se modelo recente existe
   }
   
   Saída (JSON):
   {
       "status": "training",
       "job_id": "train_xyz789",
       "started_at": "2024-02-26 14:35:00",
       "estimated_duration_seconds": 45,
       "messages": ["Carregando dados...", "Extraindo features...", "Treinando RandomForest..."]
   }
   
   Depois, usar /ml/model-status para ver resultados
"""

# ============================================================================
# CONFIGURAÇÃO - Visualizar configurações ativas
# ============================================================================

"""
9. GET /settings
   Descrição: Visualizar todas as configurações ativas
   
   Entrada: Vazia
   
   Saída (JSON):
   {
       "smc_parameters": {
           "ativo_type": 1,              # 1=WIN, 2=WDO, 3=NASDAQ, etc
           "base_timeframe_minutes": 5,
           "operation_mode": 2,          # 1=Conservador, 2=Normal, 3=Agressivo
           "alerting_enabled": true,
           "ml_refinement_enabled": true,
           "llm_analysis_enabled": true,
           "min_score_for_alert": 65
       },
       "mtv_parameters": {
           "weight_semanal": 0.45,
           "weight_diario": 0.30,
           "weight_lento": 0.15,
           "weight_medio": 0.07,
           "weight_rapido": 0.03,
           "renko_blending": {
               "atr_percent": 0.6,
               "anchor_percent": 0.4
           }
       },
       "notification_channels": {
           "telegram": {
               "enabled": true,
               "configured": true,
               "recipients": 2
           },
           "email": {
               "enabled": false,
               "configured": false
           },
           "whatsapp": {
               "enabled": false,
               "configured": false
           }
       },
       "data_sources": {
           "csv_import": "enabled",
           "api_stream": "enabled",
           "rtd_connection": "available",
           "dll_integration": "available"
       },
       "last_updated": "2024-02-26 14:00:00"
   }
   
   cURL:
   curl http://localhost:8000/settings
"""

# ============================================================================
# SISTEMA - Health e informações
# ============================================================================

"""
10. GET /health
    Descrição: Health check do servidor
    
    Saída (JSON):
    {
        "status": "healthy",
        "timestamp": "2024-02-26 14:36:30",
        "uptime_seconds": 3600,
        "version": "1.0.0",
        "components": {
            "database": "ok",
            "telegram_api": "ok",
            "openai_api": "ok",
            "ml_model": "loaded"
        }
    }
    
    cURL:
    curl http://localhost:8000/health
"""

"""
11. GET /
    Descrição: Informações gerais da aplicação
    
    Saída (JSON):
    {
        "name": "SMC Web App v1.0",
        "description": "Análise SMC com IA, ML e Notificações Multi-Canal",
        "version": "1.0.0",
        "modules": ["HFZ", "FBI", "DTM", "SDA", "MTV"],
        "features": [
            "Multi-channel notifications",
            "Machine Learning refinement",
            "LLM analysis (OpenAI)",
            "CSV/API/RTD/DLL data ingestion",
            "Real-time signal generation"
        ],
        "endpoints_count": 11,
        "documentation_url": "http://localhost:8000/docs",
        "repository": "internal"
    }
    
    cURL:
    curl http://localhost:8000/
"""

# ============================================================================
# EXEMPLOS DE USO COMPLETO
# ============================================================================

"""
FLUXO 1: Upload CSV e Análise Automática
1. POST /data/upload-csv (seu_arquivo.csv)
2. Sistema processa automaticamente cada candle
3. Monitore sinais em: GET /signals/history

FLUXO 2: Stream em Tempo Real + Notificações
1. POST /notifications/configure (Telegram + Email)
2. POST /data/api-stream (conectar API externa)
3. Sistema analisa candles conforme chegam
4. Alertas enviados quando score > 65

FLUXO 3: Machine Learning com Histórico
1. Coletar ~50+ sinais com outcomes
2. POST /ml/train
3. GET /ml/model-status → verificar métricas
4. Forward: novos scores refinados automaticamente

FLUXO 4: Desenvolvimento e Manual
1. POST /analyze/candle (um candle por vez)
2. Receber score completo + análise LLM
3. Útil para debugging e testes
"""

# ============================================================================
# CÓDIGOS DE RESPOSTA HTTP
# ============================================================================

"""
200 OK: Requisição bem-sucedida
201 Created: Recurso criado
202 Accepted: Processamento assíncrono iniciado
400 Bad Request: Parâmetros inválidos
401 Unauthorized: Credenciais faltando
403 Forbidden: Sem permissão
404 Not Found: Recurso não encontrado
422 Unprocessable Entity: Erro de validação (veja detalhes em 'detail')
429 Too Many Requests: Rate limit excedido
500 Internal Server Error: Erro do servidor
503 Service Unavailable: Serviço temporariamente indisponível
"""

print(__doc__)
