"""
SMC SaaS - Backend Principal
FastAPI + todos os módulos: Core Engine, Alerts, AI, Auth, Payments
Deploy: Railway (ou qualquer servidor com Python 3.11+)
"""

import os
import logging
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Depends, HTTPException, Header, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# new structure imports
from app.auth.router import router as auth_router
from app.middleware.subscription_guard import SubscriptionGuard

# make sure SQLAlchemy knows about the tables
from app.auth import models  # noqa: F401
from app.models import signal  # noqa: F401

# ============================================================
# IMPORTAR MÓDULOS SMC
# ============================================================
from core_engine import SMCCoreEngine, Bar
from alert_engine import AlertEngine, AlertConfig, TelegramConfig, EmailConfig, WhatsAppConfig
from ai_engine import AIEngine, AIConfig
from auth_engine import AuthEngine, AuthConfig
from payment_engine import PaymentEngine, PaymentConfig

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("smc.main")

# ============================================================
# INSTÂNCIAS GLOBAIS (inicializadas no startup)
# ============================================================
smc_engine: SMCCoreEngine = None
alert_engine: AlertEngine = None
ai_engine: AIEngine = None
auth_engine: AuthEngine = None
payment_engine: PaymentEngine = None

# Guarda o último resultado processado (por ativo)
ultimo_resultado = {}


