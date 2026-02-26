"""
Configuração centralizada da aplicação SMC
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Settings da aplicação"""
    
    # Aplicação
    APP_NAME: str = "SMC - Sistema de Monitoramento Contínuo"
    APP_VERSION: str = "2.3.0"
    DEBUG: bool = False
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: list = ["*"]
    
    # Banco de dados
    DATABASE_URL: str = "sqlite:///./smc.db"
    
    # Notificações - Telegram (strings vazias por padrão)
    TELEGRAM_BOT_TOKEN: str = Field(default="", env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_IDS: str = Field(default="", env="TELEGRAM_CHAT_IDS")
    
    # Notificações - Email (strings vazias por padrão)
    SENDGRID_API_KEY: str = Field(default="", env="SENDGRID_API_KEY")
    EMAIL_FROM: str = Field(default="noreply@smcanalysis.com", env="EMAIL_FROM")
    EMAIL_TO_ADDRESSES: str = Field(default="", env="EMAIL_TO_ADDRESSES")
    
    # Notificações - WhatsApp (strings vazias por padrão)
    TWILIO_ACCOUNT_SID: str = Field(default="", env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = Field(default="", env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = Field(default="", env="TWILIO_PHONE_NUMBER")
    WHATSAPP_NUMBERS: str = Field(default="", env="WHATSAPP_NUMBERS")
    
    # OpenAI / LLM
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    LLM_MODEL: str = "gpt-4"
    
    # Configuração de Ingestão de Dados
    CSV_UPLOAD_DIR: str = "./uploads/csv"
    ALLOWED_FILE_EXTENSIONS: list = [".csv", ".xlsx", ".json"]
    MAX_FILE_SIZE_MB: int = 100
    
    # Parâmetros SMC - Carregáveis via .env
    SMC_TIPO_ATIVO: int = Field(default=1, env="SMC_TIPO_ATIVO")  # 1=WIN, 2=WDO, 3=NASDAQ, 4=ES, 5=Ações, 6=Forex, 7=Cripto
    SMC_TF_BASE_MINUTOS: int = Field(default=5, env="SMC_TF_BASE_MINUTOS")
    SMC_MODO_OPERACAO: int = Field(default=2, env="SMC_MODO_OPERACAO")  # 1=Conservador, 2=Normal, 3=Agressivo
    SMC_ALERTING_ENABLED: bool = Field(default=True, env="SMC_ALERTING_ENABLED")
    SMC_ML_REFINEMENT: bool = Field(default=True, env="SMC_ML_REFINEMENT")
    SMC_LLM_ANALYSIS: bool = Field(default=False, env="SMC_LLM_ANALYSIS")
    
    # Parâmetros padrão SMC (legado)
    SMC_DEFAULT_PARAMS: dict = {
        "tipo_ativo": 1,
        "tf_base_minutos": 5,
        "modo_operacao": 2,
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Permite campos extras sem erro
    
    # Helper methods para converter strings em listas
    def get_telegram_chat_ids(self) -> list:
        """Converter TELEGRAM_CHAT_IDS de string para lista"""
        if not self.TELEGRAM_CHAT_IDS:
            return []
        return [id.strip() for id in str(self.TELEGRAM_CHAT_IDS).split(",") if id.strip()]
    
    def get_email_to_addresses(self) -> list:
        """Converter EMAIL_TO_ADDRESSES de string para lista"""
        if not self.EMAIL_TO_ADDRESSES:
            return []
        return [addr.strip() for addr in str(self.EMAIL_TO_ADDRESSES).split(",") if addr.strip()]
    
    def get_whatsapp_numbers(self) -> list:
        """Converter WHATSAPP_NUMBERS de string para lista"""
        if not self.WHATSAPP_NUMBERS:
            return []
        return [num.strip() for num in str(self.WHATSAPP_NUMBERS).split(",") if num.strip()]


settings = Settings()
