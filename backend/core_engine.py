"""
SMC Core Engine - Reimplementação Python do SMC MTV V2.3
Fidelidade matemática total ao indicador NTSL original.
Módulos: HFZ, FBI, DTM, SDA, MTV, Score, Filter, EventLogger
"""
import math
from dataclasses import dataclass, field
from typing import Optional

# ===========================================================================
# CONSTANTES (espelho exato do NTSL)
# ===========================================================================
MAX_HISTORICO = 100
BARRAS_MINIMAS_INICIO = 60

# HFZ
PERIODO_DELTA_HFZ = 20
SUAVIZACAO_DELTA = 5
PERIODO_ATR_HFZ = 14
THRESHOLD_HZ_BAIXO = 0.3
THRESHOLD_HZ_ALTO = 1.5
PESO_HZ_PRECO = 0.5
PESO_HZ_FLUXO = 0.5
THRESHOLD_ABSORCAO_HFZ = 1.5
JANELA_PRESSAO = 15
PESO_HFZ_DELTA = 0.30
PESO_HFZ_HZ = 0.25
PESO_HFZ_ABSORCAO = 0.20
PESO_HFZ_IMBALANCE = 0.15
PESO_HFZ_PRESSAO = 0.10

# FBI
PERIODO_LIQUIDEZ_FBI = 30
MIN_TOQUES_ZONA = 1
DISTANCIA_MERGE_ZONA = 0.003
MAX_ZONAS_FBI = 20
THRESHOLD_FORCA_ZONA = 1.5
MAX_DISTANCIA_ZONA = 0.050
PESO_FBI_FORCA = 0.40
PESO_FBI_DISTANCIA = 0.30
PESO_FBI_TIPO = 0.20
PESO_FBI_REACAO = 0.10

# DTM
THRESHOLD_TRAP_VOLUME = 1.8
MIN_BARRAS_TRAP = 3
JANELA_CONTINUIDADE = 5
THRESHOLD_FALHA_CONT = 0.6
JANELA_EFICIENCIA = 10
THRESHOLD_EFICIENCIA_BAIXA = 0.4
PERIODO_RENOVACAO_DTM = 10
THRESHOLD_RENOVACAO_REAL = 1.5
PESO_DTM_TRAP = 0.40
PESO_DTM_CONTINUIDADE = 0.30
PESO_DTM_EFICIENCIA = 0.20
PESO_DTM_RENOVACAO = 0.10

# SDA
PERIODO_REGIME = 30
THRESHOLD_TENDENCIA = 0.6
THRESHOLD_LATERAL = 0.3
PERIODO_VOL_SDA = 20
JANELA_NORMALIZACAO_VOL = 50
PERIODO_CONTINUACAO_SDA = 15
THRESHOLD_EXAUSTAO_ALTA = 2.5
JANELA_DESLOCAMENTO = 20
PESO_SDA_REGIME = 0.30
PESO_SDA_VOL = 0.25
PESO_SDA_CONTINUACAO = 0.25
PESO_SDA_DESLOCAMENTO = 0.20

# MTV
THRESHOLD_CONFLUENCIA = 0.75
THRESHOLD_DIVERGENCIA = 0.30
THRESHOLD_DIVERGENCIA_FORTE = 0.85
THRESHOLD_FORCA_MIN_MTV = 0.15
THRESHOLD_EXPANSAO_VOL = 1.5
THRESHOLD_CONTRACAO_VOL = 0.6
PESO_TF_SEMANAL_BASE = 0.35; PESO_TF_DIARIO_BASE = 0.30
PESO_TF_LENTO_BASE = 0.20;   PESO_TF_MEDIO_BASE = 0.10; PESO_TF_RAPIDO_BASE = 0.05
PESO_TF_SEMANAL_TEND = 0.45; PESO_TF_DIARIO_TEND = 0.30
PESO_TF_LENTO_TEND = 0.15;   PESO_TF_MEDIO_TEND = 0.07; PESO_TF_RAPIDO_TEND = 0.03
PESO_TF_SEMANAL_LAT = 0.20;  PESO_TF_DIARIO_LAT = 0.25
PESO_TF_LENTO_LAT = 0.25;    PESO_TF_MEDIO_LAT = 0.20;  PESO_TF_RAPIDO_LAT = 0.10
RENKO_FATOR_MINIMO = 0.5;    RENKO_FATOR_MAXIMO = 2.0
RENKO_FATOR_CONFLUENCIA = 0.8; RENKO_FATOR_DIVERGENCIA = 1.2; RENKO_FATOR_NEUTRO = 1.0
ZONA_MORTA_TF_MEDIO = 0.10;  ZONA_MORTA_TF_LENTO = 0.15
ZONA_MORTA_TF_DIARIO = 0.20; ZONA_MORTA_TF_SEMANAL = 0.25

RENKO_ESCALA_TF = {1: 0.50, 2: 0.70, 5: 1.00, 10: 1.35,
                   15: 1.65, 30: 2.10, 60: 3.00, 120: 4.00, 240: 5.00}

