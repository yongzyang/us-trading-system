"""
Momentum Strategy.
"""

import pandas as pd
from typing import List
from .base import BaseStrategy
from .indicators import calculate_rsi


class MomentumStrategy(BaseStrategy):
    """
    RSI-based Momentum Strategy.
    
    Buy when RSI > overbought_level.
    Sell when RSI < oversold_level.
    """
    
    def __init__(self, rsi_window: int = 14, overbought: float = 70, oversold: float = 30):
        """
        Initialize Momentum Strategy.
        
        Args:
            rsi_window: RSI window
            overbought: Overbought level (RSI > this = sell)
            oversold: Oversold level (RSI < this = buy)
        """
        super().__init__("Momentum")
        self.rsi_window = rsi_window
        self.overbought = overbought
        self.oversold = oversold
    
    def generate_signals(self, data: pd.DataFrame) -> List[int]:
        """
        Generate buy/sell signals based on RSI.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            List of signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate RSI
        data = data.copy()
        data['rsi'] = calculate_rsi(data['close'], self.rsi_window)
        
        signals = []
        position = 0
        
        for i in range(len(data)):
            if pd.isna(data['rsi'].iloc[i]):
                signals.append(0)
            else:
                rsi = data['rsi'].iloc[i]
                
                # Buy signal: RSI < oversold
                if rsi < self.oversold:
                    if position != 1:
                        signals.append(1)
                        position = 1
                    else:
                        signals.append(0)
                # Sell signal: RSI > overbought
                elif rsi > self.overbought:
                    if position != -1:
                        signals.append(-1)
                        position = -1
                    else:
                        signals.append(0)
                else:
                    signals.append(0)
        
        return signals
