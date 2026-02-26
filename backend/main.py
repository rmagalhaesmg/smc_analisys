"""
Aplicação FastAPI Principal - SMC Web App
Integra todos os módulos: SMC, Notificações, Ingestão de Dados, IA/ML
"""
import asyncio
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

from app.config import settings
from app.modules import HFZModule, FBIModule, DTMModule, SDAModule, MTVModule
from app.notifications import notification_manager
from app.data_ingestion import data_ingestion_manager
from app.ai_ml import llm_analyzer, ml_engine, signal_refinement

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Web App robusto para análise SMC com IA/ML"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar módulos SMC
hfz = HFZModule()
fbi = FBIModule()
dtm = DTMModule()
sda = SDAModule()
mtv = MTVModule()


class SMCAnalyzer:
    """Analisador integrado SMC"""
    
    def __init__(self):
        self.buffer_candles: List[Dict] = []
        self.signals_history: List[Dict] = []
        self.mtv_cache: Dict = {}
    
    async def process_candle(self, candle: Dict) -> Dict:
        """
        Processa um candle completo com todos os módulos SMC
        """
        try:
            # Extrair dados do candle
            high = candle.get('high', 0)
            low = candle.get('low', 0)
            open_ = candle.get('open', 0)
            close = candle.get('close', 0)
            volume = candle.get('volume', 0)
            agg_buy = candle.get('aggression_buy', 0)
            agg_sell = candle.get('aggression_sell', 0)
            trades = candle.get('trades', 0)
            
            # Calcular True Range
            tr = max(
                high - low,
                abs(high - self.buffer_candles[-1]['close']) if self.buffer_candles else 0,
                abs(low - self.buffer_candles[-1]['close']) if self.buffer_candles else 0
            )
            
            # Adicionar ao buffer
            self.buffer_candles.append(candle)
            if len(self.buffer_candles) > 100:
                self.buffer_candles.pop(0)
            
            # Atualizar históricos
            hfz.update_history(agg_buy - agg_sell, trades/60, volume)
            fbi.update_history(high, low, volume)
            dtm.update_history(close, high, low, volume, trades/60)
            sda.update_history(close, high, low, volume, tr)
            mtv.update_history(close, high, low, tr, volume)
            
            # Executar análises
            hfz_result = hfz.analyze(
                agg_buy, agg_sell, trades, high, low, open_, close, 0.01, 0.01
            )
            
            fbi_result = fbi.analyze(close, high, low, open_, close, volume)
            
            dtm_result = dtm.analyze(
                volume, high, low, open_, close, hfz_result.hz_normalizado,
                hfz_result.tentativa_cont_alta, hfz_result.tentativa_cont_baixa
            )
            
            sda_result = sda.analyze(close, high, low, volume, tr)
            
            hora_int = int(candle.get('timestamp', '0800').replace(':', '')[-4:])
            mtv_result = mtv.analyze(
                sda_result.regime_mercado, hora_int,
                settings.SMC_DEFAULT_PARAMS['tipo_ativo'],
                settings.SMC_DEFAULT_PARAMS['tf_base_minutos'],
                0.5
            )
            
            # Gerar score final
            signal = self._generate_signal(
                hfz_result, fbi_result, dtm_result, sda_result, mtv_result,
                candle, close
            )
            
            # Aplicar refinamento com ML
            if ml_engine.model:
                adjustment = signal_refinement.get_score_adjustment(signal)
                signal['score'] *= adjustment
            
            # Análise com LLM se score significativo
            if signal['score'] > 0.6 and settings.OPENAI_API_KEY:
                llm_analysis = await llm_analyzer.analyze_signal({
                    **signal,
                    'details': self._format_signal_details(
                        hfz_result, fbi_result, dtm_result, sda_result, mtv_result
                    )
                })
                signal['llm_analysis'] = llm_analysis
            
            # Adicionar ao histórico e gerar alerta se necessário
            self.signals_history.append(signal)
            ml_engine.add_signal(signal)
            
            if signal['alert'] and signal['score'] > 0.5:
                await self._send_alert(signal)
            
            return signal
        
        except Exception as e:
            logger.error(f"Erro ao processar candle: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_signal(self, hfz, fbi, dtm, sda, mtv, candle, price) -> Dict:
        """Gera sinal consolidado de todos os módulos"""
        
        # Score consolidado
        score_final = (
            hfz.score_hfz * 0.40 +
            fbi.score_fbi * 0.20 +
            dtm.score_dtm * 0.20 +
            sda.score_sda * 0.10 +
            mtv.score_confluencia * 0.10
        )
        
        # Limitar score entre -1 e 1
        score_final = max(-1, min(1, score_final))
        
        # Determinar tipo de sinal
        if score_final > 0.6 and mtv.confluencia_forte:
            signal_type = 'buy_signal' if hfz.score_compra > hfz.score_venda else 'sell_signal'
            alert = True
        elif score_final < -0.6 and mtv.confluencia_forte:
            signal_type = 'sell_signal'
            alert = True
        elif abs(score_final) > 0.4:
            signal_type = 'neutral'
            alert = False
        else:
            signal_type = 'neutral'
            alert = False
        
        # Detectar avisos
        warnings = []
        if dtm.trap_flag:
            warnings.append(f"Armadilha detectada (intensidade: {dtm.trap_intensity:.2f})")
        if mtv.divergencia_confirmada:
            warnings.append("Divergência confirmada entre TFs")
        if sda.vol_normalizada > 2:
            warnings.append("Volatilidade extrema")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'candle_timestamp': candle.get('timestamp'),
            'type': signal_type,
            'price': price,
            'score': (score_final + 1) * 50,  # Converter para 0-100
            'alert': alert,
            'warnings': warnings,
            'regime': {
                '1': 'Tendência',
                '2': 'Lateral',
                '3': 'Transição'
            }.get(str(sda.regime_mercado), 'Desconhecido'),
            'confluence_level': mtv.confluencia_camada,
            'confluence_score': mtv.score_confluencia * 100,
            'renko_suggestion': mtv.renko_sugestao,
            'session': {
                1: 'Pré-Abertura',
                2: 'Principal',
                3: 'Tarde',
                4: 'Fechamento',
                0: 'Fora de Horário'
            }.get(mtv.sessao_atual, 'Desconhecido'),
            # Scores dos módulos
            'hfz_score': max(0, min(100, (hfz.score_hfz + 1) * 50)),
            'fbi_score': max(0, min(100, fbi.score_fbi * 100)),
            'dtm_score': max(0, min(100, dtm.score_dtm * 100)),
            'sda_score': max(0, min(100, sda.score_sda * 100)),
            'mtv_score': max(0, min(100, mtv.score_confluencia * 100)),
        }
    
    def _format_signal_details(self, hfz, fbi, dtm, sda, mtv) -> str:
        """Formata detalhes para análise LLM"""
        return f"""
        HFZ: Delta={hfz.delta_normalizado:.2f}, Hz={hfz.hz_normalizado:.2f}, Imbalance={hfz.imbalance_score:.2f}
        FBI: Zona proxima={fbi.zona_proxima}, Força={fbi.forca_zona:.2f}
        DTM: Trap={dtm.trap_flag}, Cont.={dtm.falha_continuidade}, Efic.={dtm.eficiencia_deslocamento:.2f}
        SDA: Regime={sda.regime_mercado}, Continuação={sda.prob_continuacao:.2f}
        MTV: Confluência={mtv.score_confluencia:.2f}, Camada={mtv.confluencia_camada}
        """
    
    async def _send_alert(self, signal: Dict) -> None:
        """Envia alertas para múltiplos canais"""
        alert_data = {
            'type': signal['type'],
            'timestamp': signal['timestamp'],
            'price': signal['price'],
            'score': signal['score'],
            'message': f"Score: {signal['score']:.0f} | Regime: {signal['regime']} | Confluência: {signal['confluence_level']}"
        }
        
        channels = ['telegram', 'email']
        if len(signal.get('warnings', [])) > 0:
            channels.append('whatsapp')  # Alertas críticos no WhatsApp
        
        await notification_manager.send_alert(alert_data, channels)


