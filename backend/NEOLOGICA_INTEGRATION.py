"""
Exemplo de Integração com Neológica RTD
Esta classe pode ser usada para conectar ao sistema RTD da Neológica
e enviar dados em tempo real para análise
"""

import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp

# Exemplo 1: Integração via HTTP API (método mais simples)
class NeologicaAPIIntegration:
    """Integração com Neológica via HTTP API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.neologica.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def connect(self):
        """Conecta ao serviço"""
        self.session = aiohttp.ClientSession()
    
    async def disconnect(self):
        """Desconecta do serviço"""
        if self.session:
            await self.session.close()
    
    async def fetch_candle(self, ticker: str, timeframe: int = 5) -> Dict:
        """
        Obtém último candle do ativo
        
        Args:
            ticker: Código do ativo (ex: WIN@H25)
            timeframe: Timeframe em minutos
            
        Returns:
            Dicionário com dados do candle
        """
        try:
            url = f"{self.base_url}/candles/latest"
            params = {
                'ticker': ticker,
                'timeframe': timeframe,
                'api_key': self.api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._format_candle(data, ticker)
                else:
                    return None
        
        except Exception as e:
            print(f"Erro ao buscar candle: {e}")
            return None
    
    async def subscribe_stream(self, tickers: List[str], callback):
        """
        Subscreve a stream de dados em tempo real
        
        Args:
            tickers: Lista de ativos
            callback: Função async para processar cada candle
        """
        try:
            url = f"{self.base_url}/stream"
            params = {
                'tickers': ','.join(tickers),
                'api_key': self.api_key
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    async for line in response.content:
                        if line:
                            data = json.loads(line)
                            candle = self._format_candle(data, data.get('ticker'))
                            await callback(candle)
        
        except Exception as e:
            print(f"Erro ao subscrever stream: {e}")
    
    def _format_candle(self, raw_data: Dict, ticker: str) -> Dict:
        """Formata dados da Neológica para formato SMC"""
        return {
            'ticker': ticker,
            'timestamp': raw_data.get('time', datetime.now().isoformat()),
            'open': float(raw_data.get('open', 0)),
            'high': float(raw_data.get('high', 0)),
            'low': float(raw_data.get('low', 0)),
            'close': float(raw_data.get('close', 0)),
            'volume': int(raw_data.get('volume', 0)),
            'trades': int(raw_data.get('trades', 0)),
            'aggression_buy': float(raw_data.get('aggression_buy', 0)),
            'aggression_sell': float(raw_data.get('aggression_sell', 0)),
        }


# Exemplo 2: Integração com Profit (via RTD/DDE - Windows COM)
class ProfitRTDIntegration:
    """
    Integração com Profit via RTD (Real-Time Data)
    Requer: Neológica Profit instalado, pytdx ou pyuno
    """
    
    def __init__(self):
        self.rtd_server = None
        try:
            import pythoncom
            from win32com import client
            self.pythoncom = pythoncom
            self.client = client
            self.available = True
        except ImportError:
            print("Aviso: pywin32 não instalado. RTD não disponível.")
            self.available = False
    
    def connect_rtd(self):
        """Conecta ao server RTD do Profit"""
        if not self.available:
            raise RuntimeError("RTD não disponível. Instale: pip install pywin32")
        
        try:
            self.rtd_server = self.client.GetObject("rtd:neologica.rtdserver")
            print("Conectado ao RTD da Neológica")
            return True
        except Exception as e:
            print(f"Erro ao conectar RTD: {e}")
            return False
    
    def get_price(self, ticker: str) -> float:
        """Obtém preço do ativo via RTD"""
        try:
            value = self.rtd_server.RTD("Neologica", "", ticker, "price")
            return float(value)
        except Exception as e:
            print(f"Erro ao obter preço: {e}")
            return 0
    
    def get_volume(self, ticker: str) -> int:
        """Obtém volume do ativo via RTD"""
        try:
            value = self.rtd_server.RTD("Neologica", "", ticker, "volume")
            return int(value)
        except Exception as e:
            print(f"Erro ao obter volume: {e}")
            return 0
    
    def get_bid_ask(self, ticker: str) -> tuple:
        """Obtém bid/ask do ativo via RTD"""
        try:
            bid = float(self.rtd_server.RTD("Neologica", "", ticker, "bid"))
            ask = float(self.rtd_server.RTD("Neologica", "", ticker, "ask"))
            return bid, ask
        except Exception as e:
            print(f"Erro ao obter bid/ask: {e}")
            return 0, 0


# Exemplo 3: Integração com DLL (via ctypes)
class NeologicaDLLIntegration:
    """
    Integração com Neológica via DLL
    Requer: neologica.dll ou equivalente
    """
    
    def __init__(self, dll_path: str = "C:\\Program Files\\Neologica\\neologica.dll"):
        self.dll_path = dll_path
        self.dll = None
        
        try:
            import ctypes
            self.ctypes = ctypes
            self.dll = ctypes.CDLL(dll_path)
            print(f"DLL carregada: {dll_path}")
        except Exception as e:
            print(f"Erro ao carregar DLL: {e}")
    
    def get_candle(self, ticker: str, timeframe: int = 5) -> Dict:
        """Obtém candle via DLL"""
        if not self.dll:
            return None
        
        try:
            # Exemplo de chamada a função DLL
            # A sintaxe exata depende da DLL específica
            result = self.dll.GetCandle(
                self.ctypes.c_char_p(ticker.encode()),
                self.ctypes.c_int(timeframe)
            )
            
            # Parsear resultado (adaptar conforme retorno da DLL)
            return {
                'ticker': ticker,
                'open': result.open,
                'high': result.high,
                'low': result.low,
                'close': result.close,
                'volume': result.volume,
            }
        
        except Exception as e:
            print(f"Erro ao chamar DLL: {e}")
            return None


# Exemplo 4: Script de teste
async def test_integration():
    """Testa integração com Neológica"""
    
    # Testar API HTTP
    print("\\n=== Testando API HTTP ===")
    api = NeologicaAPIIntegration(api_key="seu_api_key_aqui")
    await api.connect()
    
    candle = await api.fetch_candle("WIN@H25", timeframe=5)
    if candle:
        print(f"Candle obtido:")
        print(f"  Preço de fechamento: {candle['close']}")
        print(f"  Volume: {candle['volume']}")
    
    await api.disconnect()
    
    # Testar RTD (Windows only)
    print("\\n=== Testando RTD (Windows) ===")
    rtd = ProfitRTDIntegration()
    if rtd.connect_rtd():
        price = rtd.get_price("WIN@H25")
        volume = rtd.get_volume("WIN@H25")
        bid, ask = rtd.get_bid_ask("WIN@H25")
        
        print(f"Preço: {price}")
        print(f"Volume: {volume}")
        print(f"Bid/Ask: {bid} / {ask}")


# Uso com SMC Web App
if __name__ == "__main__":
    # Exemplo: como usar com o SMC Web App
    
    # 1. Setup da integração
    neologica_api = NeologicaAPIIntegration(api_key="seu_api_key")
    
    # 2. Buscar candle
    import asyncio
    async def main():
        await neologica_api.connect()
        
        # Buscar dados
        candle = await neologica_api.fetch_candle("WIN@H25")
        
        # 3. Enviar para análise SMC
        # Você pode enviar data para: http://localhost:8000/analyze/candle
        if candle:
            import requests
            response = requests.post(
                "http://localhost:8000/analyze/candle",
                json=candle
            )
            print(f"Análise SMC: {response.json()}")
        
        await neologica_api.disconnect()
    
    asyncio.run(main())