# ============================================================
# STARTUP / SHUTDOWN
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global smc_engine, alert_engine, ai_engine, auth_engine, payment_engine

    logger.info("🚀 Iniciando SMC SaaS Backend...")
    # record start time for health checks
    app.state.start_time = datetime.now(timezone.utc)

    # Core Engine (WIN, 5min, modo profissional)
    smc_engine = SMCCoreEngine(
        tf_base_minutos=int(os.getenv("TF_BASE", "5")),
        modo_operacao=int(os.getenv("MODO_OPERACAO", "2")),
        tipo_ativo=int(os.getenv("TIPO_ATIVO", "1")),
    )

    # Alert Engine
    alert_config = AlertConfig(
        telegram=TelegramConfig(
            token=os.getenv("TELEGRAM_TOKEN", ""),
            chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            enabled=bool(os.getenv("TELEGRAM_TOKEN", ""))
        ),
        email=EmailConfig(
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            username=os.getenv("SMTP_USER", ""),
            password=os.getenv("SMTP_PASS", ""),
            from_addr=os.getenv("SMTP_USER", ""),
            to_addr=os.getenv("ALERT_EMAIL", ""),
            sendgrid_key=os.getenv("SENDGRID_KEY", ""),
            enabled=bool(os.getenv("SMTP_USER", "") or os.getenv("SENDGRID_KEY", ""))
        ),
        whatsapp=WhatsAppConfig(
            twilio_sid=os.getenv("TWILIO_SID", ""),
            twilio_token=os.getenv("TWILIO_TOKEN", ""),
            twilio_from=os.getenv("TWILIO_FROM", ""),
            twilio_to=os.getenv("TWILIO_TO", ""),
            enabled=bool(os.getenv("TWILIO_SID", ""))
        ),
        min_score_alerta=float(os.getenv("MIN_SCORE_ALERTA", "55")),
        min_qualidade_alerta=int(os.getenv("MIN_QUALIDADE_ALERTA", "4")),
        rate_limit_segundos=int(os.getenv("RATE_LIMIT_ALERTAS", "60")),
        modo_simulacao=os.getenv("ALERT_SIM", "true").lower() == "true"
    )
    alert_engine = AlertEngine(alert_config, ativo=os.getenv("ATIVO", "WIN"))

    # AI Engine
    ai_config = AIConfig(
        provider=os.getenv("AI_PROVIDER", "openai"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        modo_simulacao=not bool(os.getenv("OPENAI_API_KEY", "") or os.getenv("GEMINI_API_KEY", ""))
    )
    ai_engine = AIEngine(ai_config)

    # Auth Engine
    auth_config = AuthConfig(
        jwt_secret=os.getenv("JWT_SECRET", "TROQUE_EM_PRODUCAO_256BITS"),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=os.getenv("SMTP_USER", ""),
        smtp_pass=os.getenv("SMTP_PASS", ""),
        frontend_url=os.getenv("FRONTEND_URL", "http://localhost:3000"),
    )
    auth_engine = AuthEngine(auth_config)
    # cria usuário padrão no engine em memória (legacy)
    try:
        if not auth_engine.users:
            auth_engine.register_user("admin", "admin", "admin@example.com")
            logger.info("🚩 usuário padrão 'admin' criado (senha admin) [legacy]")
    except Exception:
        pass

    # make sure SQLite directory exists when using local file
    from app.database import SessionLocal, engine, Base, DATABASE_URL
    from app.auth.models import User, Subscription
    from app.models.signal import Signal

    if DATABASE_URL.startswith("sqlite"):
        path = DATABASE_URL.replace("sqlite://", "")
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            try:
                os.makedirs(dirpath, exist_ok=True)
                logger.info(f"✅ Criado diretório de banco de dados: {dirpath}")
            except Exception as e:
                logger.warning(f"falha ao criar diretório de banco de dados {dirpath}: {e}")

    Base.metadata.create_all(bind=engine)

    # then ensure a default SQL user exists
    from passlib.context import CryptContext
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = SessionLocal()
    try:
        if not db.query(User).first():
            default = User(
                email="admin@sql.local",
                password_hash=pwd_ctx.hash("admin"),
                is_active=True
            )
            db.add(default)
            db.flush()
            # create an active subscription so SubscriptionGuard lets the admin through
            admin_sub = Subscription(
                user_id=default.id,
                plan="admin",
                status="active",
            )
            db.add(admin_sub)
            db.commit()
            logger.info("🚩 default SQL user 'admin@sql.local' created with active subscription (senha admin)")
    except Exception:
        db.rollback()
    finally:
        db.close()

    # Payment Engine
    pay_config = PaymentConfig(
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
        stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", ""),
        mp_access_token=os.getenv("MP_ACCESS_TOKEN", ""),
        mp_notification_url=os.getenv("BACKEND_URL", "http://localhost:8000"),
        modo_simulacao=os.getenv("PAYMENT_SIM", "true").lower() == "true"
    )
    payment_engine = PaymentEngine(pay_config)
    # expose for router helpers
    app.state.payment_engine = payment_engine

    logger.info("✅ Todos os módulos inicializados")
    yield
    logger.info("👋 Backend encerrado")


# ============================================================
# APP FASTAPI
# ============================================================
app = FastAPI(
    title="SMC SaaS API",
    description="API do Sistema SMC MTV V2.3",
    version="1.0.0",
    lifespan=lifespan,
)

# simple health check -- public
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "uptime_seconds": (datetime.now(timezone.utc) - app.state.start_time).total_seconds(),
        "version": "1.0.0"
    }

# mount auth routes and global subscription guard
app.include_router(auth_router, prefix="/auth")          # auth endpoints are now served by app/auth/router.py
app.add_middleware(SubscriptionGuard)                      # blocks access when subscription inactive

# include analysis endpoints under /analysis (guard applied automatically)
from app.routes.analysis import router as analysis_router
from app.routes.stats import router as stats_router
from app.billing.router import router as billing_router
from app.billing.webhooks import router as webhook_router

# WebSocket endpoints
from app.websocket.routes import router as ws_router

app.include_router(ws_router)

app.include_router(analysis_router, prefix="/analysis")
app.include_router(stats_router, prefix="/analysis")

# billing
app.include_router(billing_router, prefix="/billing")
app.include_router(webhook_router, prefix="/billing/webhook")

