"""
Signal Manager - Fechamento Automático de Sinais
Gerencia o ciclo de vida completo dos sinais SMC
"""
from typing import List, Optional, Dict
from datetime import datetime
from app.events.schema import SignalEvent, SignalStatus, MetricsEvent
from app.websocket.manager import manager as ws_manager


class SignalManager:
    """
    Gerenciador de Sinais - Controla abertura e fechamento
    
    Responsabilidades:
    - Abrir novos sinais quando SMC gerar sinal válido
    - Fechar sinais por: alvo atingido, stop atingido, expiração
    - Calcular métricas em tempo real
    - Persistir histórico
    """
    
    def __init__(self):
        # Sinais abertos (em andamento)
        self.open_signals: Dict[str, SignalEvent] = {}
        
        # Histórico de sinais fechados
        self.closed_signals: List[SignalEvent] = []
        
        # Limite de sinais no histórico
        self.max_history = 1000
    
    def open_signal(self, event: SignalEvent) -> SignalEvent:
        """Abre um novo sinal"""
        # Armazena na lista de sinais abertos
        self.open_signals[event.event_id] = event
        
        # Broadcast do novo sinal
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(ws_manager.broadcast({
                    "type": "signal_new",
                    "data": event.to_dict()
                }))
        except:
            pass
        
        return event
    
    def close_signal(self, signal: SignalEvent, exit_price: float, reason: str = "MANUAL") -> SignalEvent:
        """
        Fecha um sinal existente
        
        Args:
            signal: O evento do sinal a ser fechado
            exit_price: Preço de saída
            reason: Motivo do fechamento (TARGET, STOP, TIME, MANUAL)
        
        Returns:
            O sinal fechado com campos atualizados
        """
        # Atualiza status
        signal.status = SignalStatus.CLOSED
        signal.exit_price = exit_price
        signal.closed_at = datetime.now().isoformat()
        
        # Calcula pontos finais
        if signal.entry_price:
            if signal.direction == "BUY":
                signal.final_points = exit_price - signal.entry_price
            else:  # SELL
                signal.final_points = signal.entry_price - exit_price
        
        # Adiciona reason ao metadata
        signal.metadata["close_reason"] = reason
        signal.metadata["closed_at"] = signal.closed_at
        
        # Remove da lista de abertos
        if signal.event_id in self.open_signals:
            del self.open_signals[signal.event_id]
        
        # Adiciona ao histórico
        self.closed_signals.append(signal)
        
        # Limita tamanho do histórico
        if len(self.closed_signals) > self.max_history:
            self.closed_signals = self.closed_signals[-self.max_history:]
        
        # Broadcast do sinal fechado
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(ws_manager.broadcast({
                    "type": "signal_closed",
                    "data": signal.to_dict()
                }))
                # Também emite métricas atualizadas
                asyncio.create_task(self._broadcast_metrics())
        except:
            pass
        
        return signal
    
    def check_and_close_by_price(self, current_price: float, 
                                 target_multiplier: float = 2.0,
                                 stop_multiplier: float = 1.0) -> List[SignalEvent]:
        """
        Verifica se algum sinal deve ser fechado por alvo ou stop
        
        Args:
            current_price: Preço atual do ativo
            target_multiplier: Multiplicador do ATR para alvo (default 2x)
            stop_multiplier: Multiplicador do ATR para stop (default 1x)
        
        Returns:
            Lista de sinais fechados
        """
        closed = []
        
        for signal_id, signal in list(self.open_signals.items()):
            if not signal.entry_price:
                continue
            
            direction = signal.direction
            entry = signal.entry_price
            
            # Calcula distância do preço atual
            if direction == "BUY":
                points = current_price - entry
            else:
                points = entry - current_price
            
            # Atualiza pontos parciais
            signal.partial_points = points
            
            # Aqui você adicionaria lógica de ATR para stop/target
            # Por agora, usa lógica simples baseada em pontos
            
            # Exemplo: Sepoints > 100 (alvo) ou < -50 (stop)
            if points > 100:  # Alvo atingido
                closed.append(self.close_signal(signal, current_price, "TARGET"))
            elif points < -50:  # Stop atingido
                closed.append(self.close_signal(signal, current_price, "STOP"))
        
        return closed
    
    def close_all_signals(self, reason: str = "EMERGENCY") -> List[SignalEvent]:
        """Fecha todos os sinais abertos (emergência)"""
        closed = []
        current_price = 0.0  # Você pegaria o preço atual aqui
        
        for signal_id, signal in list(self.open_signals.items()):
            closed.append(self.close_signal(signal, current_price, reason))
        
        return closed
    
    def get_metrics(self) -> MetricsEvent:
        """
        Calcula métricas de assertividade
        
        Fórmula:
        - assertividade = wins / total * 100
        - pontos_medios = sum(final_points) / total
        """
        total = len(self.closed_signals)
        
        if total == 0:
            return MetricsEvent(
                assertividade=0.0,
                pontos_medios=0.0,
                total=0,
                wins=0,
                losses=0
            )
        
        # Calcula wins (pontos > 0)
        wins = sum(1 for s in self.closed_signals if s.final_points and s.final_points > 0)
        losses = total - wins
        
        # Calcula pontos médios
        pontos = [s.final_points for s in self.closed_signals if s.final_points is not None]
        pontos_medios = sum(pontos) / len(pontos) if pontos else 0.0
        
        # Calcula assertividade
        assertividade = (wins / total) * 100 if total > 0 else 0.0
        
        # Conta por direção
        buys = sum(1 for s in self.closed_signals if s.direction == "BUY")
        sells = total - buys
        
        return MetricsEvent(
            assertividade=round(assertividade, 2),
            pontos_medios=round(pontos_medios, 2),
            total=total,
            wins=wins,
            losses=losses,
            buys=buys,
            sells=sells
        )
    
    async def _broadcast_metrics(self):
        """Emite métricas via WebSocket"""
        metrics = self.get_metrics()
        await ws_manager.broadcast({
            "type": "metrics",
            "data": metrics.to_dict()
        })
    
    def get_open_signals(self) -> List[SignalEvent]:
        """Retorna lista de sinais abertos"""
        return list(self.open_signals.values())
    
    def get_closed_signals(self, limit: int = 100) -> List[SignalEvent]:
        """Retorna lista de sinais fechados (mais recentes primeiro)"""
        return self.closed_signals[-limit:][::-1]
    
    def get_signal_by_id(self, event_id: str) -> Optional[SignalEvent]:
        """Busca sinal por ID (aberto ou fechado)"""
        if event_id in self.open_signals:
            return self.open_signals[event_id]
        
        for signal in self.closed_signals:
            if signal.event_id == event_id:
                return signal
        
        return None
    
    def clear_history(self):
        """Limpa o histórico de sinais"""
        self.closed_signals = []


# Singleton instance
signal_manager = SignalManager()
