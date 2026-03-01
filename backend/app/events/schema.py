"""
Schema de Evento Global - Regra de Ouro do SMC
Usado por: WebSocket, Alertas, Replay, IA, Histórico, Relatórios
"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from enum import Enum
import uuid


class SignalDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class SignalSource(str, Enum):
    RTD = "RTD"      # Real-Time Data
    CSV = "CSV"      # CSV File
    API = "API"      # External API


class SignalMode(str, Enum):
    REALTIME = "REALTIME"
    REPLAY = "REPLAY"


class SignalStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class SignalEvent(BaseModel):
    """
    Formato único de evento - Coração do Sistema SMC
    
    Used by:
    - WebSocket broadcasts
    - Alerts system
    - Replay runner
    - AI analysis
    - History records
    - Reports generation
    """
    # Identificação
    event_id: str = uuid.uuid4().__str__()
    timestamp: str = datetime.now().isoformat()
    
    # Dados do ativo
    symbol: str = "WIN$"
    
    # Direção do sinal
    direction: SignalDirection
    
    # Scores individuais (0-1)
    scores: Dict[str, float] = {
        "hfz": 0.0,
        "fbi": 0.0,
        "dtm": 0.0,
        "sda": 0.0,
        "mtv": 0.0
    }
    
    # Score final combinado
    score_final: float = 0.0
    
    # Fonte e modo
    source: SignalSource = SignalSource.CSV
    mode: SignalMode = SignalMode.REALTIME
    
    # Pontos parciais (para gestão de posição)
    partial_points: float = 0.0
    
    # Status do sinal
    status: SignalStatus = SignalStatus.OPEN
    
    # Preço de entrada (quando disponível)
    entry_price: Optional[float] = None
    
    # Preço de saída (quando fechado)
    exit_price: Optional[float] = None
    
    # Pontos finais (lucro/prejuízo)
    final_points: Optional[float] = None
    
    # Timestamp de fechamento
    closed_at: Optional[str] = None
    
    # metadata adicional
    metadata: Dict = {}
    
    class Config:
        use_enum_values = True
    
    def to_dict(self) -> dict:
        """Converte para dicionário para serialização"""
        return self.model_dump()
    
    @classmethod
    def from_smc_result(cls, result, symbol: str = "WIN$", 
                        source: SignalSource = SignalSource.CSV,
                        mode: SignalMode = SignalMode.REALTIME):
        """Cria um SignalEvent a partir de um SMCResult"""
        direction = SignalDirection.BUY if result.direcao == 1 else SignalDirection.SELL
        
        return cls(
            symbol=symbol,
            direction=direction,
            scores={
                "hfz": result.score_hfz,
                "fbi": result.score_fbi,
                "dtm": result.score_dtm,
                "sda": result.score_sda,
                "mtv": result.score_mtv
            },
            score_final=result.score_final,
            source=source,
            mode=mode,
            partial_points=0.0,
            status=SignalStatus.OPEN
        )


class MetricsEvent(BaseModel):
    """Evento de métricas calculado"""
    type: str = "metrics"
    timestamp: str = datetime.now().isoformat()
    
    # Métricas de performance
    assertividade: float = 0.0
    pontos_medios: float = 0.0
    total: int = 0
    wins: int = 0
    losses: int = 0
    
    # Direction breakdown
    buys: int = 0
    sells: int = 0
    
    def to_dict(self) -> dict:
        return self.model_dump()


class AlertEvent(BaseModel):
    """Evento de alerta"""
    type: str = "alert"
    timestamp: str = datetime.now().isoformat()
    
    level: str = "INFO"  # INFO, WARNING, ERROR
    title: str
    message: str
    event_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        return self.model_dump()
