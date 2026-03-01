"""
Replay Runner - Backtest Unificado com o Motor SMC
O mesmo motor roda tanto em tempo real quanto em replay/backtest
"""
import asyncio
from datetime import datetime
from typing import Optional, List, Callable
from app.ingestion.csv_parser import parse_csv
from app.events.schema import SignalEvent, SignalSource, SignalMode
from app.signals.manager import signal_manager
from app.websocket.manager import manager as ws_manager
import logging

logger = logging.getLogger(__name__)


class ReplayRunner:
    """
    Runner para Replay/Backtest usando o Motor SMC
    
    Características:
    - Usa o MESMO motor SMC que o tempo real
    - Gera eventos no formato padronizado
    - Suporta replay via WebSocket
    - Calcula métricas em tempo real
    """
    
    def __init__(self, core_engine, speed: float = 1.0):
        """
        Args:
            core_engine: Instância do SMCCoreEngine
            speed: Multiplicador de velocidade (1.0 = tempo real, 10.0 = 10x mais rápido)
        """
        self.core_engine = core_engine
        self.speed = speed
        self.is_running = False
        self.is_paused = False
        self.current_bar_index = 0
        self.total_bars = 0
        self.bars: List = []
        
        # Callbacks
        self.on_signal: Optional[Callable] = None
        self.on_bar: Optional[Callable] = None
        self.on_complete: Optional[Callable] = None
    
    async def load_csv(self, csv_path: str) -> int:
        """
        Carrega dados CSV para replay
        
        Returns:
            Número de barras carregadas
        """
        self.bars = parse_csv(csv_path)
        self.total_bars = len(self.bars)
        self.current_bar_index = 0
        
        logger.info(f"Loaded {self.total_bars} bars for replay")
        
        # Broadcast de início de replay
        await ws_manager.broadcast_replay({
            "type": "replay_start",
            "total_bars": self.total_bars,
            "speed": self.speed
        })
        
        return self.total_bars
    
    async def run(self, csv_path: str = None, bars: List = None):
        """
        Executa o replay/backtest
        
        Args:
            csv_path: Caminho do arquivo CSV (opcional se bars for fornecido)
            bars: Lista de barras pré-carregadas (opcional)
        """
        self.is_running = True
        
        # Carrega barras
        if csv_path:
            await self.load_csv(csv_path)
        elif bars:
            self.bars = bars
            self.total_bars = len(bars)
            self.current_bar_index = 0
        else:
            raise ValueError("Either csv_path or bars must be provided")
        
        # Loop principal de replay
        for bar in self.bars:
            if not self.is_running:
                break
            
            # Pausa se solicitado
            while self.is_paused and self.is_running:
                await asyncio.sleep(0.1)
            
            # Processa a barra no motor SMC
            result = self.core_engine.process(bar)
            
            # Callback de barra processada
            if self.on_bar:
                self.on_bar(bar, result)
            
            # Broadcast de progresso
            if self.current_bar_index % 10 == 0:
                await ws_manager.broadcast_replay({
                    "type": "replay_progress",
                    "current": self.current_bar_index,
                    "total": self.total_bars,
                    "progress": self.current_bar_index / self.total_bars * 100
                })
            
            # Se há sinal válido
            if result and result.permissao_operar:
                signal = self._create_signal_event(result, bar)
                
                # Abre o sinal
                signal_manager.open_signal(signal)
                
                # Broadcast do novo sinal
                await ws_manager.broadcast_signal(signal.to_dict())
                
                # Callback de sinal
                if self.on_signal:
                    self.on_signal(signal)
            
            # Verifica fechamento de sinais
            if signal_manager.open_signals:
                closed = signal_manager.check_and_close_by_price(bar.close)
                for closed_signal in closed:
                    await ws_manager.broadcast_signal(closed_signal.to_dict())
            
            # Controle de velocidade
            base_delay = 0.05 / self.speed  # 50ms base
            await asyncio.sleep(base_delay)
            
            self.current_bar_index += 1
        
        # Replay completo
        self.is_running = False
        
        # Broadcast de conclusão
        metrics = signal_manager.get_metrics()
        await ws_manager.broadcast_replay({
            "type": "replay_complete",
            "metrics": metrics.to_dict(),
            "total_bars": self.total_bars
        })
        
        # Callback de conclusão
        if self.on_complete:
            self.on_complete(signal_manager.get_metrics())
        
        logger.info(f"Replay complete. Processed {self.total_bars} bars")
    
    def _create_signal_event(self, result, bar) -> SignalEvent:
        """Cria um SignalEvent a partir do resultado do SMC"""
        from app.events.schema import SignalDirection
        
        direction = SignalDirection.BUY if result.direcao == 1 else SignalDirection.SELL
        
        return SignalEvent(
            symbol="WIN$",  # Você pode parametrizar
            direction=direction,
            scores={
                "hfz": result.score_hfz,
                "fbi": result.score_fbi,
                "dtm": result.score_dtm,
                "sda": result.score_sda,
                "mtv": result.score_mtv
            },
            score_final=result.score_final,
            source=SignalSource.CSV,
            mode=SignalMode.REPLAY,
            entry_price=bar.close,
            metadata={
                "bar_timestamp": str(bar.timestamp_hhmm) if hasattr(bar, 'timestamp_hhmm') else None,
                "quality": result.qualidade_setup,
                "risk": result.risco_contextual
            }
        )
    
    def pause(self):
        """Pausa o replay"""
        self.is_paused = True
        logger.info("Replay paused")
    
    def resume(self):
        """Retoma o replay"""
        self.is_paused = False
        logger.info("Replay resumed")
    
    def stop(self):
        """Para o replay"""
        self.is_running = False
        logger.info("Replay stopped")
    
    def set_speed(self, speed: float):
        """Ajusta a velocidade do replay"""
        self.speed = max(0.1, min(100.0, speed))
        logger.info(f"Replay speed set to {self.speed}x")
    
    def get_progress(self) -> dict:
        """Retorna o progresso atual do replay"""
        return {
            "running": self.is_running,
            "paused": self.is_paused,
            "current": self.current_bar_index,
            "total": self.total_bars,
            "progress": (self.current_bar_index / self.total_bars * 100) if self.total_bars > 0 else 0
        }


# Função de conveniência para rodar backtest
async def run_backtest(csv_path: str, core_engine, speed: float = 10.0) -> dict:
    """
    Executa um backtest completo
    
    Args:
        csv_path: Caminho do CSV do Profit
        core_engine: Instância do SMCCoreEngine
        speed: Velocidade do replay (default 10x)
    
    Returns:
        Métricas do backtest
    """
    runner = ReplayRunner(core_engine, speed=speed)
    await runner.run(csv_path=csv_path)
    return signal_manager.get_metrics().to_dict()
