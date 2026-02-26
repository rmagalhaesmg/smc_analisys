"""
Módulo FBI - Contexto Espacial e Zonas Institucionais
Análise de support/resistance e reações em zonas críticas
"""
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Zone:
    """Representa uma zona de preço"""
    price: float
    volume: float
    touches: int
    zone_type: int  # 1=Suporte, 3=Resistência
    strength: float
    active: bool


@dataclass
class FBIResult:
    """Resultado da análise FBI"""
    zona_proxima: bool
    preco_zona: float
    tipo_zona: int
    forca_zona: float
    distancia_normalizada: float
    contato_zona: bool
    reacao_zona: int
    score_fbi: float


class FBIModule:
    """Módulo de análise de contexto espacial e zonas"""
    
    def __init__(self):
        self.periodo_liquidez = 30
        self.threshold_liquidez_alta = 1.8
        self.min_toques = 1
        self.distancia_merge = 0.003
        self.max_zonas = 20
        self.min_barras_zona = 5
        self.threshold_forca_zona = 1.5
        self.max_distancia_zona = 0.050
        
        # Pesos
        self.peso_forca = 0.40
        self.peso_distancia = 0.30
        self.peso_tipo = 0.20
        self.peso_reacao = 0.10
        
        self.zones: List[Zone] = []
        self.hist_high = np.zeros(100)
        self.hist_low = np.zeros(100)
        self.hist_volume = np.zeros(100)
    
    def update_history(self, high: float, low: float, volume: float):
        """Atualiza histórico de preços e volume"""
        self.hist_high = np.roll(self.hist_high, 1)
        self.hist_high[0] = high
        
        self.hist_low = np.roll(self.hist_low, 1)
        self.hist_low[0] = low
        
        self.hist_volume = np.roll(self.hist_volume, 1)
        self.hist_volume[0] = volume
    
    def _identify_zones(self):
        """Identifica zonas de preço (suporte/resistência)"""
        if len(self.hist_high) < self.periodo_liquidez:
            return
        
        self.zones = []
        media_volume = np.mean(self.hist_volume[:self.periodo_liquidez])
        if media_volume <= 0:
            media_volume = 1
        
        # Identificar topos e fundos
        for i in range(1, self.periodo_liquidez - 1):
            # Topos (resistência)
            if (self.hist_high[i] >= self.hist_high[i-1] and 
                self.hist_high[i] >= self.hist_high[i+1] and 
                len(self.zones) < self.max_zonas):
                
                # Verificar se já existe zona próxima
                zone_exists = False
                for zone in self.zones:
                    if abs(self.hist_high[i] - zone.price) < \
                       self.hist_high[i] * self.distancia_merge:
                        zone.touches += 1
                        zone_exists = True
                        break
                
                if not zone_exists:
                    strength = min(1.0, self.hist_volume[i] / media_volume)
                    new_zone = Zone(
                        price=self.hist_high[i],
                        volume=self.hist_volume[i],
                        touches=1,
                        zone_type=3,  # Resistência
                        strength=strength,
                        active=True
                    )
                    self.zones.append(new_zone)
            
            # Fundos (suporte)
            if (self.hist_low[i] <= self.hist_low[i-1] and 
                self.hist_low[i] <= self.hist_low[i+1] and 
                len(self.zones) < self.max_zonas):
                
                zone_exists = False
                for zone in self.zones:
                    if abs(self.hist_low[i] - zone.price) < \
                       self.hist_low[i] * self.distancia_merge:
                        zone.touches += 1
                        zone_exists = True
                        break
                
                if not zone_exists:
                    strength = min(1.0, self.hist_volume[i] / media_volume)
                    new_zone = Zone(
                        price=self.hist_low[i],
                        volume=self.hist_volume[i],
                        touches=1,
                        zone_type=1,  # Suporte
                        strength=strength,
                        active=True
                    )
                    self.zones.append(new_zone)
    
    def _find_nearest_zone(self, current_price: float) -> Tuple[bool, float, int, float, float]:
        """Encontra a zona mais próxima"""
        nearest_zone = None
        min_distance = float('inf')
        
        for zone in self.zones:
            if zone.active and zone.touches >= self.min_toques:
                distance = abs(current_price - zone.price)
                if distance < min_distance:
                    min_distance = distance
                    nearest_zone = zone
        
        if nearest_zone is None:
            return False, 0, 0, 0, 0
        
        if current_price > 0:
            distancia_normalizada = min_distance / current_price
        else:
            distancia_normalizada = 0
        
        return True, nearest_zone.price, nearest_zone.zone_type, \
               nearest_zone.strength, distancia_normalizada
    
    def analyze(self, current_price: float, high: float, low: float, 
               open_: float, close: float, volume: float) -> FBIResult:
        """
        Executa análise completa FBI
        
        Args:
            current_price: Preço atual (close)
            high: Máxima da barra
            low: Mínima da barra
            open_: Abertura
            close: Fechamento
            volume: Volume
            
        Returns:
            FBIResult com análise de zonas
        """
        self._identify_zones()
        
        zona_proxima, preco_zona, tipo_zona, forca_zona, distancia_norm = \
            self._find_nearest_zone(current_price)
        
        # Verificar contato em zona
        contato = zona_proxima and (distancia_norm < 0.002)
        
        # Reação em zona
        reacao = 0
        if contato:
            if tipo_zona == 3:  # Resistência
                if close < open_:
                    reacao = 1  # Rejeição (negativo)
                elif close > preco_zona:
                    reacao = 0  # Rompimento
                else:
                    reacao = -1  # Falsa continuação
            elif tipo_zona == 1:  # Suporte
                if close > open_:
                    reacao = 1  # Continuação (positivo)
                elif close < preco_zona:
                    reacao = 0  # Quebra
                else:
                    reacao = -1  # Falso suporte
        
        # Score FBI
        score_fbi = 0.0
        
        if zona_proxima:
            # Forca da zona
            if forca_zona > self.threshold_forca_zona:
                strength_score = 1.0
            else:
                strength_score = forca_zona / self.threshold_forca_zona
            
            score_fbi += strength_score * self.peso_forca
            
            # Distancia
            distancia_score = max(0, 1 - (distancia_norm / self.max_distancia_zona))
            score_fbi += distancia_score * self.peso_distancia
            
            # Tipo de zona
            tipo_score = 0.8  # Ambas suporte e resistência têm valor
            score_fbi += tipo_score * self.peso_tipo
            
            # Reação
            if contato:
                if reacao == 1:
                    reacao_score = 1.0
                elif reacao == -1:
                    reacao_score = 0.5
                else:
                    reacao_score = 0.3
                
                score_fbi += reacao_score * self.peso_reacao
        
        score_fbi = min(1.0, score_fbi)
        
        return FBIResult(
            zona_proxima=zona_proxima,
            preco_zona=preco_zona if zona_proxima else 0,
            tipo_zona=tipo_zona,
            forca_zona=forca_zona,
            distancia_normalizada=distancia_norm,
            contato_zona=contato,
            reacao_zona=reacao,
            score_fbi=score_fbi
        )
