"""
Payment Engine - Sistema de pagamentos para o SMC SaaS
Suporta Stripe e MercadoPago
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger("smc.payment_engine")


# ============================================================
# PLANOS
# ============================================================
PLANOS = {
    "free": {
        "nome": "Free",
        "preco_brl": 0,
        "duracao_dias": 999999,
        "features": ["sinais_basicos", "1_ativo"]
    },
    "mensal": {
        "nome": "Premium Mensal",
        "preco_brl": 97,
        "duracao_dias": 30,
        "features": ["sinais_completos", "todos_ativos", "alertas"]
    },
    "semestral": {
        "nome": "Premium Semestral",
        "preco_brl": 470,
        "duracao_dias": 180,
        "features": ["sinais_completos", "todos_ativos", "alertas", "suporte"]
    },
    "anual": {
        "nome": "Premium Anual",
        "preco_brl": 797,
        "duracao_dias": 365,
        "features": ["sinais_completos", "todos_ativos", "alertas", "suporte", "优先"]
    }
}


# ============================================================
# CONFIG
# ============================================================
@dataclass
class PaymentConfig:
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    mp_access_token: str = ""
    mp_notification_url: str = "http://localhost:8000"
    modo_simulacao: bool = True


# ============================================================
# Payment Engine
# ============================================================
class PaymentEngine:
    def __init__(self, config: PaymentConfig):
        self.config = config
        self.assinaturas: Dict[str, Dict] = {}
        self.pagamentos: List[Dict] = []
        
        logger.info(f"PaymentEngine inicializado (simulacao: {config.modo_simulacao})")

    def criar_checkout_stripe(self, user_id: str, email: str, plano: str) -> Dict[str, Any]:
        """Cria sessão de checkout Stripe."""
        if plano not in PLANOS:
            raise ValueError(f"Plano invalido: {plano}")
        
        dados_plano = PLANOS[plano]
        
        if self.config.modo_simulacao:
            return {
                "url": f"/checkout/simulado/{plano}",
                "plano": plano,
                "valor": dados_plano["preco_brl"],
                "modo": "simulacao"
            }
        
        # Implementacao real com Stripe
        logger.warning("Stripe: implementacao requer stripe>=5.0")
        return {"url": "/checkout/stripe", "plano": plano}

    async def criar_preferencia_mp(self, user_id: str, email: str, plano: str) -> Dict[str, Any]:
        """Cria preferencia MercadoPago."""
        if plano not in PLANOS:
            raise ValueError(f"Plano invalido: {plano}")
        
        dados_plano = PLANOS[plano]
        
        if self.config.modo_simulacao:
            return {
                "init_point": f"/checkout/simulado/{plano}",
                "plano": plano,
                "valor": dados_plano["preco_brl"],
                "modo": "simulacao"
            }
        
        # Implementacao real com MercadoPago
        logger.warning("MercadoPago: implementacao requer mercadopago>=2.0")
        return {"init_point": "/checkout/mp", "plano": plano}

    def status_assinatura(self, user_id: str) -> Dict[str, Any]:
        """Retorna status da assinatura."""
        if user_id not in self.assinaturas:
            return {
                "ativa": False,
                "plano": "free",
                "user_id": user_id
            }
        
        assinatura = self.assinaturas[user_id]
        
        return {
            "ativa": True,
            "plano": assinatura["plano"],
            "data_expiracao": assinatura.get("data_expiracao"),
            "user_id": user_id
        }

    def processar_webhook_stripe(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Processa webhook do Stripe."""
        if self.config.modo_simulacao:
            logger.info("[SIMULACAO] Stripe webhook processado")
            return {"status": "simulado"}
        
        logger.warning("Stripe webhook: implementacao requerida")
        return {"status": "nao_implementado"}

    async def processar_webhook_mp(self, payload: Dict) -> Dict[str, Any]:
        """Processa webhook do MercadoPago."""
        if self.config.modo_simulacao:
            logger.info("[SIMULACAO] MP webhook processado")
            return {"status": "simulado"}
        
        logger.warning("MercadoPago webhook: implementacao requerida")
        return {"status": "nao_implementado"}

    def historico_pagamentos(self, user_id: str) -> List[Dict]:
        """Retorna historico de pagamentos."""
        return [p for p in self.pagamentos if p.get("user_id") == user_id]

    def cancelar_assinatura(self, user_id: str) -> bool:
        """Cancela assinatura."""
        if user_id in self.assinaturas:
            del self.assinaturas[user_id]
            logger.info(f"Assinatura cancelada: {user_id}")
            return True
        return False


# ============================================================
# Stub classes for compatibility
# ============================================================
class Subscription:
    """Stub para compatibilidade."""
    pass


class Invoice:
    """Stub para compatibilidade."""
    pass