# Instância global do analisador
analyzer = SMCAnalyzer()


# ============================================================================
# ROTAS DA API
# ============================================================================

@app.get("/")
async def root():
    """Raiz da API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Verificar saúde da aplicação"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "hfz": "ok",
            "fbi": "ok",
            "dtm": "ok",
            "sda": "ok",
            "mtv": "ok"
        }
    }


@app.post("/analyze/candle")
async def analyze_candle(candle: Dict):
    """Analisa um candle individual"""
    result = await analyzer.process_candle(candle)
    return result


@app.post("/data/upload-csv")
async def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Faz upload e processa arquivo CSV"""
    try:
        # Salvar arquivo temporário
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Ingerir dados
        ingestion_result = await data_ingestion_manager.ingest_csv(temp_path)
        
        if ingestion_result['status'] == 'success':
            candles = ingestion_result['data']
            
            # Processar candles em background
            if background_tasks:
                background_tasks.add_task(
                    _process_candles_batch,
                    candles
                )
            
            return {
                'status': 'success',
                'candles_loaded': len(candles),
                'message': 'Candles carregados e sendo processados'
            }
        else:
            return JSONResponse(
                status_code=400,
                content=ingestion_result
            )
    
    except Exception as e:
        logger.error(f"Erro ao fazer upload CSV: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={'status': 'error', 'message': str(e)}
        )


