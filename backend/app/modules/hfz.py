"""
Módulo HFZ - Microestrutura e Fluxo
Análise de delta, frequência, absorção e imbalance
"""
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class HFZResult:
    """Resultado da análise HFZ"""
    delta_normalizado: float
    hz_normalizado: float
    absorcao_normalizada: float
    imbalance_score: float
    pressao_liquida: float
    score_hfz: float
    score_compra: float
    score_venda: float
    qualidade_fluxo: int
    tentativa_cont_alta: bool
    tentativa_cont_baixa: bool
    exaustao_compra: bool
    exaustao_venda: bool


class HFZModule:
    """Módulo de análise de microestrutura e fluxo"""
    
    def __init__(self):
        # Parâmetros HFZ
        self.periodo_delta = 20
        self.suavizacao_delta = 5
        self.periodo_hz = 60
        self.threshold_hz_baixo = 0.3
        self.threshold_hz_alto = 1.5
        self.periodo_atr = 14
        self.threshold_absorcao = 1.5
        self.periodo_imbalance = 10
        self.threshold_imbalance_forte = 0.6
        self.janela_pressao = 15
        
        # Pesos
        self.peso_delta = 0.30
        self.peso_hz = 0.25
        self.peso_absorcao = 0.20
        self.peso_imbalance = 0.15
        self.peso_pressao = 0.10
        
        # Histórico
        self.hist_delta = np.zeros(100)
        self.hist_hz = np.zeros(100)
        self.hist_volume = np.zeros(100)
        
    def update_history(self, delta: float, hz: float, volume: float):
        """Atualiza histórico com novos valores"""
        self.hist_delta = np.roll(self.hist_delta, 1)
        self.hist_delta[0] = delta
        
        self.hist_hz = np.roll(self.hist_hz, 1)
        self.hist_hz[0] = hz
        
        self.hist_volume = np.roll(self.hist_volume, 1)
        self.hist_volume[0] = volume
    
    def _normalize_delta(self, delta_suavizado: float) -> float:
        """Normaliza o delta usando média e desvio padrão"""
        media = np.mean(self.hist_delta[:self.periodo_delta])
        desvio = np.std(self.hist_delta[:self.periodo_delta])
        
        if desvio > 0:
            return (delta_suavizado - media) / desvio
        return 0
    
    def _calculate_hz(self, volume_compra: float, volume_venda: float, trades: int) -> float:
        """Calcula frequência ponderada"""
        hz_frequencia = trades / 60  # trades por minuto
        hz_volume = volume_compra / 60 if volume_compra > 0 else 0
        
        # Normalizar Hz
        if hz_frequencia < self.threshold_hz_baixo:
            hz_normalizado = 0.2
        elif hz_frequencia > self.threshold_hz_alto:
            hz_normalizado = 1.0
        else:
            hz_normalizado = (hz_frequencia - self.threshold_hz_baixo) / \
                           (self.threshold_hz_alto - self.threshold_hz_baixo)
        
        return hz_normalizado
    
    def _calculate_absorcao(self, volume_compra: float, volume_venda: float,
                           range_barra: float, atr: float) -> Tuple[float, float, float]:
        """Calcula absorção de compra e venda"""
        media_volume = np.mean(self.hist_volume[:20])
        if media_volume <= 0:
            media_volume = 1
            
        if range_barra > 0:
            absorcao_compra = (volume_compra / media_volume) / (range_barra / atr)
            absorcao_venda = (volume_venda / media_volume) / (range_barra / atr)
        else:
            absorcao_compra = 0
            absorcao_venda = 0
        
        if absorcao_compra > absorcao_venda:
            absorcao_normalizada = min(1.0, absorcao_compra / self.threshold_absorcao)
        else:
            absorcao_normalizada = min(1.0, absorcao_venda / self.threshold_absorcao)
        
        return absorcao_compra, absorcao_venda, absorcao_normalizada
    
    def _calculate_imbalance(self, volume_compra: float, volume_venda: float,
                            delta: float) -> float:
        """Calcula imbalance do livro e fluxo"""
        total_volume = volume_compra + volume_venda
        if total_volume > 0:
            imbalance_book = (volume_compra - volume_venda) / total_volume
        else:
            imbalance_book = 0
        
        media_volume = np.mean(self.hist_volume[:20])
        if media_volume > 0:
            imbalance_fluxo = delta / media_volume
        else:
            imbalance_fluxo = 0
        
        imbalance_score = (imbalance_book + imbalance_fluxo) * 0.5
        
        # Limitar entre -1 e 1
        return max(-1, min(1, imbalance_score))
    
    def analyze(self, volume_compra: float, volume_venda: float, trades: int,
               high: float, low: float, open_: float, close: float,
               atr: float, tick_minimo: float) -> HFZResult:
        """
        Executa análise completa HFZ
        
        Args:
            volume_compra: Volume de agressão de compra
            volume_venda: Volume de agressão de venda
            trades: Número de trades na barra
            high: Máxima da barra
            low: Mínima da barra
            open_: Abertura da barra
            close: Fechamento da barra
            atr: ATR calculado
            tick_minimo: Tamanho mínimo do tick
            
        Returns:
            HFZResult com análise completa
        """
        if atr <= 0:
            atr = tick_minimo
        
        # Delta
        delta_bruto = volume_compra - volume_venda
        delta_suavizado = self._suavizar_exponencial(delta_bruto)
        delta_normalizado = self._normalize_delta(delta_suavizado)
        
        # Hz
        hz_normalizado = self._calculate_hz(volume_compra, volume_venda, trades)
        
        # Absorção
        range_barra = high - low
        if range_barra < tick_minimo:
            range_barra = tick_minimo
            
        abs_compra, abs_venda, abs_normalizada = self._calculate_absorcao(
            volume_compra, volume_venda, range_barra, atr
        )
        
        # Imbalance
        imbalance = self._calculate_imbalance(volume_compra, volume_venda, delta_bruto)
        
        # Pressão
        hist_pos = np.sum(self.hist_delta[:self.janela_pressao][self.hist_delta[:self.janela_pressao] > 0])
        hist_neg = np.sum(-self.hist_delta[:self.janela_pressao][self.hist_delta[:self.janela_pressao] < 0])
        
        pressao_compra = hist_pos / self.janela_pressao if self.janela_pressao > 0 else 0
        pressao_venda = hist_neg / self.janela_pressao if self.janela_pressao > 0 else 0
        pressao_liquida = pressao_compra - pressao_venda
        
        # Tentativas de continuação
        tentativa_alta = (delta_normalizado > 0.5) and (hz_normalizado > 0.6) and \
                        (pressao_compra > pressao_venda * 1.5)
        tentativa_baixa = (delta_normalizado < -0.5) and (hz_normalizado > 0.6) and \
                         (pressao_venda > pressao_compra * 1.5)
        
        # Exaustão
        media_volume = np.mean(self.hist_volume[:20])
        exaustao_compra = (abs_compra > self.threshold_absorcao) and \
                         (volume_compra > media_volume * 1.8) and (close < open_)
        exaustao_venda = (abs_venda > self.threshold_absorcao) and \
                        (volume_venda > media_volume * 1.8) and (close > open_)
        
        # Score Compra
        score_compra = 0.0
        if delta_normalizado > 0:
            score_compra += delta_normalizado * self.peso_delta
        score_compra += hz_normalizado * self.peso_hz
        if abs_compra < self.threshold_absorcao:
            score_compra += (1 - abs_normalizada) * self.peso_absorcao
        if imbalance > 0:
            score_compra += imbalance * self.peso_imbalance
        if pressao_liquida > 0:
            score_compra += (pressao_compra / (pressao_compra + pressao_venda + 1)) * self.peso_pressao
        
        score_compra = min(1.0, score_compra)
        
        # Score Venda
        score_venda = 0.0
        if delta_normalizado < 0:
            score_venda += (-delta_normalizado) * self.peso_delta
        score_venda += hz_normalizado * self.peso_hz
        if abs_venda < self.threshold_absorcao:
            score_venda += (1 - abs_normalizada) * self.peso_absorcao
        if imbalance < 0:
            score_venda += (-imbalance) * self.peso_imbalance
        if pressao_liquida < 0:
            score_venda += (pressao_venda / (pressao_compra + pressao_venda + 1)) * self.peso_pressao
        
        score_venda = min(1.0, score_venda)
        
        score_hfz = score_compra - score_venda
        
        # Qualidade de fluxo
        if hz_normalizado > 0.8:
            qualidade_fluxo = 10
        elif hz_normalizado > 0.6:
            qualidade_fluxo = 7
        elif hz_normalizado > 0.4:
            qualidade_fluxo = 5
        else:
            qualidade_fluxo = 2
        
        return HFZResult(
            delta_normalizado=delta_normalizado,
            hz_normalizado=hz_normalizado,
            absorcao_normalizada=abs_normalizada,
            imbalance_score=imbalance,
            pressao_liquida=pressao_liquida,
            score_hfz=score_hfz,
            score_compra=score_compra,
            score_venda=score_venda,
            qualidade_fluxo=qualidade_fluxo,
            tentativa_cont_alta=tentativa_alta,
            tentativa_cont_baixa=tentativa_baixa,
            exaustao_compra=exaustao_compra,
            exaustao_venda=exaustao_venda
        )
    
    def _suavizar_exponencial(self, valor: float, alpha: float = None) -> float:
        """Suavização exponencial simples"""
        if alpha is None:
            alpha = 2.0 / (self.suavizacao_delta + 1)
        return valor
