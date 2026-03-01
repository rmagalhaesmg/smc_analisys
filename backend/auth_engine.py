"""
Auth Engine - Sistema de autenticação para o SMC SaaS
Gerencia usuários, tokens JWT e sessões
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import hashlib
import secrets

logger = logging.getLogger("smc.auth_engine")


# ============================================================
# CONFIG
# ============================================================
@dataclass
class AuthConfig:
    jwt_secret: str = "TROQUE_EM_PRODUCAO_256BITS"
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    frontend_url: str = "http://localhost:3000"


# ============================================================
# Auth Engine
# ============================================================
class AuthEngine:
    def __init__(self, config: AuthConfig):
        self.config = config
        self.users: Dict[str, Dict] = {}
        self.tokens: Dict[str, Dict] = {}
        
        logger.info("AuthEngine inicializado")

    def register_user(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        """Registra novo usuário."""
        if username in self.users:
            raise ValueError(f"Usuario {username} ja existe")
        
        # Hash simples da senha (em producao use bcrypt)
        password_hash = self._hash_password(password)
        
        self.users[username] = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        logger.info(f"Usuario registrado: {username}")
        return self.users[username]

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Autentica usuário e retorna token."""
        if username not in self.users:
            raise ValueError("Usuario ou senha invalidos")
        
        user = self.users[username]
        password_hash = self._hash_password(password)
        
        if password_hash != user["password_hash"]:
            raise ValueError("Usuario ou senha invalidos")
        
        # Gera token
        token = secrets.token_urlsafe(32)
        self.tokens[token] = {
            "username": username,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=7)
        }
        
        logger.info(f"Login bem-sucedido: {username}")
        return {
            "token": token,
            "username": username,
            "email": user.get("email", "")
        }

    def verificar_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica se token é válido."""
        if token not in self.tokens:
            return None
        
        token_data = self.tokens[token]
        
        # Verifica expiração
        if datetime.now() > token_data["expires_at"]:
            del self.tokens[token]
            return None
        
        return {
            "username": token_data["username"],
            "token": token
        }

    def logout(self, token: str):
        """Invalida token."""
        if token in self.tokens:
            del self.tokens[token]
            logger.info("Logout realizado")

    def _hash_password(self, password: str) -> str:
        """Hash simples de senha."""
        # Em producao, use bcrypt ou argon2
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Retorna dados do usuário."""
        return self.users.get(username)

    def list_users(self) -> List[Dict[str, Any]]:
        """Lista todos os usuários."""
        return list(self.users.values())


# ============================================================
# Stub classes for compatibility
# ============================================================
class AuthService:
    """Alias para compatibilidade."""
    pass


class User:
    """Stub para compatibilidade."""
    pass
