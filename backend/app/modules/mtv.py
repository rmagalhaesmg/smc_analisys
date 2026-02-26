"""
Módulo MTV - Confluência Multi-Timeframe V2.2+V2.3
Análise de alinhamento entre 5 timeframes com calibração por ativo e regime
"""
import numpy as np
from typing import Tuple
from dataclasses import dataclass


@dataclass
class MTVResult:
    """Resultado da análise MTV"""
    score_confluencia: float
    score_divergencia: float
    tipo_confluencia: int
    tipo_divergencia: int
    confluencia_forte: bool
    divergencia_forte: bool
    divergencia_confirmada: bool
    confluencia_camada: int  # 0=nenhuma, 1=estrutural, 2=tendência, 3=total
    renko_sugestao: float
    renko_qualidade: int
    nome_ativo: str
    sessao_atual: int


class MTVModule:
    """Módulo de confluência multi-timeframe"""
    
    def __init__(self):
        # Parâmetros de TF
        self.periodo_atr = 14
        self.threshold_confluencia = 0.75
        self.threshold_divergencia = 0.30
        self.threshold_divergencia_forte = 0.85
        self.threshold_forca_min = 0.15
        self.threshold_expansao_vol = 1.5
        self.threshold_contracao_vol = 0.6
        
        # Pesos base dos TFs
        self.peso_sem_vento = {
            'semanal': 0.35,
            'diario': 0.30,
            'lento': 0.20,
            'medio': 0.10,
            'rapido': 0.05
        }
        
        self.peso_tendencia = {
            'semanal': 0.45,
            'diario': 0.30,
            'lento': 0.15,
            'medio': 0.07,
            'rapido': 0.03
        }
        
        self.peso_lateralizacao = {
            'semanal': 0.20,
            'diario': 0.25,
            'lento': 0.25,
            'medio': 0.20,
            'rapido': 0.10
        }
        
        # Zonas mortas
        self.zona_morta_pct = {
            'medio': 0.10,
            'lento': 0.15,
            'diario': 0.20,
            'semanal': 0.25
        }
        
        # Renko - Perfis de Ativo (V2.3)
        self.ativo_perfis = {
            'WIN': {
                'min': 50.0, 'ref': 200.0, 'max': 600.0,
                'tend': 300.0, 'lat': 100.0, 'trans': 175.0
            },
            'WDO': {
                'min': 1.0, 'ref': 4.0, 'max': 15.0,
                'tend': 6.0, 'lat': 2.0, 'trans': 3.5
            },
            'NASDAQ': {
                'min': 5.0, 'ref': 20.0, 'max': 80.0,
                'tend': 30.0, 'lat': 10.0, 'trans': 18.0
            },
            'ES': {
                'min': 2.0, 'ref': 8.0, 'max': 30.0,
                'tend': 12.0, 'lat': 4.0, 'trans': 7.0
            },
        }
        
        # Escala de Renko por TF (V2.2)
        self.renko_escala_tf = {
            1: 0.50, 2: 0.70, 5: 1.00, 10: 1.35,
            15: 1.65, 30: 2.10, 60: 3.00, 120: 4.00, 240: 5.00
        }
        
        # Sessões de mercado
        self.sessoes = {
            'pre': (830, 930, 0.80),
            'principal': (930, 1200, 1.00),
            'tarde': (1200, 1430, 0.85),
            'fechamento': (1430, 1700, 0.90),
            'fora': (0, 0, 0.70)
        }
        
        # Histórico
        self.hist_close = np.zeros(100)
        self.hist_high = np.zeros(100)
        self.hist_low = np.zeros(100)
        self.hist_tr = np.zeros(100)
        self.hist_volume = np.zeros(100)
    
    def update_history(self, close: float, high: float, low: float,
                      true_range: float, volume: float):
        """Atualiza histórico"""
        self.hist_close = np.roll(self.hist_close, 1)
        self.hist_close[0] = close
        
        self.hist_high = np.roll(self.hist_high, 1)
        self.hist_high[0] = high
        
        self.hist_low = np.roll(self.hist_low, 1)
        self.hist_low[0] = low
        
        self.hist_tr = np.roll(self.hist_tr, 1)
        self.hist_tr[0] = true_range
        
        self.hist_volume = np.roll(self.hist_volume, 1)
        self.hist_volume[0] = volume
    
    def _calculate_atr(self, bars: int) -> float:
        """Calcula ATR (Average True Range) para período"""
        if bars <= 0 or bars > len(self.hist_tr):
            bars = len(self.hist_tr)
        
        atr = np.mean(self.hist_tr[:bars])
        return max(0.001, atr)
    
    def _calculate_direction_force(self, bars_period: int, atr_val: float,
                                  zona_morta: float) -> Tuple[int, float]:
        """Calcula direção e força para timeframe específico"""
        if bars_period <= 1 or bars_period > 99:
            return 0, 0
        
        close_atual = np.mean(self.hist_close[:bars_period])
        close_anterior = np.mean(self.hist_close[bars_period:bars_period*2])
        
        diferenca = close_atual - close_anterior
        
        if diferenca > zona_morta:
            direcao = 1
            forca = min(1.0, diferenca / atr_val)
        elif diferenca < -zona_morta:
            direcao = -1
            forca = min(1.0, (-diferenca) / atr_val)
        else:
            direcao = 0
            forca = 0
        
        # Aplicar threshold mínimo
        if forca < self.threshold_forca_min:
            direcao = 0
            forca = 0
        
        return direcao, forca
    
    def _detect_convergence(self, direcoes: dict, forcas: dict,
                           pesos: dict) -> Tuple[float, float, int]:
        """Detecta confluência entre TFs"""
        score_align = 0
        peso_efetivo = 0
        
        # 10 pares de comparação entre 5 TFs
        pares = [
            ('semanal', 'diario', pesos['semanal']),
            ('semanal', 'lento', pesos['semanal'] * 0.6),
            ('semanal', 'medio', pesos['semanal'] * 0.4),
            ('semanal', 'rapido', pesos['semanal'] * 0.2),
            ('diario', 'lento', pesos['diario']),
            ('diario', 'medio', pesos['diario'] * 0.6),
            ('diario', 'rapido', pesos['diario'] * 0.3),
            ('lento', 'medio', pesos['lento']),
            ('lento', 'rapido', pesos['lento'] * 0.5),
            ('medio', 'rapido', pesos['medio']),
        ]
        
        for tf1, tf2, peso in pares:
            if direcoes[tf1] != 0 and direcoes[tf2] != 0:
                peso_efetivo_par = peso * ((forcas[tf1] + forcas[tf2]) * 0.5)
                
                if direcoes[tf1] == direcoes[tf2]:
                    score_align += peso_efetivo_par
                else:
                    score_align -= peso_efetivo_par
                
                peso_efetivo += peso_efetivo_par
        
        if peso_efetivo > 0:
            score_alinhamento = score_align / peso_efetivo
        else:
            score_alinhamento = 0
        
        # Confluência positiva ou divergência?
        if score_alinhamento > 0:
            confluencia = score_alinhamento
            divergencia = 0
        else:
            confluencia = 0
            divergencia = -score_alinhamento
        
        # Tipo de confluência
        if confluencia >= self.threshold_confluencia:
            if direcoes['diario'] == 1 and direcoes['semanal'] >= 0:
                tipo = 1
            elif direcoes['diario'] == -1 and direcoes['semanal'] <= 0:
                tipo = -1
            else:
                tipo = 0
        else:
            tipo = 0
        
        return confluencia, divergencia, tipo
    
    def _get_renko_sugestao(self, atr_base: float, confluencia: float,
                           divergencia: float, regime: int, tipo_ativo: int,
                           tf_base: int, peso_ancora_ativo: float) -> Tuple[float, int]:
        """Calcula sugestão Renko com novo sistema V2.3"""
        
        # Fator base por confluência/divergência
        if confluencia >= self.threshold_confluencia:
            fator_ajuste = 0.8
        elif divergencia >= self.threshold_divergencia_forte:
            fator_ajuste = 1.2
        else:
            fator_ajuste = 1.0
        
        # Escala pelo TF base
        escala_tf = self.renko_escala_tf.get(tf_base, 1.0)
        
        # Renko calculado por ATR
        renko_atr = atr_base * fator_ajuste * escala_tf
        
        # Obter perfil do ativo
        ativo_nome = f"Ativo {tipo_ativo}"
        if tipo_ativo == 1:
            ativo_nome = "WIN"
            perfil = self.ativo_perfis.get('WIN')
        elif tipo_ativo == 2:
            ativo_nome = "WDO"
            perfil = self.ativo_perfis.get('WDO')
        elif tipo_ativo == 3:
            ativo_nome = "NASDAQ"
            perfil = self.ativo_perfis.get('NASDAQ')
        elif tipo_ativo == 4:
            ativo_nome = "ES"
            perfil = self.ativo_perfis.get('ES')
        else:
            perfil = None
        
        # Aplicar perfil do ativo com blending
        if perfil:
            # Selecionar âncora por regime
            if regime == 1:  # Tendência
                ancora_regime = perfil['tend']
            elif regime == 2:  # Lateral
                ancora_regime = perfil['lat']
            else:  # Transição
                ancora_regime = perfil['trans']
            
            # Blending entre ATR e âncora
            renko_sugestao = (renko_atr * (1 - peso_ancora_ativo)) + \
                           (ancora_regime * peso_ancora_ativo)
            
            # Pinçar dentro de min/max
            renko_sugestao = max(perfil['min'], min(perfil['max'], renko_sugestao))
        else:
            renko_sugestao = renko_atr
        
        # Qualidade Renko
        if confluencia > self.threshold_confluencia and regime != 2:
            qualidade = 3
        elif confluencia > 0.5 or regime == 1:
            qualidade = 2
        else:
            qualidade = 1
        
        return renko_sugestao, qualidade
    
    def _get_sessao(self, hora: int) -> Tuple[int, float]:
        """Determina sessão de mercado e seu multiplicador"""
        if 830 <= hora < 930:
            return 1, self.sessoes['pre'][2]
        elif 930 <= hora < 1200:
            return 2, self.sessoes['principal'][2]
        elif 1200 <= hora < 1430:
            return 3, self.sessoes['tarde'][2]
        elif 1430 <= hora < 1700:
            return 4, self.sessoes['fechamento'][2]
        else:
            return 0, self.sessoes['fora'][2]
    
    def analyze(self, regime: int, hora: int, tipo_ativo: int = 1,
               tf_base: int = 5, peso_ancora_ativo: float = 0.5) -> MTVResult:
        """
        Executa análise completa MTV com 5 TFs
        
        Args:
            regime: Regime do SDA (1=Tendência, 2=Lateral, 3=Transição)
            hora: Hora em formato HHMM
            tipo_ativo: Tipo do ativo para calibração Renko
            tf_base: TimeFrame base em minutos
            peso_ancora_ativo: Peso da âncora do ativo vs ATR (0-1)
            
        Returns:
            MTVResult com análise completa
        """
        # Pesos dinâmicos por regime
        if regime == 1:  # Tendência
            pesos = self.peso_tendencia
        elif regime == 2:  # Lateral
            pesos = self.peso_lateralizacao
        else:
            pesos = self.peso_sem_vento
        
        # Calcular ATRs por TF
        atr_rapido = self._calculate_atr(14)
        atr_medio = self._calculate_atr(12)  # 60min = 12 barras de 5min
        atr_lento = self._calculate_atr(6)   # 240min = 48 barras, usar cap
        atr_diario = self._calculate_atr(4)  # ~288 barras, usar cap
        atr_semanal = self._calculate_atr(2) # ~1440 barras, usar cap
        
        # Calcular direções e forças
        direcoes = {}
        forcas = {}
        
        for tf_name, bars, atr in [
            ('rapido', 1, atr_rapido),
            ('medio', 12, atr_medio),
            ('lento', 48, atr_lento),
            ('diario', 288, atr_diario),
            ('semanal', 1440, atr_semanal)
        ]:
            zona_morta = atr * self.zona_morta_pct.get(tf_name, 0.15)
            dir_, forca = self._calculate_direction_force(
                min(bars, 99), atr, zona_morta
            )
            direcoes[tf_name] = dir_
            forcas[tf_name] = forca
        
        # Detectar confluência/divergência
        conf, div, tipo_conf = self._detect_convergence(direcoes, forcas, pesos)
        
        # Sessão de mercado
        sessao, score_sessao = self._get_sessao(hora)
        conf *= score_sessao
        
        # Renko
        renko_sug, renko_qual = self._get_renko_sugestao(
            atr_rapido, conf, div, regime, tipo_ativo, tf_base, peso_ancora_ativo
        )
        
        # Confluência por camada
        conf_estrutural = (direcoes['semanal'] != 0 and
                          direcoes['diario'] != 0 and
                          direcoes['semanal'] == direcoes['diario'])
        
        conf_tendencia = (conf_estrutural and
                         direcoes['lento'] != 0 and
                         direcoes['lento'] == direcoes['semanal'])
        
        conf_total = (conf_tendencia and
                     direcoes['medio'] != 0 and
                     direcoes['rapido'] != 0 and
                     direcoes['medio'] == direcoes['semanal'] and
                     direcoes['rapido'] == direcoes['semanal'])
        
        if conf_total:
            camada = 3
        elif conf_tendencia:
            camada = 2
        elif conf_estrutural:
            camada = 1
        else:
            camada = 0
        
        # Divergência confirmada
        div_confirmada = (div >= self.threshold_divergencia_forte and
                         ((direcoes['semanal'] != 0 and
                           direcoes['diario'] != 0 and
                           direcoes['semanal'] == direcoes['diario'] and
                           direcoes['rapido'] != 0 and
                           direcoes['rapido'] != direcoes['semanal'])))
        
        return MTVResult(
            score_confluencia=conf,
            score_divergencia=div,
            tipo_confluencia=tipo_conf,
            tipo_divergencia=1 if div_confirmada else -1,
            confluencia_forte=conf >= self.threshold_confluencia,
            divergencia_forte=div >= self.threshold_divergencia_forte,
            divergencia_confirmada=div_confirmada,
            confluencia_camada=camada,
            renko_sugestao=renko_sug,
            renko_qualidade=renko_qual,
            nome_ativo=f"Ativo {tipo_ativo}",
            sessao_atual=sessao
        )
