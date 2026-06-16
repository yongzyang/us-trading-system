"""
Base strategy class for all trading strategies.
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Optional
from logger import setup_logger


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    """
    
    def __init__(self, name: str):
        """
        Initialize strategy.
        
        Args:
            name: Strategy name
        """
        self.name = name
        self.logger = setup_logger(self.__class__.__name__)
        self.signals = []
        self.positions = []
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> List[int]:
        """
        Generate trading signals.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            List of signals: 1 (buy), -1 (sell), 0 (hold)
        """
        pass
    
    def on_bar(self, current_data: pd.DataFrame, index: int) -> int:
        """
        Called on each bar. Override for real-time signal generation.
        
        Args:
            current_data: DataFrame up to current bar
            index: Current bar index
            
        Returns:
            Signal: 1 (buy), -1 (sell), 0 (hold)
        """
        return 0
    
    def reset(self):
        """
        Reset strategy state.
        """
        self.signals = []
        self.positions = []
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
