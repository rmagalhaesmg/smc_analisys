"""
Alert Engine - Sistema de alertas para o SMC SaaS
Suporta Telegram, Email e WhatsApp
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger("smc.alert_engine")


# ============================================================
# CONFIG classes
# ============================================================
@dataclass
class TelegramConfig:
    token: str = ""
    chat_id: str = ""
    enabled: bool = False


@dataclass
class EmailConfig:
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    from_addr: str = ""
    to_addr: str = ""
    sendgrid_key: str = ""
    enabled: bool = False


@dataclass
class WhatsAppConfig:
    twilio_sid: str = ""
    twilio_token: str = ""
    twilio_from: str = ""
    twilio_to: str = ""
    enabled: bool = False


@dataclass
class AlertConfig:
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    email: EmailConfig = field(default_factory=EmailConfig)
    whatsapp: WhatsAppConfig = field(default_factory=WhatsAppConfig)
    min_score_alerta: float = 55.0
    min_qualidade_alerta: int = 4
    rate_limit_segundos: int = 60
    modo_simulacao: bool = True


# ============================================================
# Alert Engine
# ============================================================
class AlertEngine:
    def __init__(self, config: AlertConfig, ativo: str = "WIN"):
        self.config = config
        self.ativo = ativo
        self.ultimo_alerta = None
        self.total_enviados = 0
        self.log: List[Dict] = []
        
        logger.info(f"AlertEngine inicializado para {ativo} (simulacao: {config.modo_simulacao})")

    def processar(self, resultado: Dict[str, Any]) -> bool:
        """Processa resultado e envia alertas se necessario."""
        if resultado is None:
            return False
        
        score = resultado.get("score_final", 0)
        qualidade = resultado.get("qualidade_setup", 0)
        
        # Verifica se deve enviar alerta
        if (score >= self.config.min_score_alerta and 
            qualidade >= self.config.min_qualidade_alerta):
            
            # Rate limiting
            if self.ultimo_alerta:
                tempo_desde_ultimo = (datetime.now() - self.ultimo_alerta).total_seconds()
                if tempo_desde_ultimo < self.config.rate_limit_segundos:
                    logger.debug("Alerta ignorado por rate limit")
                    return False
            
            # Envia alertas
            self._enviar_alertas(resultado)
            self.ultimo_alerta = datetime.now()
            self.total_enviados += 1
            return True
        
        return False

    def _enviar_alertas(self, resultado: Dict[str, Any]):
        """Envia alertas para todos os canais configurados."""
        mensagem = self._formatar_mensagem(resultado)
        
        if self.config.telegram.enabled and self.config.telegram.token:
            self._enviar_telegram(mensagem)
        
        if self.config.email.enabled:
            self._enviar_email(mensagem)
        
        if self.config.whatsapp.enabled:
            self._enviar_whatsapp(mensagem)
        
        # Log
        self.log.append({
            "timestamp": datetime.now().isoformat(),
            "mensagem": mensagem,
            "score": resultado.get("score_final", 0)
        })

    def _formatar_mensagem(self, resultado: Dict[str, Any]) -> str:
        """Formata mensagem de alerta."""
        direcao = resultado.get("direcao", "NEUTRO")
        score = resultado.get("score_final", 0)
        qualidade = resultado.get("qualidade_setup", 0)
        
        emoji = "🟢" if direcao == "COMPRA" else "🔴" if direcao == "VENDA" else "⚪"
        
        return f"""
{emoji} *SMC Alert - {self.ativo}*

📊 Score: {score:.1f}
📈 Direcao: {direcao}
⭐ Qualidade: {qualidade}/5

💰 Permissao Compra: {resultado.get('permissao_compra', False)}
💸 Permissao Venda: {resultado.get('permissao_venda', False)}

🔗 Analise completa disponivel no dashboard
"""

    def _enviar_telegram(self, mensagem: str):
        """Envia alerta via Telegram."""
        if self.config.modo_simulacao:
            logger.info(f"[SIMULACAO] Telegram: {mensagem[:50]}...")
            return
        
        # Implementacao real do Telegram
        logger.warning("Telegram: implementacao requer python-telegram-bot")

    def _enviar_email(self, mensagem: str):
        """Envia alerta via Email."""
        if self.config.modo_simulacao:
            logger.info(f"[SIMULACAO] Email: {mensagem[:50]}...")
            return
        
        # Implementacao real de email
        logger.warning("Email: implementacao requer smtplib ou sendgrid")

    def _enviar_whatsapp(self, mensagem: str):
        """Envia alerta via WhatsApp (Twilio)."""
        if self.config.modo_simulacao:
            logger.info(f"[SIMULACAO] WhatsApp: {mensagem[:50]}...")
            return
        
        # Implementacao real do WhatsApp
        logger.warning("WhatsApp: implementacao requer twilio")

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatisticas do engine."""
        return {
            "total_enviados": self.total_enviados,
            "ultimo_alerta": self.ultimo_alerta.isoformat() if self.ultimo_alerta else None,
            "log_count": len(self.log)
        }

    def get_log(self) -> List[Dict]:
        """Retorna log de alertas."""
        return self.log[-50:]  # ultimos 50


# ============================================================
# Stub classes for compatibility
# ============================================================
class AlertService:
    """Alias para compatibilidade."""
    pass


class EmailAlert:
    """Stub para compatibilidade."""
    pass


class TelegramAlert:
    """Stub para compatibilidade."""
    pass
