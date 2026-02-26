"""
Módulo SDA - Regime e Estrutura de Mercado
Análise de tendência, volatilidade, continuação e exaustão
"""
import numpy as np
from typing import Tuple
from dataclasses import dataclass


@dataclass
class SDAResult:
    """Resultado da análise SDA"""
    regime_mercado: int  # 1=Tendência, 2=Lateral, 3=Transição
    direcao_regime: int  # 1=Alta, -1=Baixa, 0=Neutra
    score_regime: float
    vol_atual: float
    vol_normalizada: float
    prob_continuacao: float
    prob_exaustao: float
    fase_movimento: int  # 1=Iniciação, 2=Continuação, 3=Exaustão
    score_sda: float
    score_continuacao: float


class SDAModule:
    """Módulo de análise de regime e estrutura"""
    
    def __init__(self):
        self.periodo_regime = 30
        self.threshold_tendencia = 0.6
        self.threshold_lateral = 0.3
        self.periodo_vol = 20
        self.janela_normalizacao_vol = 50
        self.periodo_continuacao = 15
        self.threshold_continuacao_alta = 0.7
        self.threshold_exaustao = 2.5
        self.janela_deslocamento = 20
        
        # Pesos
        self.peso_regime = 0.30
        self.peso_vol = 0.25
        self.peso_continuacao = 0.25
        self.peso_deslocamento = 0.20
        
        self.hist_close = np.zeros(100)
        self.hist_high = np.zeros(100)
        self.hist_low = np.zeros(100)
        self.hist_volume = np.zeros(100)
        self.hist_tr = np.zeros(100)  # True Range
        self.hist_vol_sda = np.zeros(100)
    
    def update_history(self, close: float, high: float, low: float, 
                      volume: float, true_range: float):
        """Atualiza histórico"""
        self.hist_close = np.roll(self.hist_close, 1)
        self.hist_close[0] = close
        
        self.hist_high = np.roll(self.hist_high, 1)
        self.hist_high[0] = high
        
        self.hist_low = np.roll(self.hist_low, 1)
        self.hist_low[0] = low
        
        self.hist_volume = np.roll(self.hist_volume, 1)
        self.hist_volume[0] = volume
        
        self.hist_tr = np.roll(self.hist_tr, 1)
        self.hist_tr[0] = true_range
        
        vol_atual = np.mean(self.hist_tr[:self.periodo_vol])
        self.hist_vol_sda = np.roll(self.hist_vol_sda, 1)
        self.hist_vol_sda[0] = vol_atual
    
    def _identify_regime(self) -> Tuple[int, int, float]:
        """Identifica regime de mercado"""
        # Calcular eficiência de movimento
        closes_altos = sum(1 for i in range(self.periodo_regime)
                          if self.hist_close[i] > self.hist_close[i+1])
        
        eficiencia_direcional = closes_altos / self.periodo_regime
        
        # Calcular amplitude vs deslocamento
        amplitude_total = np.sum(self.hist_high[:self.periodo_regime] - 
                               self.hist_low[:self.periodo_regime])
        
        deslocamento_liquido = abs(self.hist_close[0] - self.hist_close[self.periodo_regime])
        
        if amplitude_total > 0:
            eficiencia_movimento = deslocamento_liquido / amplitude_total
        else:
            eficiencia_movimento = 0
        
        # Determinar regime
        if eficiencia_movimento > self.threshold_tendencia:
            regime = 1  # Tendência
            
            # Determinar direção
            if eficiencia_direcional > 0.6:
                direcao = 1  # Alta
            elif eficiencia_direcional < 0.4:
                direcao = -1  # Baixa
            else:
                direcao = 0  # Neutra
            
            score = eficiencia_movimento
        
        elif eficiencia_movimento < self.threshold_lateral:
            regime = 2  # Lateralização
            direcao = 0
            score = 1 - eficiencia_movimento
        
        else:
            regime = 3  # Transição
            direcao = 0
            score = 0.5
        
        return regime, direcao, score
    
    def _analyze_volatility(self) -> Tuple[float, float]:
        """Analisa volatilidade normalizada"""
        vol_atual = np.mean(self.hist_tr[:self.periodo_vol])
        
        # Normalizar volatilidade
        media_vol = np.mean(self.hist_vol_sda[:self.janela_normalizacao_vol])
        desvio_vol = np.std(self.hist_vol_sda[:self.janela_normalizacao_vol])
        
        if desvio_vol > 0:
            vol_normalizada = (vol_atual - media_vol) / desvio_vol
        else:
            vol_normalizada = 0
        
        return vol_atual, vol_normalizada
    
    def _analyze_continuacao(self, direcao_regime: int) -> Tuple[float, float, int]:
        """Analisa probabilidade de continuação"""
        if direcao_regime == 1:  # Tendência alta
            closes_altos = sum(1 for i in range(self.periodo_continuacao)
                             if self.hist_close[i] > self.hist_close[i+1])
            prob_continuacao = closes_altos / self.periodo_continuacao
        
        elif direcao_regime == -1:  # Tendência baixa
            closes_baixos = sum(1 for i in range(self.periodo_continuacao)
                              if self.hist_close[i] < self.hist_close[i+1])
            prob_continuacao = closes_baixos / self.periodo_continuacao
        
        else:
            prob_continuacao = 0.5
        
        # Probabilidade de exaustão
        media_volume = np.mean(self.hist_volume[:self.periodo_continuacao])
        volume_atual = self.hist_volume[0]
        
        if (volume_atual > media_volume * self.threshold_exaustao and
            prob_continuacao < 0.4):
            prob_exaustao = 0.8
        else:
            prob_exaustao = 1 - prob_continuacao
        
        # Fase do movimento
        if prob_continuacao > 0.7:
            fase = 2  # Continuação
        elif prob_exaustao > 0.6:
            fase = 3  # Exaustão
        else:
            fase = 1  # Iniciação
        
        return prob_continuacao, prob_exaustao, fase
    
    def analyze(self, close: float, high: float, low: float, 
               volume: float, true_range: float) -> SDAResult:
        """
        Executa análise completa SDA
        
        Args:
            close: Fechamento
            high: Máxima
            low: Mínima
            volume: Volume
            true_range: True Range
            
        Returns:
            SDAResult com análise de regime e estrutura
        """
        # Identificar regime
        regime, direcao, score_regime = self._identify_regime()
        
        # Volatilidade
        vol_atual, vol_normalizada = self._analyze_volatility()
        
        # Continuação
        prob_continuacao, prob_exaustao, fase = self._analyze_continuacao(direcao)
        
        # Deslocamento médio
        dist_media_desl = np.mean([abs(self.hist_close[i] - self.hist_close[i+1])
                                   for i in range(self.janela_deslocamento - 1)])
        
        # Score SDA
        score_sda = 0.0
        score_sda += score_regime * self.peso_regime
        
        # Score volatilidade
        if vol_normalizada < 0:
            vol_score = 0
        elif vol_normalizada > 2:
            vol_score = 1.0
        else:
            vol_score = vol_normalizada / 2
        
        score_sda += vol_score * self.peso_vol
        score_sda += prob_continuacao * self.peso_continuacao
        
        # Score deslocamento
        if dist_media_desl > 0 and close > 0:
            desl_pct = dist_media_desl / (close * 0.01)
            desl_pct = min(1.0, desl_pct)
            score_sda += desl_pct * self.peso_deslocamento
        
        score_sda = min(1.0, score_sda)
        
        return SDAResult(
            regime_mercado=regime,
            direcao_regime=direcao,
            score_regime=score_regime,
            vol_atual=vol_atual,
            vol_normalizada=vol_normalizada,
            prob_continuacao=prob_continuacao,
            prob_exaustao=prob_exaustao,
            fase_movimento=fase,
            score_sda=score_sda,
            score_continuacao=prob_continuacao
        )
