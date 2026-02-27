"""
AI Engine - Stub Implementation
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class AIConfig:
    provider: str = "openai"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    modo_simulacao: bool = True

class AIEngine:
    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()

    async def analyze_setup(self, bar_data: dict) -> dict:
        """Analyze trading setup using AI"""
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "recommendation": "HOLD"
        }

    async def generate_signal_explanation(self, score_data: dict) -> str:
        """Generate explanation for trading signal"""
        return "Signal analysis pending"

    async def predict_next_movement(self, historical_data: list) -> dict:
        """Predict next price movement"""
        return {
            "direction": 0,
            "probability": 0.5,
            "target_price": None
        }
