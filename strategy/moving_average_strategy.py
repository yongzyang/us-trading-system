"""
Moving Average Crossover Strategy.
"""

import pandas as pd
from typing import List
from .base import BaseStrategy
from .indicators import calculate_sma


class MovingAverageStrategy(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy.
    
    Buy when short-term MA crosses above long-term MA.
    Sell when short-term MA crosses below long-term MA.
    """
    
    def __init__(self, short_window: int = 5, long_window: int = 20):
        """
        Initialize Moving Average Strategy.
        
        Args:
            short_window: Short MA window
            long_window: Long MA window
        """
        super().__init__("MovingAverageCrossover")
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> List[int]:
        """
        Generate buy/sell signals based on MA crossover.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            List of signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate moving averages
        data = data.copy()
        data['sma_short'] = calculate_sma(data['close'], self.short_window)
        data['sma_long'] = calculate_sma(data['close'], self.long_window)
        
        signals = []
        position = 0
        
        for i in range(len(data)):
            if pd.isna(data['sma_short'].iloc[i]) or pd.isna(data['sma_long'].iloc[i]):
                signals.append(0)
            else:
                # Buy signal: short MA > long MA
                if data['sma_short'].iloc[i] > data['sma_long'].iloc[i]:
                    if position != 1:
                        signals.append(1)
                        position = 1
                    else:
                        signals.append(0)
                # Sell signal: short MA < long MA
                elif data['sma_short'].iloc[i] < data['sma_long'].iloc[i]:
                    if position != -1:
                        signals.append(-1)
                        position = -1
                    else:
                        signals.append(0)
                else:
                    signals.append(0)
        
        return signals