@app.post("/data/api-stream")
async def api_stream(endpoint: str, params: Dict = None):
    """Conecta a uma API externa e processa dados em tempo real"""
    try:
        result = await data_ingestion_manager.ingest_api(endpoint, params or {})
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'status': 'error', 'message': str(e)}
        )


@app.post("/notifications/configure")
async def configure_notifications(config: Dict):
    """Configura canais de notificação"""
    try:
        # Atualizar configurações
        if 'telegram_token' in config:
            settings.TELEGRAM_BOT_TOKEN = config['telegram_token']
        
        if 'telegram_chat_ids' in config:
            # Converter lista em string com vírgula separada
            ids = config['telegram_chat_ids']
            if isinstance(ids, list):
                settings.TELEGRAM_CHAT_IDS = ",".join(str(id) for id in ids)
            else:
                settings.TELEGRAM_CHAT_IDS = str(ids)
        
        if 'email_to' in config:
            # Converter lista em string com vírgula separada
            emails = config['email_to']
            if isinstance(emails, list):
                settings.EMAIL_TO_ADDRESSES = ",".join(emails)
            else:
                settings.EMAIL_TO_ADDRESSES = str(emails)
        
        if 'sendgrid_key' in config:
            settings.SENDGRID_API_KEY = config['sendgrid_key']
        
        # WhatsApp
        if 'twilio_sid' in config:
            settings.TWILIO_ACCOUNT_SID = config['twilio_sid']
        
        if 'whatsapp_numbers' in config:
            # Converter lista em string com vírgula separada
            numbers = config['whatsapp_numbers']
            if isinstance(numbers, list):
                settings.WHATSAPP_NUMBERS = ",".join(numbers)
            else:
                settings.WHATSAPP_NUMBERS = str(numbers)
        
        return {
            'status': 'success',
            'message': 'Configurações de notificação atualizadas'
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'status': 'error', 'message': str(e)}
        )


@app.post("/notifications/test")
async def test_notifications(channels: List[str] = None):
    """Testa envio de notificações"""
    test_alert = {
        'type': 'test',
        'timestamp': datetime.now().isoformat(),
        'price': 100.00,
        'score': 75,
        'message': 'Teste de notificação SMC'
    }
    
    results = await notification_manager.send_alert(test_alert, channels)
    return results


@app.get("/signals/history")
async def get_signals_history(limit: int = 20):
    """Retorna histórico de sinais"""
    return {
        'count': len(analyzer.signals_history),
        'latest': analyzer.signals_history[-limit:] if analyzer.signals_history else []
    }


@app.get("/ml/model-status")
async def get_ml_model_status():
    """Retorna status do modelo ML"""
    return {
        'trained': ml_engine.model is not None,
        'signals_count': len(ml_engine.historical_signals),
        'outcomes_count': len(ml_engine.signal_outcomes),
        'feature_importance': ml_engine.get_feature_importance()
    }


@app.post("/ml/train")
async def train_ml_model():
    """Treina modelo ML com histórico"""
    result = ml_engine.train_model()
    return result


@app.get("/settings")
async def get_settings():
    """Retorna configurações ativas"""
    return {
        'app_name': settings.APP_NAME,
        'app_version': settings.APP_VERSION,
        'default_params': settings.SMC_DEFAULT_PARAMS,
        'notifications': {
            'telegram': bool(settings.TELEGRAM_BOT_TOKEN),
            'email': bool(settings.SENDGRID_API_KEY),
            'whatsapp': bool(settings.TWILIO_ACCOUNT_SID),
            'openai': bool(settings.OPENAI_API_KEY)
        }
    }


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

async def _process_candles_batch(candles: List[Dict]) -> None:
    """Processa lote de candles em background"""
    for candle in candles:
        try:
            await analyzer.process_candle(candle)
            await asyncio.sleep(0.01)  # Pequeno delay para não sobrecarregar
        except Exception as e:
            logger.error(f"Erro ao processar candle: {str(e)}")


@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a aplicação"""
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Treinar modelo ML se houver dados
    if len(ml_engine.historical_signals) > 10:
        await asyncio.to_thread(ml_engine.train_model)
    
    logger.info("Aplicação iniciada com sucesso")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
