"""
AQ-NHE Configuration Settings
Centralized configuration management with environment variables and default values
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    database_url: str
    
    def __post_init__(self):
        """Validate Firebase configuration"""
        if not all([self.project_id, self.private_key, self.client_email]):
            raise ValueError("Missing required Firebase credentials")
        # Clean private key formatting
        self.private_key = self.private_key.replace('\\n', '\n')

@dataclass
class TradingConfig:
    """Trading-specific configuration"""
    exchange: str = "binance"
    timeframe: str = "1h"
    max_position_size: float = 0.1  # 10% of capital
    max_strategies: int = 100
    backtest_days: int = 365

@dataclass
class QuantumNeuroConfig:
    """Quantum-Neuro algorithm configuration"""
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    quantum_bits: int = 10
    neuro_layers: list = None
    
    def __post_init__(self):
        if self.neuro_layers is None:
            self.neuro_layers = [64, 32, 16, 8]

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/aq_nhe.log"

class AQNHEConfig:
    """Main configuration class"""
    
    def __init__(self):
        self._validate_environment()
        
        # Initialize Firebase config
        self.firebase = FirebaseConfig(
            project_id=os.getenv("FIREBASE_PROJECT_ID", ""),
            private_key_id=os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
            private_key=os.getenv("FIREBASE_PRIVATE_KEY", ""),
            client_email=os.getenv("FIREBASE_CLIENT_EMAIL", ""),
            client_id=os.getenv("FIREBASE_CLIENT_ID", ""),
            database_url=os.getenv("FIREBASE_DATABASE_URL", "")
        )
        
        self.trading = TradingConfig()
        self.quantum_neuro = QuantumNeuroConfig()
        self.logging = LoggingConfig()
        
        # Performance thresholds
        self.min_sharpe_ratio: float = 1.0
        self.max_drawdown: float = -0.2
        self.min_win_rate: float = 0.55
    
    def _validate_environment(self) -> None:
        """Validate required environment variables"""
        required_vars = ["FIREBASE_PROJECT_ID", "FIREBASE_PRIVATE_KEY", "FIREBASE_CLIENT_EMAIL"]
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Please set these in your .env file or environment."
            )

# Global configuration instance
config = AQNHEConfig()