# ingestion endpoints (CSV upload/backtest)
from app.ingestion.csv_upload import router as ingestion_router
app.include_router(ingestion_router, prefix="/ingestion")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # em prod: troque por seus domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DEPENDÊNCIA: AUTENTICAÇÃO
# ============================================================
def get_current_user(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    user = auth_engine.verificar_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return user


def get_user_com_plano(user=Depends(get_current_user)):
    """Exige assinatura ativa para acessar dados de sinal."""
    status = payment_engine.status_assinatura(user["id"])
    if not status["ativa"] and user.get("plano") == "free":
        raise HTTPException(status_code=403, detail="Assinatura necessária")
    return user


# ============================================================
# MODELS PYDANTIC
# ============================================================
class BarInput(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float
    volume_compra: float
    volume_venda: float
    trades: int
    true_range: float
    timestamp_hhmm: int
    tick_minimo: float = 5.0
    ativo: str = "WIN"

class RegisterBody(BaseModel):
    email: str
    password: str
    nome: str = ""

class LoginBody(BaseModel):
    email: str
    password: str

class ChatBody(BaseModel):
    pergunta: str
    ativo: str = "WIN"

class PlanoBody(BaseModel):
    plano: str  # "mensal", "semestral", "anual"
    gateway: str = "stripe"  # "stripe" ou "mercadopago"


# ============================================================
# ROTAS PÚBLICAS
# ============================================================
@app.get("/")
def root():
    return {
        "status": "online",
        "app": "SMC SaaS API",
        "versao": "1.0.0",
        "timestamp": datetime.now(tz=timezone.utc).isoformat()
    }

@app.get("/api/status")
def api_status():
    return {
        "engine": "online",
        "barras_processadas": smc_engine.contador_barras if smc_engine else 0,
        "alertas_enviados": alert_engine.get_stats()["total_enviados"] if alert_engine else 0,
        "ai_consultas": ai_engine.get_stats()["total_consultas"] if ai_engine else 0,
        "timestamp": datetime.now(tz=timezone.utc).isoformat()
    }


# ============================================================
# ROTAS AUTH (LEGADO / temporário)
# ============================================================
# these endpoints are maintained for backward compatibility while the
# new `app/auth` package gets rolling; eventually they can be removed
# once the SQLAlchemy/jwt implementation is fully in place.
#
# A lean router is now provided by app/auth/router.py and has been
# mounted earlier in the file with `app.include_router(auth_router)`.

@app.post("/auth/register")
def register(body: RegisterBody):
    # legacy implementation (keep for now)
    try:
        result = auth_engine.registrar(body.email, body.password, body.nome)
        return {"mensagem": "Cadastro realizado! Verifique seu e-mail.",
                "email": result["email"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(body: LoginBody):
    try:
        return auth_engine.login(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# refresh / verify-email / forgot-password / reset-password / me remain
# untouched below – they are still used by the frontend until migration



# ============================================================
# ROTAS DE SINAIS (requer autenticação)
# ============================================================
@app.post("/api/processar-barra")
async def processar_barra(
    bar_input: BarInput,
    background_tasks: BackgroundTasks,
    user=Depends(get_user_com_plano)
):
    """Processa uma barra e retorna o resultado SMC completo."""
    bar = Bar(
        open=bar_input.open, high=bar_input.high,
        low=bar_input.low, close=bar_input.close,
        volume=bar_input.volume, volume_compra=bar_input.volume_compra,
        volume_venda=bar_input.volume_venda, trades=bar_input.trades,
        true_range=bar_input.true_range, timestamp_hhmm=bar_input.timestamp_hhmm,
        tick_minimo=bar_input.tick_minimo
    )

    resultado = smc_engine.process(bar)

    if resultado is None:
        return {
            "aquecendo": True,
            "barras_restantes": max(0, 60 - smc_engine.contador_barras),
            "mensagem": "Engine em aquecimento (60 barras necessárias)"
        }

    # Salva último resultado para consultas
    ultimo_resultado[bar_input.ativo] = resultado

    # Dispara alertas em background
    background_tasks.add_task(alert_engine.processar, resultado)

    return _resultado_para_dict(resultado)


@app.get("/api/ultimo-sinal/{ativo}")
def ultimo_sinal(ativo: str = "WIN", user=Depends(get_user_com_plano)):
    """Retorna o último resultado processado para o ativo."""
    r = ultimo_resultado.get(ativo)
    if not r:
        return {"mensagem": f"Sem dados para {ativo} ainda"}
    return _resultado_para_dict(r)

@app.get("/api/alertas/log")
def log_alertas(user=Depends(get_current_user)):
    return {"alertas": alert_engine.get_log()[-20:]}

@app.get("/api/alertas/stats")
def stats_alertas(user=Depends(get_current_user)):
    return alert_engine.get_stats()


# ============================================================
# ROTAS AI
# ============================================================
@app.get("/api/ai/interpretar/{ativo}")
async def ai_interpretar(ativo: str = "WIN", user=Depends(get_user_com_plano)):
    r = ultimo_resultado.get(ativo)
    if not r:
        raise HTTPException(404, f"Sem dados para {ativo}")
    texto = await ai_engine.interpretar(r, ativo)
    return {"interpretacao": texto, "ativo": ativo}

@app.post("/api/ai/chat")
async def ai_chat(body: ChatBody, user=Depends(get_user_com_plano)):
    r = ultimo_resultado.get(body.ativo)
    if not r:
        raise HTTPException(404, f"Sem dados para {body.ativo}")
    resposta = await ai_engine.chat(body.pergunta, r, body.ativo)
    return {"resposta": resposta, "ativo": body.ativo}

@app.get("/api/ai/relatorio/{ativo}")
async def ai_relatorio(ativo: str = "WIN", user=Depends(get_user_com_plano)):
    r = ultimo_resultado.get(ativo)
    if not r:
        raise HTTPException(404, f"Sem dados para {ativo}")
    relatorio = await ai_engine.relatorio(r, ativo)
    return {"relatorio": relatorio, "ativo": ativo}

@app.delete("/api/ai/chat/historico")
def limpar_chat(user=Depends(get_current_user)):
    ai_engine.limpar_historico_chat()
    return {"mensagem": "Histórico de chat limpo"}


# ============================================================
# ROTAS PAGAMENTOS
# ============================================================
@app.get("/api/planos")
def listar_planos():
    from payment_engine import PLANOS
    return {"planos": [
        {"id": k, "nome": v["nome"], "preco": v["preco_brl"],
         "duracao_dias": v["duracao_dias"]}
        for k, v in PLANOS.items()
    ]}

@app.post("/api/pagamento/checkout")
async def criar_checkout(body: PlanoBody, user=Depends(get_current_user)):
    try:
        if body.gateway == "stripe":
            return await payment_engine.criar_checkout_stripe(
                user["id"], user["email"], body.plano)
        else:
            return await payment_engine.criar_preferencia_mp(
                user["id"], user["email"], body.plano)
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/api/pagamento/status")
def status_pagamento(user=Depends(get_current_user)):
    return payment_engine.status_assinatura(user["id"])

@app.get("/api/pagamento/historico")
def historico_pagamentos(user=Depends(get_current_user)):
    return {"pagamentos": payment_engine.historico_pagamentos(user["id"])}

@app.post("/api/pagamento/cancelar")
def cancelar_assinatura(user=Depends(get_current_user)):
    ok = payment_engine.cancelar_assinatura(user["id"])
    return {"cancelado": ok}


# ============================================================
# WEBHOOKS (sem autenticação JWT — validados por assinatura)
# ============================================================
@app.post("/webhooks/stripe")
async def webhook_stripe(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        result = payment_engine.processar_webhook_stripe(payload, sig)
        logger.info(f"Stripe webhook: {result}")
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))

@app.post("/webhooks/mercadopago")
async def webhook_mercadopago(request: Request):
    try:
        payload = await request.json()
        result = await payment_engine.processar_webhook_mp(payload)
        logger.info(f"MP webhook: {result}")
        return result
    except Exception as e:
        raise HTTPException(400, str(e))


# ============================================================
# HELPER — converte SMCResult para dict serializável
# ============================================================
def _resultado_para_dict(r) -> dict:
    return {
        # Scores
        "score_final": round(r.score_final, 1),
        "score_compra": round(r.score_compra, 1),
        "score_venda": round(r.score_venda, 1),
        "score_hfz": round(r.score_hfz * 100, 1),
        "score_fbi": round(r.score_fbi * 100, 1),
        "score_dtm": round(r.score_dtm * 100, 1),
        "score_sda": round(r.score_sda * 100, 1),
        "score_mtv": round(r.score_mtv * 100, 1),
        # Estado
        "estado_mercado": r.estado_mercado,
        "direcao": r.direcao,
        "forca": r.forca,
        "qualidade_setup": r.qualidade_setup,
        "risco_contextual": r.risco_contextual,
        "permissao_compra": r.permissao_compra,
        "permissao_venda": r.permissao_venda,
        # HFZ
        "delta_normalizado": round(r.delta_normalizado, 3),
        "hz_normalizado": round(r.hz_normalizado, 3),
        "absorcao_normalizada": round(r.absorcao_normalizada, 3),
        "imbalance_score": round(r.imbalance_score, 3),
        "exaustao_compra": r.exaustao_compra,
        "exaustao_venda": r.exaustao_venda,
        # FBI
        "zona_proxima": r.zona_proxima,
        "preco_zona_proxima": r.preco_zona_proxima,
        "tipo_zona_proxima": r.tipo_zona_proxima,
        "distancia_zona": round(r.distancia_zona * 100, 2),
        "contato_zona": r.contato_zona,
        "reacao_zona": r.reacao_zona,
        # DTM
        "trap_flag": r.trap_flag,
        "trap_intensity": round(r.trap_intensity, 2),
        "falha_continuidade": r.falha_continuidade,
        "eficiencia_deslocamento": round(r.eficiencia_deslocamento, 2),
        # SDA
        "regime_mercado": r.regime_mercado,
        "direcao_regime": r.direcao_regime,
        "vol_normalizada": round(r.vol_normalizada, 2),
        "prob_continuacao": round(r.prob_continuacao, 2),
        "fase_movimento": r.fase_movimento,
        # MTV
        "score_confluencia": round(r.score_confluencia * 100, 1),
        "score_divergencia": round(r.score_divergencia * 100, 1),
        "confluencia_camada": r.confluencia_camada,
        "confluencia_forte": r.confluencia_forte,
        "divergencia_confirmada": r.divergencia_confirmada,
        "sessao_atual": r.sessao_atual,
        "direcao_tf_rapido": r.direcao_tf_rapido,
        "direcao_tf_medio": r.direcao_tf_medio,
        "direcao_tf_lento": r.direcao_tf_lento,
        "direcao_tf_diario": r.direcao_tf_diario,
        "direcao_tf_semanal": r.direcao_tf_semanal,
        "renko_sugestao": r.renko_sugestao,
        "renko_qualidade": r.renko_qualidade,
        "nome_ativo": r.nome_ativo,
        # Eventos
        "evento_score_alto": r.evento_score_alto,
        "evento_trap": r.evento_trap,
        "evento_confluencia": r.evento_confluencia,
        "evento_divergencia": r.evento_divergencia,
        "evento_contato_zona": r.evento_contato_zona,
        # Bloqueios
        "bloqueio_score_baixo": r.bloqueio_score_baixo,
        "bloqueio_trap": r.bloqueio_trap,
        "bloqueio_divergencia": r.bloqueio_divergencia,
    }


# ============================================================
# ENTRY POINT LOCAL
# ============================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)