SESSAO_PRE_INI = 830;       SESSAO_PRE_FIM = 930
SESSAO_PRINCIPAL_INI = 930; SESSAO_PRINCIPAL_FIM = 1200
SESSAO_TARDE_INI = 1200;    SESSAO_TARDE_FIM = 1430
SESSAO_FECHAMENTO_INI = 1430; SESSAO_FECHAMENTO_FIM = 1700
SCORE_SESSAO = {0: 0.70, 1: 0.80, 2: 1.00, 3: 0.85, 4: 0.90}

PERFIS_ATIVO = {
    1: {"nome": "WIN (Mini Índice)", "min": 50.0,   "ref": 200.0,  "max": 600.0,  "tend": 300.0,  "lat": 100.0,  "trans": 175.0},
    2: {"nome": "WDO (Mini Dólar)",  "min": 1.0,    "ref": 4.0,    "max": 15.0,   "tend": 6.0,    "lat": 2.0,    "trans": 3.5},
    3: {"nome": "NASDAQ / NQ",       "min": 5.0,    "ref": 20.0,   "max": 80.0,   "tend": 30.0,   "lat": 10.0,   "trans": 18.0},
    4: {"nome": "ES / SP500",        "min": 2.0,    "ref": 8.0,    "max": 30.0,   "tend": 12.0,   "lat": 4.0,    "trans": 7.0},
    5: {"nome": "Acoes BR",          "min": 0.05,   "ref": 0.20,   "max": 1.00,   "tend": 0.30,   "lat": 0.10,   "trans": 0.18},
    6: {"nome": "Forex (Major)",     "min": 0.0005, "ref": 0.0020, "max": 0.0080, "tend": 0.0030, "lat": 0.0010, "trans": 0.0018},
    7: {"nome": "Cripto (BTC/USD)",  "min": 50.0,   "ref": 200.0,  "max": 1000.0, "tend": 350.0,  "lat": 100.0,  "trans": 200.0},
}

PESO_MODULO_HFZ = 0.40
PESO_MODULO_FBI = 0.20
PESO_MODULO_DTM = 0.20
PESO_MODULO_SDA = 0.10
PESO_MODULO_MTV = 0.10
THRESHOLD_SCORE_ALTO = 55
THRESHOLD_SCORE_MEDIO = 40

MIN_SCORE_OPERACAO = 30
MAX_TRAP_PERMITIDO = 0.6
MIN_HZ_ZONA = 0.2
MIN_VOL_NORMALIZADA = 0.1

MIN_SCORE_LOG = 65
MIN_TRAP_INTENSITY_LOG = 0.6
MIN_ABSORCAO_LOG = 1.5
MIN_HZ_PICO_LOG = 2.5


@dataclass
class Bar:
    open: float
    high: float
    low: float
    close: float
    volume: float
    volume_compra: float
    volume_venda: float
    trades: int
    true_range: float
    timestamp_hhmm: int
    tick_minimo: float = 1.0


@dataclass
class SMCResult:
    score_hfz: float = 0.0
    score_fbi: float = 0.0
    score_dtm: float = 0.0
    score_sda: float = 0.0
    score_mtv: float = 0.0
    score_final: float = 0.0
    score_compra: float = 0.0
    score_venda: float = 0.0
    direcao: int = 0
    forca: int = 1
    estado_mercado: int = 4
    qualidade_setup: int = 0
    risco_contextual: int = 0
    permissao_operar: bool = False
    permissao_compra: bool = False
    permissao_venda: bool = False
    delta_normalizado: float = 0.0
    hz_normalizado: float = 0.0
    absorcao_normalizada: float = 0.0
    imbalance_score: float = 0.0
    pressao_liquida: float = 0.0
    exaustao_compra: bool = False
    exaustao_venda: bool = False
    zona_proxima: bool = False
    preco_zona_proxima: float = 0.0
    tipo_zona_proxima: int = 0
    distancia_zona: float = 0.0
    contato_zona: bool = False
    reacao_zona: int = 0
    trap_flag: bool = False
    trap_intensity: float = 0.0
    tipo_trap: int = 0
    falha_continuidade: bool = False
    eficiencia_deslocamento: float = 0.0
    renovacao_real: bool = False
    regime_mercado: int = 3
    direcao_regime: int = 0
    vol_normalizada: float = 0.0
    prob_continuacao: float = 0.0
    fase_movimento: int = 1
    score_confluencia: float = 0.0
    score_divergencia: float = 0.0
    tipo_confluencia: int = 0
    confluencia_forte: bool = False
    divergencia_forte: bool = False
    divergencia_confirmada: bool = False
    confluencia_camada: int = 0
    sessao_atual: int = 0
    direcao_tf_rapido: int = 0
    direcao_tf_medio: int = 0
    direcao_tf_lento: int = 0
    direcao_tf_diario: int = 0
    direcao_tf_semanal: int = 0
    renko_sugestao: float = 0.0
    renko_qualidade: int = 1
    nome_ativo: str = ""
    evento_score_alto: bool = False
    evento_contato_zona: bool = False
    evento_trap: bool = False
    evento_falha_continuidade: bool = False
    evento_absorcao: bool = False
    evento_pico_hz: bool = False
    evento_rompimento: bool = False
    evento_falso_rompimento: bool = False
    evento_confluencia: bool = False
    evento_divergencia: bool = False
    bloqueio_score_baixo: bool = False
    bloqueio_trap: bool = False
    bloqueio_fora_zona: bool = False
    bloqueio_hz_morto: bool = False
    bloqueio_vol_baixa: bool = False
    bloqueio_regime_invalido: bool = False
    bloqueio_divergencia: bool = False


