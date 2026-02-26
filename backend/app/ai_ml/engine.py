"""
Módulo AI/ML - Integração LLM e Aprendizado Contínuo
Utiliza OpenAI GPT para análise contextual e melhoria do sistema
"""
import asyncio
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from app.config import settings

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """Analisador de contexto com LLM"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL
        
        if self.api_key:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def analyze_signal(self, signal_data: Dict) -> Dict:
        """Analisa sinal com contexto LLM"""
        if not self.client:
            return {'status': 'skipped', 'reason': 'LLM não configurado'}
        
        try:
            prompt = self._build_analysis_prompt(signal_data)
            
            message = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Você é um analista de trading profissional especializado em 
                        análise de microestrutura de mercado utilizando o sistema SMC. Analise os sinais
                        com foco em risco, confirmação e contexto de mercado."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            analysis_text = message.choices[0].message.content
            
            return {
                'status': 'success',
                'analysis': analysis_text,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Erro ao analisar com LLM: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _build_analysis_prompt(self, signal_data: Dict) -> str:
        """Constrói prompt para análise"""
        prompt = f"""
        Analise o seguinte sinal de trading:
        
        **Tipo de Sinal:** {signal_data.get('type')}
        **Score:** {signal_data.get('score')}
        **Preço Atual:** {signal_data.get('price')}
        **Contexto de Mercado:** {signal_data.get('regime')}
        
        **Scores dos Módulos SMC:**
        - HFZ (Microestrutura): {signal_data.get('hfz_score')}
        - FBI (Zonas Institucionais): {signal_data.get('fbi_score')}
        - DTM (Validação): {signal_data.get('dtm_score')}
        - SDA (Regime): {signal_data.get('sda_score')}
        - MTV (Multi-TF): {signal_data.get('mtv_score')}
        
        **Detalhes:**
        {signal_data.get('details', 'N/A')}
        
        Por favor, forneça:
        1. Confirmação do sinal (forte/médio/fraco)
        2. Pontos de risco principais
        3. Recomendação de ação
        4. Sugestões de stop loss e take profit
        """
        
        return prompt
    
    async def evaluate_trade_outcome(self, trade_data: Dict) -> Dict:
        """Avalia resultado de trade para aprendizado"""
        if not self.client:
            return {'status': 'skipped'}
        
        try:
            prompt = f"""
            Analise o resultado deste trade para aprendizado contínuo:
            
            **Sinal Iniciál:** {trade_data.get('signal_type')}
            **Score:** {trade_data.get('initial_score')}
            **Entry Price:** {trade_data.get('entry_price')}
            **Exit Price:** {trade_data.get('exit_price')}
            **P&L:** {trade_data.get('pnl')}
            **Duração:** {trade_data.get('duration')}
            
            Identifique padrões para melhoria no sistema.
            """
            
            message = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            return {
                'status': 'success',
                'evaluation': message.choices[0].message.content
            }
        
        except Exception as e:
            logger.error(f"Erro ao avaliar trade: {str(e)}")
            return {'status': 'error'}


class MachineLearningEngine:
    """Engine de Machine Learning para aprendizado contínuo"""
    
    def __init__(self):
        self.historical_signals = []
        self.signal_outcomes = []
        self.model = None
    
    def add_signal(self, signal: Dict) -> None:
        """Adiciona sinal ao histórico (com tamanho limitado)"""
        self.historical_signals.append({
            'timestamp': datetime.now().isoformat(),
            **signal
        })
        # manter buffer de tamanho limitado para evitar consumo infinito
        max_history = 5000
        if len(self.historical_signals) > max_history:
            self.historical_signals.pop(0)
    
    def add_outcome(self, signal_id: str, outcome: Dict) -> None:
        """Adiciona resultado de sinal"""
        self.signal_outcomes.append({
            'signal_id': signal_id,
            'timestamp': datetime.now().isoformat(),
            **outcome
        })
        # opcional: limitar histórico de outcomes
        max_outcomes = 5000
        if len(self.signal_outcomes) > max_outcomes:
            self.signal_outcomes.pop(0)
    
    def extract_features(self, signal: Dict) -> np.ndarray:
        """Extrai features de um sinal para ML"""
        features = [
            signal.get('hfz_score', 0),
            signal.get('fbi_score', 0), 
            signal.get('dtm_score', 0),
            signal.get('sda_score', 0),
            signal.get('mtv_score', 0),
            signal.get('confluencia_level', 0),
            signal.get('volatility', 0),
            signal.get('volume_ratio', 1),
        ]
        
        return np.array(features)
    
    def train_model(self) -> Dict:
        """Treina modelo com histórico"""
        try:
            from sklearn.ensemble import RandomForestRegressor
            
            if len(self.historical_signals) < 10:
                return {'status': 'insufficient_data'}
            
            # Preparar dados
            X = []
            y = []
            
            for signal in self.historical_signals:
                features = self.extract_features(signal)
                X.append(features)
                y.append(signal.get('score', 0.5))
            
            X = np.array(X)
            y = np.array(y)
            
            # Treinar modelo
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            
            logger.info(f"Modelo treinado com {len(X)} amostras")
            
            return {
                'status': 'success',
                'samples': len(X),
                'model_type': 'RandomForest'
            }
        
        except Exception as e:
            logger.error(f"Erro ao treinar modelo: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def predict(self, signal: Dict) -> float:
        """Prediz score melhorado para sinal"""
        if self.model is None:
            return signal.get('score', 0.5)
        
        try:
            features = self.extract_features(signal)
            predicted_score = float(self.model.predict([features])[0])
            
            return min(1.0, max(0.0, predicted_score))
        
        except Exception as e:
            logger.error(f"Erro ao predizer: {str(e)}")
            return signal.get('score', 0.5)
    
    def get_feature_importance(self) -> Dict:
        """Retorna importância das features"""
        if self.model is None:
            return {}
        
        features_names = [
            'HFZ', 'FBI', 'DTM', 'SDA', 'MTV',
            'Confluência', 'Volatilidade', 'Volume'
        ]
        
        importances = self.model.feature_importances_
        
        return {
            name: float(imp) for name, imp in zip(features_names, importances)
        }


class AdaptiveSignalRefinement:
    """Refinamento adaptativo de sinais baseado em performance"""
    
    def __init__(self):
        self.win_rate_by_type = {}
        self.avg_profit_by_confluencia = {}
        self.adjustment_factors = {}
    
    def update_performance_metrics(self, outcome: Dict) -> None:
        """Atualiza métricas de performance"""
        signal_type = outcome.get('signal_type')
        confluencia = outcome.get('confluencia_level', 0)
        pnl = outcome.get('pnl', 0)
        
        # Atualizar win rate por tipo
        if signal_type not in self.win_rate_by_type:
            self.win_rate_by_type[signal_type] = {'wins': 0, 'losses': 0}
        
        if pnl > 0:
            self.win_rate_by_type[signal_type]['wins'] += 1
        else:
            self.win_rate_by_type[signal_type]['losses'] += 1
        
        # Atualizar profit por confluência
        conf_bucket = f"{int(confluencia*10)}/10"
        if conf_bucket not in self.avg_profit_by_confluencia:
            self.avg_profit_by_confluencia[conf_bucket] = []
        
        self.avg_profit_by_confluencia[conf_bucket].append(pnl)
    
    def get_score_adjustment(self, signal: Dict) -> float:
        """Calcula ajuste de score baseado em performance histórica"""
        signal_type = signal.get('type')
        confluencia = signal.get('confluencia_level', 0)
        
        adjustment = 1.0
        
        # Ajustar por histórico de win rate
        if signal_type in self.win_rate_by_type:
            metrics = self.win_rate_by_type[signal_type]
            total = metrics['wins'] + metrics['losses']
            
            if total > 0:
                win_rate = metrics['wins'] / total
                adjustment *= (0.9 + (win_rate * 0.2))  # 0.9 a 1.1
        
        # Ajustar por confluência
        conf_bucket = f"{int(confluencia*10)}/10"
        if conf_bucket in self.avg_profit_by_confluencia:
            profits = self.avg_profit_by_confluencia[conf_bucket]
            avg_profit = np.mean(profits) if profits else 0
            
            if avg_profit > 0:
                adjustment *= 1.1
            elif avg_profit < 0:
                adjustment *= 0.9
        
        return adjustment


# Instâncias
llm_analyzer = LLMAnalyzer()
ml_engine = MachineLearningEngine()
signal_refinement = AdaptiveSignalRefinement()
