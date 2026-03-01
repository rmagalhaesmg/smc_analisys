"""
Core Engine - Motor principal do SMC (Smart Money Concepts)
Analise de mercados financeiros usando conceitos de smart money
"""
import os
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger("smc.core_engine")


# ============================================================
# DATA CLASSES
# ============================================================
@dataclass
class Bar:
    """Representa um candle/barra de preco."""
    open: float
    high: float
    low: float
    close: float
    volume: float
    volume_compra: float = 0
    volume_venda: float = 0
    trades: int = 0
    true_range: float = 0
    timestamp_hhmm: int = 0
    tick_minimo: float = 5.0


@dataclass
class SMCResult:
    """Resultado da analise SMC."""
    # Scores
    score_final: float = 50.0
    score_compra: float = 50.0
    score_venda: float = 50.0
    score_hfz: float = 50.0
    score_fbi: float = 50.0
    score_dtm: float = 50.0
    score_sda: float = 50.0
    score_mtv: float = 50.0
    
    # Direcao
    estado_mercado: str = "lateral"
    direcao: str = "neutro"
    forca: float = 50.0
    qualidade_setup: int = 3
    
    # Permissoes
    permissao_compra: bool = False
    permissao_venda: bool = False
    risco_contextual: str = "baixo"
    
    # HFZ
    delta_normalizado: float = 0
    hz_normalizado: float = 0
    absorcao_normalizada: float = 0
    imbalance_score: float = 0
    exaustao_compra: bool = False
    exaustao_venda: bool = False
    
    # FBI
    zona_proxima: str = ""
    preco_zona_proxima: float = 0
    tipo_zona_proxima: str = ""
    distancia_zona: float = 0
    contato_zona: bool = False
    reacao_zona: str = ""
    
    # DTM
    trap_flag: bool = False
    trap_intensity: float = 0
    falha_continuidade: bool = False
    eficiencia_deslocamento: float = 0
    
    # SDA
    regime_mercado: str = "lateral"
    direcao_regime: str = "neutro"
    vol_normalizada: float = 0
    prob_continuacao: float = 0
    fase_movimento: str = ""
    
    # MTV
    score_confluencia: float = 0
    score_divergencia: float = 0
    confluencia_camada: List[str] = field(default_factory=list)
    confluencia_forte: bool = False
    divergencia_confirmada: bool = False
    sessao_atual: str = ""
    direcao_tf_rapido: str = "neutro"
    direcao_tf_medio: str = "neutro"
    direcao_tf_lento: str = "neutro"
    direcao_tf_diario: str = "neutro"
    direcao_tf_semanal: str = "neutro"
    renko_sugestao: str = ""
    renko_qualidade: int = 0
    
    # Info
    nome_ativo: str = ""
    
    # Eventos
    evento_score_alto: bool = False
    evento_trap: bool = False
    evento_confluencia: bool = False
    evento_divergencia: bool = False
    evento_contato_zona: bool = False
    
    # Bloqueios
    bloqueio_score_baixo: bool = False
    bloqueio_trap: bool = False
    bloqueio_divergencia: bool = False


