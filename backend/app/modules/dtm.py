"""
Módulo DTM - Validação e Detecção de Armadilhas
Identifica false breakouts, eficiência de movimento, renovação de volume
"""
import numpy as np
from typing import Tuple
from dataclasses import dataclass


@dataclass
class DTMResult:
    """Resultado da análise DTM"""
    trap_flag: bool
    trap_intensity: float
    trap_type: int  # 1=Bull Trap, -1=Bear Trap, 0=Nenhum
    falha_continuidade: bool
    score_continuidade: float
    eficiencia_deslocamento: float
    renovacao_real: bool
    score_dtm: float


class DTMModule:
    """Módulo de validação e detecção de armadilhas"""
    
    def __init__(self):
        self.threshold_trap_volume = 1.8
        self.min_barras_trap = 3
        self.janela_continuidade = 5
        self.threshold_falha_cont = 0.6
        self.janela_eficiencia = 10
        self.threshold_eficiencia_baixa = 0.4
        self.periodo_renovacao = 10
        self.threshold_renovacao_real = 1.5
        
        # Pesos
        self.peso_trap = 0.40
        self.peso_continuidade = 0.30
        self.peso_eficiencia = 0.20
        self.peso_renovacao = 0.10
        
        self.contador_trap = 0
        self.hist_close = np.zeros(100)
        self.hist_high = np.zeros(100)
        self.hist_low = np.zeros(100)
        self.hist_volume = np.zeros(100)
        self.hist_hz = np.zeros(100)
    
    def update_history(self, close: float, high: float, low: float, 
                      volume: float, hz: float):
        """Atualiza histórico"""
        self.hist_close = np.roll(self.hist_close, 1)
        self.hist_close[0] = close
        
        self.hist_high = np.roll(self.hist_high, 1)
        self.hist_high[0] = high
        
        self.hist_low = np.roll(self.hist_low, 1)
        self.hist_low[0] = low
        
        self.hist_volume = np.roll(self.hist_volume, 1)
        self.hist_volume[0] = volume
        
        self.hist_hz = np.roll(self.hist_hz, 1)
        self.hist_hz[0] = hz
    
    def _detect_trap(self, volume: float, high: float, low: float, 
                    open_: float, close: float, hz: float) -> Tuple[bool, float, int]:
        """Detecta armadilhas (false breakouts)"""
        media_volume = np.mean(self.hist_volume[:20])
        if media_volume <= 0:
            media_volume = 1
        
        range_barra = high - low
        
        # Bull Trap: volume alto, rompimento para cima mas fechamento baixo
        if (volume > media_volume * self.threshold_trap_volume and
            close > open_ and
            high > self.hist_high[1] and
            close < (high - (range_barra * 0.7)) and
            hz < 0.6):
            
            return True, 0.7, 1  # Bull trap
        
        # Bear Trap: volume alto, rompimento para baixo mas fechamento alto
        if (volume > media_volume * self.threshold_trap_volume and
            close < open_ and
            low < self.hist_low[1] and
            close > (low + (range_barra * 0.7)) and
            hz < 0.6):
            
            return True, 0.7, -1  # Bear trap
        
        return False, 0, 0
    
    def _check_continuidade(self, tentativa_alta: bool, 
                           tentativa_baixa: bool) -> bool:
        """Verifica se há falha na continuidade do movimento"""
        if tentativa_alta:
            closes_altos = sum(1 for i in range(self.janela_continuidade)
                             if self.hist_close[i] > self.hist_close[i+1])
            
            if closes_altos < (self.janela_continuidade * self.threshold_falha_cont):
                return True
        
        elif tentativa_baixa:
            closes_baixos = sum(1 for i in range(self.janela_continuidade)
                              if self.hist_close[i] < self.hist_close[i+1])
            
            if closes_baixos < (self.janela_continuidade * self.threshold_falha_cont):
                return True
        
        return False
    
    def _calculate_eficiencia(self) -> float:
        """Calcula eficiência de deslocamento"""
        range_total = np.sum(self.hist_high[:self.janela_eficiencia] - 
                            self.hist_low[:self.janela_eficiencia])
        
        deslocamento = 0
        for i in range(self.janela_eficiencia - 1):
            deslocamento += abs(self.hist_close[i] - self.hist_close[i+1])
        
        if range_total > 0:
            return deslocamento / range_total
        return 0
    
    def _check_renovacao(self) -> bool:
        """Verifica se há renovação real de volume"""
        primeira_metade = np.mean(self.hist_hz[:self.periodo_renovacao // 2])
        segunda_metade = np.mean(self.hist_hz[self.periodo_renovacao // 2:self.periodo_renovacao])
        
        if segunda_metade > 0:
            return segunda_metade > (primeira_metade * self.threshold_renovacao_real)
        
        return False
    
    def analyze(self, volume: float, high: float, low: float, open_: float, 
               close: float, hz: float, tentativa_alta: bool, 
               tentativa_baixa: bool) -> DTMResult:
        """
        Executa análise completa DTM
        
        Args:
            volume: Volume da barra
            high: Máxima
            low: Mínima
            open_: Abertura
            close: Fechamento
            hz: Frequência normalizada
            tentativa_alta: Tentativa de continuação alta
            tentativa_baixa: Tentativa de continuação baixa
            
        Returns:
            DTMResult com análise de validação
        """
        # Detectar armadilhas
        trap_detected, trap_intensity, trap_type = self._detect_trap(
            volume, high, low, open_, close, hz
        )
        
        if trap_detected:
            self.contador_trap = self.min_barras_trap
        elif self.contador_trap > 0:
            self.contador_trap -= 1
            trap_detected = True
            trap_intensity *= 0.8
        
        # Verificar continuidade
        falha_continuidade = self._check_continuidade(tentativa_alta, tentativa_baixa)
        
        if falha_continuidade:
            score_continuidade = 0.3
        else:
            score_continuidade = 1 - self.threshold_falha_cont
        
        # Eficiência de deslocamento
        eficiencia = self._calculate_eficiencia()
        
        # Renovação
        renovacao_real = self._check_renovacao()
        
        # Score DTM
        score_dtm = 0.0
        
        if trap_detected:
            score_dtm += (1 - trap_intensity) * self.peso_trap
        else:
            score_dtm += 1 * self.peso_trap
        
        score_dtm += score_continuidade * self.peso_continuidade
        
        if eficiencia > self.threshold_eficiencia_baixa:
            score_dtm += eficiencia * self.peso_eficiencia
        
        if renovacao_real:
            score_dtm += 1 * self.peso_renovacao
        
        score_dtm = min(1.0, score_dtm)
        
        return DTMResult(
            trap_flag=trap_detected,
            trap_intensity=trap_intensity,
            trap_type=trap_type,
            falha_continuidade=falha_continuidade,
            score_continuidade=score_continuidade,
            eficiencia_deslocamento=eficiencia,
            renovacao_real=renovacao_real,
            score_dtm=score_dtm
        )