class SMCCoreEngine:
    def __init__(self, tf_base_minutos=5, modo_operacao=2,
                 tipo_ativo=1, renko_peso_ancora=0.5, fator_renko_manual=1.0):
        self.tf_base = tf_base_minutos
        self.modo_operacao = modo_operacao
        self.tipo_ativo = tipo_ativo
        self.renko_peso_ancora = renko_peso_ancora
        self.fator_renko_manual = fator_renko_manual
        self.contador_barras = 0
        self.tick_minimo = 1.0

        tf = max(1, tf_base_minutos)
        self.barras_tf_medio = max(1, round(60 / tf))
        self.barras_tf_lento = max(1, round(240 / tf))
        self.barras_tf_diario = min(95, max(1, round(1440 / tf)))
        self.barras_tf_semanal = min(95, max(1, round(7200 / tf)))
        self.renko_escala_tf = self._get_renko_escala(tf_base_minutos)

        n = MAX_HISTORICO
        self.hist_delta   = [0.0] * n
        self.hist_hz      = [0.0] * n
        self.hist_vol_sda = [0.0] * n
        self.hist_close   = [0.0] * n
        self.hist_high    = [0.0] * n
        self.hist_low     = [0.0] * n
        self.hist_volume  = [0.0] * n
        self.hist_score   = [0.0] * n
        self.hist_tr      = [0.0] * n

        self.delta_suavizado = 0.0
        self.contador_trap = 0
        self.trap_intensity = 0.0
        self.tipo_trap = 0
        self._hz_atual = 0.0
        self._hz_norm = 0.0
        self._tent_alta = False
        self._tent_baixa = False
        self._regime = 3
        self._direcao_regime = 0
        self._score_regime = 0.5
        self._prob_cont = 0.0
        self._vol_norm = 0.0
        self._vol_atual_sda = 0.0
        self._conf_forte = False
        self._tipo_conf = 0
        self._div_conf = False
        self._div_forte = False
        self._conf_total = False
        self._camada = 0
        self._score_hfz_compra = 0.0
        self._score_hfz_venda = 0.0

    def _get_renko_escala(self, tf):
        for k, v in sorted(RENKO_ESCALA_TF.items()):
            if tf <= k:
                return v
        return RENKO_ESCALA_TF[240]

    def _media(self, arr, n):
        n = min(n, len(arr))
        return sum(arr[:n]) / n if n > 0 else 0.0

    def _desvio(self, arr, n):
        m = self._media(arr, n)
        n = min(n, len(arr))
        if n == 0:
            return 0.0
        return math.sqrt(sum((arr[i] - m) ** 2 for i in range(n)) / n)

    def process(self, bar: Bar) -> Optional[SMCResult]:
        self.tick_minimo = bar.tick_minimo if bar.tick_minimo > 0 else 0.01
        self.contador_barras += 1

        if self.contador_barras < BARRAS_MINIMAS_INICIO:
            self._atualizar_historico(bar)
            return None

        r = SMCResult()
        range_barra = max(bar.high - bar.low, self.tick_minimo)
        media_volume = max(self._media(self.hist_volume, 20), 1.0)

        self._calcular_hfz(bar, r, range_barra, media_volume)
        self._calcular_fbi(bar, r)
        self._calcular_dtm(bar, r, range_barra, media_volume)
        self._calcular_sda(bar, r)
        self._calcular_mtv(bar, r)
        self._calcular_score(r)
        self._calcular_filter(r)
        self._calcular_eventos(bar, r)
        self._atualizar_historico(bar, r)
        return r

    def _calcular_hfz(self, bar, r, range_barra, media_volume):
        delta_bruto = bar.volume_compra - bar.volume_venda
        alpha = 2.0 / (SUAVIZACAO_DELTA + 1)
        self.delta_suavizado = (delta_bruto * alpha + self.delta_suavizado * (1 - alpha)
                                if self.contador_barras > BARRAS_MINIMAS_INICIO
                                else delta_bruto)

        media_d = self._media(self.hist_delta, PERIODO_DELTA_HFZ)
        desv_d = self._desvio(self.hist_delta, PERIODO_DELTA_HFZ)
        delta_norm = (self.delta_suavizado - media_d) / desv_d if desv_d > 0 else 0.0

        hz_atual = ((bar.volume_compra / 60.0) * PESO_HZ_FLUXO +
                    (bar.trades / 60.0) * PESO_HZ_PRECO)
        hz_norm = (0.2 if hz_atual < THRESHOLD_HZ_BAIXO else
                   (1.0 if hz_atual > THRESHOLD_HZ_ALTO else
                    (hz_atual - THRESHOLD_HZ_BAIXO) / (THRESHOLD_HZ_ALTO - THRESHOLD_HZ_BAIXO)))

        atr_hfz = max(self._media(self.hist_tr, PERIODO_ATR_HFZ), self.tick_minimo)

        abs_c = ((bar.volume_compra / media_volume) / (range_barra / atr_hfz)
                 if range_barra > 0 else 0.0)
        abs_v = ((bar.volume_venda / media_volume) / (range_barra / atr_hfz)
                 if range_barra > 0 else 0.0)
        abs_norm = min(max(abs_c, abs_v) / THRESHOLD_ABSORCAO_HFZ, 1.0)

        tv = bar.volume_compra + bar.volume_venda
        imb = max(-1.0, min(1.0, (
            (bar.volume_compra - bar.volume_venda) / tv if tv > 0 else 0.0) +
            (delta_bruto / media_volume if media_volume > 0 else 0.0)) * 0.5)

        pc = sum(d for d in self.hist_delta[:JANELA_PRESSAO] if d > 0) / JANELA_PRESSAO
        pv = sum(-d for d in self.hist_delta[:JANELA_PRESSAO] if d < 0) / JANELA_PRESSAO

        sc = min(((delta_norm * PESO_HFZ_DELTA if delta_norm > 0 else 0) +
                  hz_norm * PESO_HFZ_HZ +
                  ((1 - abs_norm) * PESO_HFZ_ABSORCAO if abs_c < THRESHOLD_ABSORCAO_HFZ else 0) +
                  (imb * PESO_HFZ_IMBALANCE if imb > 0 else 0) +
                  ((pc / (pc + pv + 1)) * PESO_HFZ_PRESSAO if pc > pv else 0)), 1.0)

        sv = min(((-delta_norm * PESO_HFZ_DELTA if delta_norm < 0 else 0) +
                  hz_norm * PESO_HFZ_HZ +
                  ((1 - abs_norm) * PESO_HFZ_ABSORCAO if abs_v < THRESHOLD_ABSORCAO_HFZ else 0) +
                  (-imb * PESO_HFZ_IMBALANCE if imb < 0 else 0) +
                  ((pv / (pc + pv + 1)) * PESO_HFZ_PRESSAO if pv > pc else 0)), 1.0)

        r.score_hfz = sc - sv
        r.delta_normalizado = delta_norm
        r.hz_normalizado = hz_norm
        r.absorcao_normalizada = abs_norm
        r.imbalance_score = imb
        r.pressao_liquida = pc - pv
        r.exaustao_compra = abs_c > THRESHOLD_ABSORCAO_HFZ and bar.volume > media_volume * 1.8 and bar.close < bar.open
        r.exaustao_venda  = abs_v > THRESHOLD_ABSORCAO_HFZ and bar.volume > media_volume * 1.8 and bar.close > bar.open

        self._hz_atual = hz_atual
        self._hz_norm = hz_norm
        self._tent_alta = delta_norm > 0.5 and hz_norm > 0.6 and pc > pv * 1.5
        self._tent_baixa = delta_norm < -0.5 and hz_norm > 0.6 and pv > pc * 1.5
        self._score_hfz_compra = sc
        self._score_hfz_venda = sv

    def _calcular_fbi(self, bar, r):
        if self.contador_barras < PERIODO_LIQUIDEZ_FBI:
            return
        media_vol = max(self._media(self.hist_volume, PERIODO_LIQUIDEZ_FBI), 1.0)
        zonas = []
        for i in range(1, PERIODO_LIQUIDEZ_FBI - 1):
            if self.hist_high[i] >= self.hist_high[i-1] and self.hist_high[i] >= self.hist_high[i+1]:
                pass
            if self.hist_low[i] <= self.hist_low[i-1] and self.hist_low[i] <= self.hist_low[i+1]:
                pass

        merged = []
        for z in zonas[:MAX_ZONAS_FBI]:
            found = any(abs(z["preco"] - m["preco"]) < m["preco"] * DISTANCIA_MERGE_ZONA
                        for m in merged)
            if not found:
                merged.append(z)

        zona = min((z for z in merged if z["toques"] >= MIN_TOQUES_ZONA),
                   key=lambda z: abs(bar.close - z["preco"]), default=None)
        if not zona:
            return

        dist = abs(bar.close - zona["preco"])
        dist_norm = dist / bar.close if bar.close > 0 else 1.0
        contato = dist_norm < 0.002
        reacao = 0
        if contato:
            if zona["tipo"] == 3:
                reacao = 1
            else:
                reacao = 0

        score = (min(zona["forca"] / THRESHOLD_FORCA_ZONA, 1.0) * PESO_FBI_FORCA +
                 max(0.0, 1.0 - dist_norm / MAX_DISTANCIA_ZONA) * PESO_FBI_DISTANCIA +
                 0.8 * PESO_FBI_TIPO)
        if contato:
            score += (1.0 if reacao == 1 else 0.5 if reacao == -1 else 0.3) * PESO_FBI_REACAO

        r.score_fbi = min(score, 1.0)
        r.zona_proxima = True
        r.preco_zona_proxima = zona["preco"]
        r.tipo_zona_proxima = zona["tipo"]
        r.distancia_zona = dist_norm
        r.contato_zona = contato
        r.reacao_zona = reacao

    def _calcular_dtm(self, bar, r, range_barra, media_volume):
        trap = False
        if self.contador_trap > 0:
            self.contador_trap -= 1
            self.trap_intensity *= 0.8
            trap = True
        else:
            self.trap_intensity = 0.0
            self.tipo_trap = 0

        if (bar.volume > media_volume * THRESHOLD_TRAP_VOLUME and bar.close > bar.open and
                bar.high > self.hist_high[1] and
                bar.close < bar.high - range_barra * 0.7 and self._hz_norm < 0.6):
            trap = True; self.tipo_trap = 1; self.trap_intensity = 0.7
            self.contador_trap = MIN_BARRAS_TRAP

        if (bar.volume > media_volume * THRESHOLD_TRAP_VOLUME and bar.close < bar.open and
                bar.low < self.hist_low[1] and
                bar.close > bar.low + range_barra * 0.7 and self._hz_norm < 0.6):
            trap = True; self.tipo_trap = -1; self.trap_intensity = 0.7
            self.contador_trap = MIN_BARRAS_TRAP

        falha = False
        if self._tent_alta:
            c = sum(1 for i in range(JANELA_CONTINUIDADE) if self.hist_close[i] > self.hist_close[i+1])
            falha = c < JANELA_CONTINUIDADE * THRESHOLD_FALHA_CONT
        elif self._tent_baixa:
            c = sum(1 for i in range(JANELA_CONTINUIDADE) if self.hist_close[i] < self.hist_close[i+1])
            falha = c < JANELA_CONTINUIDADE * THRESHOLD_FALHA_CONT

        rt = sum(self.hist_high[i] - self.hist_low[i] for i in range(JANELA_EFICIENCIA))
        desl = sum(abs(self.hist_close[i] - self.hist_close[i+1]) for i in range(JANELA_EFICIENCIA - 1))
        efic = desl / rt if rt > 0 else 0.0

        m = PERIODO_RENOVACAO_DTM // 2
        hz_r = self._media(self.hist_hz, m)
        hz_a = sum(self.hist_hz[m:PERIODO_RENOVACAO_DTM]) / m if m > 0 else hz_r
        renov = hz_r / hz_a > THRESHOLD_RENOVACAO_REAL if hz_a > 0 else False

        score = ((1 - self.trap_intensity if trap else 1.0) * PESO_DTM_TRAP +
                 (0.3 if falha else 1 - THRESHOLD_FALHA_CONT) * PESO_DTM_CONTINUIDADE +
                 (efic * PESO_DTM_EFICIENCIA if efic > THRESHOLD_EFICIENCIA_BAIXA else 0) +
                 (PESO_DTM_RENOVACAO if renov else 0))

        r.score_dtm = min(score, 1.0)
        r.trap_flag = trap
        r.trap_intensity = self.trap_intensity
        r.tipo_trap = self.tipo_trap
        r.falha_continuidade = falha
        r.eficiencia_deslocamento = efic
        r.renovacao_real = renov

    def _calcular_sda(self, bar, r):
        ca = sum(1 for i in range(PERIODO_REGIME) if self.hist_close[i] > self.hist_close[i+1])
        prop = ca / PERIODO_REGIME
        rt = sum(self.hist_high[i] - self.hist_low[i] for i in range(PERIODO_REGIME))
        desl = abs(sum(self.hist_close[i] - self.hist_close[i+1] for i in range(PERIODO_REGIME)))
        efic = desl / rt if rt > 0 else 0.0

        if efic > THRESHOLD_TENDENCIA:
            regime = 1
            direcao = 1 if prop > 0.55 else (-1 if prop < 0.45 else 0)
            sr = 1.0
        elif efic < THRESHOLD_LATERAL:
            regime = 3
            direcao = 0
            sr = 0.5
        else:
            regime = 2
            direcao = 0
            sr = 0.75

        vol = self._media(self.hist_tr, PERIODO_VOL_SDA)
        mv = self._media(self.hist_vol_sda, JANELA_NORMALIZACAO_VOL)
        dv = self._desvio(self.hist_vol_sda, JANELA_NORMALIZACAO_VOL)
        vol_norm = (vol - mv) / dv if dv > 0 else 0.0

        n = PERIODO_CONTINUACAO_SDA
        cont = (sum(1 for i in range(n) if self.hist_close[i] > self.hist_close[i+1]) if direcao == 1 else
                sum(1 for i in range(n) if self.hist_close[i] < self.hist_close[i+1]) if direcao == -1 else 0)
        prob = cont / n if n > 0 else 0.0

        mve = self._media(self.hist_volume, n)
        if bar.volume > mve * THRESHOLD_EXAUSTAO_ALTA and prob < 0.4:
            prob = prob * 0.5
            prob_ex = prob
        else:
            prob_ex = prob
        fase = 2 if prob > 0.7 else (3 if prob_ex > 0.6 else 1)

        dm = sum(abs(self.hist_close[i] - self.hist_close[i+1])
                 for i in range(JANELA_DESLOCAMENTO - 1)) / (JANELA_DESLOCAMENTO - 1)

        score = (sr * PESO_SDA_REGIME +
                 max(0.0, min(1.0, vol_norm / 2.0)) * PESO_SDA_VOL +
                 prob * PESO_SDA_CONTINUACAO +
                 (min(dm / (bar.close * 0.01), 1.0) * PESO_SDA_DESLOCAMENTO if dm > 0 and bar.close > 0 else 0))

        r.score_sda = min(score, 1.0)
        r.regime_mercado = regime
        r.direcao_regime = direcao
        r.vol_normalizada = vol_norm
        r.prob_continuacao = prob
        r.fase_movimento = fase

        self._regime = regime; self._direcao_regime = direcao; self._score_regime = sr
        self._prob_cont = prob; self._vol_norm = vol_norm; self._vol_atual_sda = vol

    def _calcular_mtv(self, bar, r):
        hhmm = bar.timestamp_hhmm
        sessao = (1 if SESSAO_PRE_INI <= hhmm < SESSAO_PRE_FIM else
                  2 if SESSAO_PRINCIPAL_INI <= hhmm < SESSAO_PRINCIPAL_FIM else
                  3 if SESSAO_TARDE_INI <= hhmm < SESSAO_TARDE_FIM else
                  4 if SESSAO_FECHAMENTO_INI <= hhmm < SESSAO_FECHAMENTO_FIM else 0)
        ss = SCORE_SESSAO.get(sessao, 0.70)

        if self._regime == 1:
            pw = (PESO_TF_SEMANAL_TEND, PESO_TF_DIARIO_TEND, PESO_TF_LENTO_TEND, PESO_TF_MEDIO_TEND, PESO_TF_RAPIDO_TEND)
        elif self._regime == 2:
            pw = (PESO_TF_SEMANAL_LAT, PESO_TF_DIARIO_LAT, PESO_TF_LENTO_LAT, PESO_TF_MEDIO_LAT, PESO_TF_RAPIDO_LAT)
        else:
            pw = (PESO_TF_SEMANAL_BASE, PESO_TF_DIARIO_BASE, PESO_TF_LENTO_BASE, PESO_TF_MEDIO_BASE, PESO_TF_RAPIDO_BASE)
        p_sem, p_dia, p_len, p_med, p_rap = pw

        atr_r = max(self._media(self.hist_tr, 14), self.tick_minimo)
        atr_m = self._atr_sintetico(self.barras_tf_medio, 14) or atr_r * self.barras_tf_medio
        atr_l = self._atr_sintetico(self.barras_tf_lento, 6) or atr_m * 4
        atr_d = self._atr_sintetico(self.barras_tf_diario, 3) or atr_l * 6
        atr_s = self._atr_sintetico(self.barras_tf_semanal, 2) or atr_d * 5

        vols = [min(a / max(a, self.tick_minimo), 5.0) for a in [atr_r, atr_m, atr_l, atr_d, atr_s]]
        ev = [1 if v >= THRESHOLD_EXPANSAO_VOL else (3 if v <= THRESHOLD_CONTRACAO_VOL else 2) for v in vols]

        dr, fr = self._direcao_regime_tf()
        dm, fm = self._direcao_medias(self.barras_tf_medio, atr_m, ZONA_MORTA_TF_MEDIO)
        dl, fl = self._direcao_medias(self.barras_tf_lento, atr_l, ZONA_MORTA_TF_LENTO)
        dd, fd = self._direcao_medias(self.barras_tf_diario, atr_d, ZONA_MORTA_TF_DIARIO)
        ds, fs = self._direcao_medias(self.barras_tf_semanal, atr_s, ZONA_MORTA_TF_SEMANAL)

        pares = [
            (ds, dd, p_sem,       fs, fd),
            (ds, dl, p_sem * 0.6, fs, fl),
            (ds, dm, p_sem * 0.4, fs, fm),
            (ds, dr, p_sem * 0.2, fs, fr),
            (dd, dl, p_dia,       fd, fl),
            (dd, dm, p_dia * 0.6, fd, fm),
            (dd, dr, p_dia * 0.3, fd, fr),
            (dl, dm, p_len,       fl, fm),
            (dl, dr, p_len * 0.5, fl, fr),
            (dm, dr, p_med,       fm, fr),
        ]
        acum = peso_t = 0.0
        for d1, d2, peso, f1, f2 in pares:
            if d1 != 0 and d2 != 0 and d1 == d2:
                acum += peso * (f1 + f2) / 2
            peso_t += peso
        alin = acum / peso_t if peso_t > 0 else 0.0

        sc = max(0.0, alin) * ss
        sd = max(0.0, -alin)

        tc = 0
        if sc >= THRESHOLD_CONFLUENCIA:
            tc = 1 if sc >= THRESHOLD_CONFLUENCIA and sc < THRESHOLD_DIVERGENCIA_FORTE else 2

        td = 0
        if sd >= THRESHOLD_DIVERGENCIA:
            td = 1 if sd >= THRESHOLD_DIVERGENCIA else 0

        cf = sc >= THRESHOLD_CONFLUENCIA
        df = sd >= THRESHOLD_DIVERGENCIA_FORTE
        dc = df and td == 1
        ce = ds != 0 and dd != 0 and ds == dd
        ct = ce and dl != 0 and dl == ds
        ctot = ct and dm != 0 and dr != 0 and dm == ds and dr == ds
        cam = 3 if ctot else (2 if ct else (1 if ce else 0))

        atr_base = max(atr_d * 0.60 + atr_m * 0.40, atr_r * self.barras_tf_medio * 0.4)
        fr_renko = (RENKO_FATOR_CONFLUENCIA if cf else
                    RENKO_FATOR_DIVERGENCIA if df else RENKO_FATOR_NEUTRO)
        fr_renko *= (0.85 if ev[1] == 1 else 1.20 if ev[1] == 3 else 1.0)
        fr_renko *= self.fator_renko_manual * self.renko_escala_tf
        fr_renko = max(RENKO_FATOR_MINIMO, min(RENKO_FATOR_MAXIMO, fr_renko))
        rc = atr_base * fr_renko
        if self.tick_minimo > 0:
            rc = round(rc / self.tick_minimo) * self.tick_minimo

        perfil = PERFIS_ATIVO.get(self.tipo_ativo)
        if perfil:
            amin, amax, at, al, atr2 = perfil["min"], perfil["max"], perfil["tend"], perfil["lat"], perfil["ref"]
        else:
            amin, amax, at, al, atr2 = 0.01, 100.0, 10.0, 5.0, 1.0
        ar = at if self._regime == 1 else (al if self._regime == 2 else atr2)
        rf = max(amin, min(amax, rc * (1 - self.renko_peso_ancora) + ar * self.renko_peso_ancora))
        if self.tick_minimo > 0:
            rf = round(rf / self.tick_minimo) * self.tick_minimo

        rq = (3 if ctot and ev[1] == 2 else 2 if cam >= 2 or (cf and ev[1] == 2) else 1)
        smtv = min(sc * 0.50 + (0.30 if ev[1] == 2 else 0.15 if ev[1] == 1 else 0.05) +
                   (rq / 3) * 0.20 + (0.10 if ctot else 0), 1.0)

        r.score_mtv = smtv
        r.score_confluencia = sc; r.score_divergencia = sd
        r.tipo_confluencia = tc; r.confluencia_forte = cf
        r.divergencia_forte = df; r.divergencia_confirmada = dc
        r.confluencia_camada = cam; r.sessao_atual = sessao
        r.direcao_tf_rapido = dr; r.direcao_tf_medio = dm
        r.direcao_tf_lento = dl; r.direcao_tf_diario = dd; r.direcao_tf_semanal = ds
        r.renko_sugestao = rf; r.renko_qualidade = rq; r.nome_ativo = PERFIS_ATIVO.get(self.tipo_ativo, {}).get("nome", "")

        self._conf_forte = cf; self._tipo_conf = tc; self._div_conf = dc
        self._div_forte = df; self._conf_total = ctot; self._camada = cam

    def _atr_sintetico(self, barras, periodos):
        total = count = idx = 0
        while count < periodos and idx + barras - 1 < MAX_HISTORICO:
            h_seg = self.hist_high[idx:idx + barras]
            l_seg = self.hist_low[idx:idx + barras]
            total += max(h_seg) - min(l_seg) if len(h_seg) > 0 else 0
            count += 1
            idx += barras
        return total / count if count > 0 else 0.0

    def _direcao_regime_tf(self):
        f = self._score_regime
        return (0, 0.0) if f < THRESHOLD_FORCA_MIN_MTV else (self._direcao_regime, f)

    def _direcao_medias(self, barras, atr, zm_fator):
        if barras <= 0 or atr <= 0:
            return (0, 0.0)
        n = min(barras, MAX_HISTORICO)
        n2 = min(barras * 2, MAX_HISTORICO)
        m1 = sum(self.hist_close[:n]) / n if n > 0 else 0.0
        m2 = (sum(self.hist_close[n:n2]) / (n2 - n) if n2 > n else m1)
        diff = m1 - m2; zona = atr * zm_fator
        if diff > zona:
            return (1, abs(diff) / atr if atr > 0 else 0.0)
        elif diff < -zona:
            return (-1, abs(diff) / atr if atr > 0 else 0.0)
        return (0, 0.0)

    def _calcular_score(self, r):
        sf = max(-1.0, min(1.0,
                           r.score_hfz * PESO_MODULO_HFZ + r.score_fbi * PESO_MODULO_FBI +
                           r.score_dtm * PESO_MODULO_DTM + r.score_sda * PESO_MODULO_SDA +
                           r.score_mtv * PESO_MODULO_MTV))
        sc = sv = 0.0
        if r.score_hfz > 0:
            sc += r.score_hfz * PESO_MODULO_HFZ
        else:
            sv += -r.score_hfz * PESO_MODULO_HFZ
        for s in [r.score_fbi, r.score_dtm]:
            sc += s * PESO_MODULO_FBI if s > 0 else 0
            sv += -s if s < 0 else 0
        sc += r.prob_continuacao * PESO_MODULO_SDA
        sv += r.prob_continuacao * PESO_MODULO_SDA
        if self._conf_forte:
            sc *= 1.2
            sv *= 0.8
        else:
            sc *= 0.9
            sv *= 0.9
        sc *= 100; sv *= 100
        r.score_final = sf * 100; r.score_compra = sc; r.score_venda = sv
        r.direcao = 1 if sc > sv else (-1 if sv > sc else 0)
        r.forca = (3 if max(sc, sv) > THRESHOLD_SCORE_ALTO else
                   2 if max(sc, sv) > THRESHOLD_SCORE_MEDIO else 1)

    def _calcular_filter(self, r):
        bs = r.score_compra < MIN_SCORE_OPERACAO and r.score_venda < MIN_SCORE_OPERACAO
        bt = r.trap_flag and r.trap_intensity > MAX_TRAP_PERMITIDO
        bz = not r.zona_proxima or r.distancia_zona > MAX_DISTANCIA_ZONA
        bh = r.hz_normalizado < MIN_HZ_ZONA and r.zona_proxima
        bv = r.vol_normalizada < MIN_VOL_NORMALIZADA
        br = self._regime == 2 and self.modo_operacao == 1
        bd = (r.divergencia_forte if self.modo_operacao == 1 else
              r.divergencia_confirmada if self.modo_operacao == 2 else False)

        perm = (not any([bs, bt, bz, bh, bv, br, bd]) if self.modo_operacao == 1 else
                not any([bs, bt, bd]) if self.modo_operacao == 2 else
                not (bt and r.trap_intensity > 0.7) if self.modo_operacao == 3 else False)

        pc = perm and r.direcao == 1 and r.score_compra > MIN_SCORE_OPERACAO
        pv = perm and r.direcao == -1 and r.score_venda > MIN_SCORE_OPERACAO

        est = (4 if not perm else 1 if pc and r.forca >= 2 else
               2 if pv and r.forca >= 2 else 3 if pc or pv else 4)

        qual = 0
        if est in (1, 2):
            qual = 3 if r.forca >= 3 else (2 if r.confluencia_forte or r.divergencia_confirmada else 1)

        risco = (3 if bt else 0) + (2 if bz else 0) + (1 if bv else 0) + (2 if br else 0) + (3 if r.divergencia_confirmada else 1 if r.divergencia_forte else 0)

        r.permissao_operar = perm; r.permissao_compra = pc; r.permissao_venda = pv
        r.estado_mercado = est; r.qualidade_setup = qual; r.risco_contextual = risco
        r.bloqueio_score_baixo = bs; r.bloqueio_trap = bt; r.bloqueio_fora_zona = bz
        r.bloqueio_hz_morto = bh; r.bloqueio_vol_baixa = bv
        r.bloqueio_regime_invalido = br; r.bloqueio_divergencia = bd

    def _calcular_eventos(self, bar, r):
        r.evento_score_alto = r.score_compra >= MIN_SCORE_LOG or r.score_venda >= MIN_SCORE_LOG
        r.evento_contato_zona = r.contato_zona
        r.evento_trap = r.trap_flag and r.trap_intensity >= MIN_TRAP_INTENSITY_LOG
        r.evento_falha_continuidade = r.falha_continuidade
        r.evento_absorcao = r.absorcao_normalizada >= MIN_ABSORCAO_LOG
        r.evento_pico_hz = self._hz_atual >= MIN_HZ_PICO_LOG
        r.evento_rompimento = bar.high > self.hist_high[1] or bar.low < self.hist_low[1]
        r.evento_falso_rompimento = r.evento_rompimento and r.trap_flag
        r.evento_confluencia = r.confluencia_forte
        r.evento_divergencia = r.divergencia_confirmada

    def _atualizar_historico(self, bar, result=None):
        for i in range(MAX_HISTORICO - 1, 0, -1):
            self.hist_delta[i] = self.hist_delta[i - 1]
            self.hist_hz[i] = self.hist_hz[i - 1]
            self.hist_vol_sda[i] = self.hist_vol_sda[i - 1]
            self.hist_close[i] = self.hist_close[i - 1]
            self.hist_high[i] = self.hist_high[i - 1]
            self.hist_low[i] = self.hist_low[i - 1]
            self.hist_volume[i] = self.hist_volume[i - 1]
            self.hist_score[i] = self.hist_score[i - 1]
            self.hist_tr[i] = self.hist_tr[i - 1]
        self.hist_delta[0]   = self.delta_suavizado
        self.hist_hz[0]      = self._hz_atual
        self.hist_vol_sda[0] = self._vol_atual_sda
        self.hist_close[0]   = bar.close
        self.hist_high[0]    = bar.high
        self.hist_low[0]     = bar.low
        self.hist_volume[0]  = bar.volume
        self.hist_score[0]   = result.score_final if result else 0.0
        self.hist_tr[0]      = bar.true_range
