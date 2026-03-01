"""
Configuração centralizada da aplicação SMC
"""
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseModel as BaseSettings
    SettingsConfigDict = None
from pydantic import Field
import os


class Settings(BaseSettings):
    """Settings da aplicação"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    ) if SettingsConfigDict else {}
    
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
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_IDS: str = ""
    
    # Notificações - Email (strings vazias por padrão)
    SENDGRID_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@smcanalysis.com"
    EMAIL_TO_ADDRESSES: str = ""
    
    # Notificações - WhatsApp (strings vazias por padrão)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    WHATSAPP_NUMBERS: str = ""
    
    # OpenAI / LLM
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    
    # Configuração de Ingestão de Dados
    CSV_UPLOAD_DIR: str = "./uploads/csv"
    ALLOWED_FILE_EXTENSIONS: list = [".csv", ".xlsx", ".json"]
    MAX_FILE_SIZE_MB: int = 100
    
    # Parâmetros SMC - Carregáveis via .env
    SMC_TIPO_ATIVO: int = 1  # 1=WIN, 2=WDO, 3=NASDAQ, 4=ES, 5=Ações, 6=Forex, 7=Cripto
    SMC_TF_BASE_MINUTOS: int = 5
    SMC_MODO_OPERACAO: int = 2  # 1=Conservador, 2=Normal, 3=Agressivo
    SMC_ALERTING_ENABLED: bool = True
    SMC_ML_REFINEMENT: bool = True
    SMC_LLM_ANALYSIS: bool = False
    
    # Parâmetros padrão SMC (legado)
    SMC_DEFAULT_PARAMS: dict = {
        "tipo_ativo": 1,
        "tf_base_minutos": 5,
        "modo_operacao": 2,
    }
    
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