# ============================================================
# SMC CORE ENGINE
# ============================================================
class SMCCoreEngine:
    def __init__(
        self,
        tf_base_minutos: int = 5,
        modo_operacao: int = 2,
        tipo_ativo: int = 1
    ):
        self.tf_base_minutos = tf_base_minutos
        self.modo_operacao = modo_operacao
        self.tipo_ativo = tipo_ativo
        
        self.barras: List[Bar] = []
        self.contador_barras = 0
        self.ultimo_resultado: Optional[SMCResult] = None
        
        logger.info(f"SMCCoreEngine inicializado (TF: {tf_base_minutos}m, modo: {modo_operacao})")

    def process(self, bar: Bar) -> Optional[SMCResult]:
        """Processa uma barra e retorna analise SMC."""
        self.barras.append(bar)
        self.contador_barras += 1
        
        # Warmup - precisa de barras suficientes
        if len(self.barras) < 60:
            return None
        
        # Limita tamanho do buffer
        if len(self.barras) > 500:
            self.barras = self.barras[-500:]
        
        # Executa analise SMC
        resultado = self._analisar()
        self.ultimo_resultado = resultado
        
        return resultado

    def _analisar(self) -> SMCResult:
        """Executa a analise completa SMC."""
        barras = self.barras
        ultima = barras[-1]
        
        # Calculo basico de scores
        resultado = SMCResult(
            nome_ativo=getattr(self, 'ativo', 'WIN'),
            estado_mercado=self._detectar_estado(barras),
            direcao=self._detectar_direcao(barras),
            qualidade_setup=3
        )
        
        # Calcula scores dos modulos
        resultado = self._calcular_scores(barras, resultado)
        
        # Determina permissao final
        resultado = self._determinar_permissao(resultado)
        
        return resultado

    def _detectar_estado(self, barras: List[Bar]) -> str:
        """Detecta estado do mercado."""
        if len(barras) < 20:
            return "lateral"
        
        ultimos = barras[-20:]
        highs = [b.high for b in ultimos]
        lows = [b.low for b in ultimos]
        
        # Simplificado: detecta se ha tendencia
        primeiro_high = highs[0]
        ultimo_high = highs[-1]
        primeiro_low = lows[0]
        ultimo_low = lows[-1]
        
        if ultimo_high > primeiro_high and ultimo_low > primeiro_low:
            return "alta"
        elif ultimo_high < primeiro_high and ultimo_low < primeiro_low:
            return "baixa"
        
        return "lateral"

    def _detectar_direcao(self, barras: List[Bar]) -> str:
        """Detecta direcao predominante."""
        if len(barras) < 10:
            return "neutro"
        
        ultimas = barras[-10:]
        closes = [b.close for b in ultimas]
        
        media = sum(closes) / len(closes)
        ultimo_close = closes[-1]
        
        if ultimo_close > media * 1.001:
            return "COMPRA"
        elif ultimo_close < media * 0.999:
            return "VENDA"
        
        return "neutro"

    def _calcular_scores(self, barras: List[Bar], resultado: SMCResult) -> SMCResult:
        """Calcula scores dos modulos SMC."""
        # Scores simulados baseados em indicadores simples
        
        ultima = barras[-1]
        media20 = sum([b.close for b in barras[-20:]]) / 20
        
        # Score baseado em posicao relativa
        if ultima.close > media20:
            resultado.score_compra = 60
            resultado.score_venda = 40
        else:
            resultado.score_compra = 40
            resultado.score_venda = 60
        
        # Scores dos modulos
        resultado.score_hfz = 50
        resultado.score_fbi = 50
        resultado.score_dtm = 50
        resultado.score_sda = 50
        resultado.score_mtv = 50
        
        # Score final
        resultado.score_final = (resultado.score_compra + resultado.score_venda) / 2
        
        return resultado

    def _determinar_permissao(self, resultado: SMCResult) -> SMCResult:
        """Determina permissoes de compra/venda."""
        # Regras basicas
        if resultado.score_final >= 60 and resultado.qualidade_setup >= 3:
            if resultado.direcao == "COMPRA":
                resultado.permissao_compra = True
            elif resultado.direcao == "VENDA":
                resultado.permissao_venda = True
        
        # Bloqueios
        if resultado.score_final < 55:
            resultado.bloqueio_score_baixo = True
        
        return resultado

    def reset(self):
        """Reseta o engine."""
        self.barras = []
        self.contador_barras = 0
        self.ultimo_resultado = None
        logger.info("SMCCoreEngine resetado")

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatisticas do engine."""
        return {
            "barras_processadas": self.contador_barras,
            "barras_buffer": len(self.barras),
            "ultimo_resultado": self.ultimo_resultado is not None
        }


# ============================================================
# Stub classes for compatibility
# ============================================================
class SMCEngine:
    """Alias para compatibilidade."""
    pass


class MarketAnalyzer:
    """Stub para compatibilidade."""
    pass
