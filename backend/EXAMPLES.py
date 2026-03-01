"""
EXEMPLOS PRÁTICOS - Código para usar a SMC Web App

Use estes exemplos para integrar o sistema em seus workflows.
"""

# ============================================================================
# EXEMPLO 1: Analisar um candle isolado
# ============================================================================

"""
Cenário: Você tem um DataFrame com OHLC e quer analisar cada linha
"""

import requests
import json
from datetime import datetime

def analyze_single_candle(timestamp, open, high, low, close, volume, trades=0):
    """
    Analisar um único candle via API
    
    Args:
        timestamp (str): "2024-02-26 09:30:00"
        open (float): Preço de abertura
        high (float): Máxima
        low (float): Mínima
        close (float): Fechamento
        volume (int): Volume total
        trades (int): Número de negócios
    
    Returns:
        dict: Resultado completo da análise
    """
    
    candle_data = {
        "timestamp": timestamp,
        "open": open,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
        "trades": trades,
        "aggression_buy": volume * 0.6,     # Estimado
        "aggression_sell": volume * 0.4     # Estimado
    }
    
    response = requests.post(
        "http://localhost:8000/analyze/candle",
        json=candle_data
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

# Uso:
result = analyze_single_candle(
    timestamp="2024-02-26 09:30:00",
    open=127850,
    high=128200,
    low=127700,
    close=128100,
    volume=1200000,
    trades=4850
)

if result:
    print(f"Score Final: {result['final_score']}")
    print(f"Recomendação: {result['recommendation']}")
    print(f"HFZ: {result['signals']['hfz_score']}")
    print(f"FBI: {result['signals']['fbi_score']}")
    print(f"Confluência: {result['signals']['confluencia']}")
    print(f"Análise LLM: {result['signals']['llm_analysis'][:100]}...")


# ============================================================================
# EXEMPLO 2: Processar DataFrame inteiro
# ============================================================================

"""
Cenário: Você tem um DataFrame com múltiplos candles do histórico
"""

import pandas as pd

def analyze_dataframe(df):
    """
    Analisar todos os candles de um DataFrame
    
    Args:
        df (pd.DataFrame): Colunas: timestamp, open, high, low, close, volume, trades
    
    Returns:
        pd.DataFrame: DataFrame original + colunas de análise
    """
    
    results = []
    
    for idx, row in df.iterrows():
        result = analyze_single_candle(
            timestamp=str(row['timestamp']),
            open=float(row['open']),
            high=float(row['high']),
            low=float(row['low']),
            close=float(row['close']),
            volume=int(row['volume']),
            trades=int(row.get('trades', 0))
        )
        
        if result:
            # Extrair dados do resultado
            result_flat = {
                'timestamp': row['timestamp'],
                'final_score': result['final_score'],
                'recommendation': result['recommendation'],
                'hfz_score': result['signals']['hfz_score'],
                'fbi_score': result['signals']['fbi_score'],
                'dtm_score': result['signals']['dtm_score'],
                'sda_score': result['signals']['sda_score'],
                'mtv_score': result['signals']['mtv_score'],
                'confluencia': result['signals']['confluencia'],
                'mlm_refined': result['signals']['mlm_refined_score']
            }
            results.append(result_flat)
    
    return pd.DataFrame(results)

# Uso:
df_historico = pd.read_csv('example_data.csv')
df_result = analyze_dataframe(df_historico)
print(df_result)

# Salvar resultados
df_result.to_csv('analise_resultados.csv', index=False)


# ============================================================================
# EXEMPLO 3: Upload de arquivo CSV
# ============================================================================

"""
Cenário: Você tem um arquivo CSV com candles e quer processar em background
"""

def upload_csv(filepath):
    """
    Upload e processamento de arquivo CSV
    
    Args:
        filepath (str): Caminho para arquivo CSV
    
    Returns:
        dict: Status do processamento
    """
    
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            "http://localhost:8000/data/upload-csv",
            files=files
        )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

# Uso:
status = upload_csv("dados_fevereiro.csv")
if status:
    print(f"Total de candles: {status['total_candles']}")
    print(f"Sinais gerados: {status['generated_signals']}")
    print(f"Score médio: {status['avg_score']:.1f}")
    print(f"Melhor sinal: {status['top_signal']}")


# ============================================================================
# EXEMPLO 4: Configurar notificações (Telegram)
# ============================================================================

"""
Cenário: Você quer receber alertas no Telegram
"""

def setup_telegram_notifications(bot_token, chat_ids):
    """
    Configurar notificações via Telegram
    
    Args:
        bot_token (str): Token obtido de @BotFather
        chat_ids (list[str]): Lista de IDs de chat para receber alertas
    """
    
    config_data = {
        "telegram": {
            "enabled": True,
            "bot_token": bot_token,
            "chat_ids": chat_ids
        },
        "email": {
            "enabled": False
        },
        "whatsapp": {
            "enabled": False
        },
        "alert_thresholds": {
            "min_score_for_alert": 65,
            "alert_on_trap_detected": True,
            "alert_on_divergence": True,
            "alert_on_exhaustion": True
        }
    }
    
    response = requests.post(
        "http://localhost:8000/notifications/configure",
        json=config_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Telegram configurado: {result['telegram_configured']}")
        
        # Testar notificação
        test_response = requests.post(
            "http://localhost:8000/notifications/test"
        )
        if test_response.status_code == 200:
            test_result = test_response.json()
            print(f"✓ Teste enviado: {test_result['telegram']['status']}")
        return result
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return None

# Uso:
setup_telegram_notifications(
    bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    chat_ids=["987654321", "123456789"]
)


# ============================================================================
# EXEMPLO 5: Monitorar histórico de sinais
# ============================================================================

"""
Cenário: Você quer acompanhar os sinais gerados
"""

def get_recent_signals(limit=20, min_score=70):
    """
    Obter sinais recentes filtrados
    
    Args:
        limit (int): Número máximo de sinais
        min_score (int): Score mínimo para filtro
    
    Returns:
        list[dict]: Lista de sinais
    """
    
    response = requests.get(
        "http://localhost:8000/signals/history",
        params={
            "limit": limit,
            "min_score": min_score
        }
    )
    
    if response.status_code == 200:
        signals = response.json()
        
        # Formatar para exibição
        for signal in signals:
            print(f"\n{'='*60}")
            print(f"Timestamp: {signal['timestamp']}")
            print(f"Score: {signal['final_score']} → {signal['recommendation']}")
            print(f"Confluência: {'⭐' * signal['signals']['confluencia']}")
            print(f"Análise: {signal['signals']['llm_analysis'][:150]}...")
            
            if 'outcome' in signal and signal['outcome']['final']:
                result = "✓ WIN" if signal['outcome']['result'] == "WIN" else "✗ LOSS"
                print(f"Resultado: {result} ({signal['outcome']['profit_percent']:.2f}%)")
        
        return signals
    else:
        print(f"Erro {response.status_code}: {response.text}")
        return []

# Uso:
signals = get_recent_signals(limit=10, min_score=70)


# ============================================================================
# EXEMPLO 6: Treinar modelo ML
# ============================================================================

"""
Cenário: Você tem histórico de sinais e quer treinar o modelo
"""

def train_ml_model(min_samples=50):
    """
    Treinar modelo de ML para refinamento de scores
    """
    
    # Iniciar treinamento (assíncrono)
    response = requests.post(
        "http://localhost:8000/ml/train",
        json={
            "min_samples": min_samples,
            "test_split": 0.2,
            "force_retrain": True
        }
    )
    
    if response.status_code == 200:
        job = response.json()
        print(f"✓ Treinamento iniciado (Job: {job['job_id']})")
        print(f"  Duração estimada: {job['estimated_duration_seconds']}s")
        
        # Aguardar alguns segundos e verificar status
        import time
        time.sleep(job['estimated_duration_seconds'] + 5)
        
        # Obter métricas do modelo treinado
        status_response = requests.get(
            "http://localhost:8000/ml/model-status"
        )
        
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"\n✓ Modelo treinado com sucesso!")
            print(f"  R² Score: {status['performance_metrics']['r2_score']:.3f}")
            print(f"  MAE: {status['performance_metrics']['mean_absolute_error']:.2f}")
            print(f"\nImportância dos features:")
            for feature, importance in status['feature_importance'].items():
                bar = '█' * int(importance * 50)
                print(f"  {feature:15} {bar} {importance:.2%}")
            
            return status

# Uso:
train_ml_model(min_samples=50)


# ============================================================================
# EXEMPLO 7: Integração contínua (Loop)
# ============================================================================

"""
Cenário: Você quer processar candles em tempo real continuamente
"""

async def continuous_analysis_loop(api_url, symbol, interval_seconds=5):
    """
    Loop contínuo de análise (use com aiohttp para melhor performance)
    """
    
    import aiohttp
    import asyncio
    from datetime import datetime
    
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                # Buscar dado mais recente (sua API)
                async with session.get(api_url) as resp:
                    data = await resp.json()
                
                # Preparar candle
                candle = {
                    "timestamp": data['timestamp'],
                    "open": data['open'],
                    "high": data['high'],
                    "low": data['low'],
                    "close": data['close'],
                    "volume": data['volume'],
                    "trades": data.get('trades', 0)
                }
                
                # Analisar
                async with session.post(
                    "http://localhost:8000/analyze/candle",
                    json=candle
                ) as resp:
                    result = await resp.json()
                
                # Processar resultado
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                      f"{symbol} → {result['final_score']} "
                      f"({result['recommendation']})")
                
                if result['recommendation'] in ['BUY', 'SELL']:
                    print(f"  ⚠️  ALERTA: {result['recommendation']}")
                    print(f"  SL: {result['suggested_sl']}")
                    print(f"  TP: {result['suggested_tp']}")
                
                # Aguardar próximo intervalo
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                print(f"Erro: {e}")
                await asyncio.sleep(interval_seconds)

# Uso (em um ambiente async):
# asyncio.run(continuous_analysis_loop(
#     api_url="https://seu-broker.com/api/candle/WIN@H25",
#     symbol="WIN@H25",
#     interval_seconds=5
# ))


# ============================================================================
# EXEMPLO 8: Dashboard simplificado
# ============================================================================

"""
Cenário: Você quer criar um painel simples de monitoramento
"""

def print_dashboard():
    """
    Exibir dashboard com informações do sistema
    """
    
    # Obter status do sistema
    response = requests.get("http://localhost:8000/health")
    health = response.json()
    
    # Obter sinais recentes
    response = requests.get("http://localhost:8000/signals/history?limit=5&min_score=70")
    signals = response.json()
    
    # Obter status ML
    response = requests.get("http://localhost:8000/ml/model-status")
    ml_status = response.json()
    
    # Limpar tela e exibir
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║              SMC WEB APP - DASHBOARD                           ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Status do servidor
    status_color = "🟢" if health['status'] == 'healthy' else "🔴"
    print(f"{status_color} Status do Servidor: {health['status']}")
    print(f"   Uptime: {health['uptime_seconds']}s")
    print(f"   Versão: {health['version']}")
    
    # Sinais recentes
    print(f"\n📊 Últimos Sinais (Score > 70):")
    if signals:
        for sig in signals[:3]:
            icon = "📈" if sig['recommendation'] == 'BUY' else "📉"
            print(f"   {icon} {sig['timestamp']} → Score: {sig['final_score']} | {sig['recommendation']}")
    else:
        print("   Nenhum sinal relevante nos últimos sinais")
    
    # ML Status
    print(f"\n🤖 Machine Learning:")
    if ml_status['model_trained']:
        print(f"   ✓ Modelo treinado")
        print(f"   R² Score: {ml_status['performance_metrics']['r2_score']:.3f}")
        print(f"   Samples: {ml_status['training_samples']}")
    else:
        print(f"   ❌ Modelo não treinado ainda")
    
    print("\n" + "="*60)

# Uso:
print_dashboard()

# Executar periodicamente:
# import schedule
# schedule.every(5).seconds.do(print_dashboard)
# while True:
#     schedule.run_pending()


print("Veja exemplos acima para usar a API da SMC Web App")
