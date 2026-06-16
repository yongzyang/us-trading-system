"""
Mean Reversion Strategy.
"""

import pandas as pd
from typing import List
from .base import BaseStrategy
from .indicators import calculate_bollinger_bands


class MeanReversionStrategy(BaseStrategy):
    """
    Bollinger Bands Mean Reversion Strategy.
    
    Buy when price touches lower band.
    Sell when price touches upper band.
    """
    
    def __init__(self, window: int = 20, num_std: float = 2.0):
        """
        Initialize Mean Reversion Strategy.
        
        Args:
            window: Bollinger Bands window
            num_std: Number of standard deviations
        """
        super().__init__("MeanReversion")
        self.window = window
        self.num_std = num_std
    
    def generate_signals(self, data: pd.DataFrame) -> List[int]:
        """
        Generate buy/sell signals based on Bollinger Bands.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            List of signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate Bollinger Bands
        data = data.copy()
        upper, middle, lower = calculate_bollinger_bands(
            data['close'], 
            self.window, 
            self.num_std
        )
        
        data['upper_band'] = upper
        data['middle_band'] = middle
        data['lower_band'] = lower
        
        signals = []
        position = 0
        
        for i in range(len(data)):
            if pd.isna(data['lower_band'].iloc[i]) or pd.isna(data['upper_band'].iloc[i]):
                signals.append(0)
            else:
                close = data['close'].iloc[i]
                lower_band = data['lower_band'].iloc[i]
                upper_band = data['upper_band'].iloc[i]
                
                # Buy signal: price touches lower band
                if close <= lower_band:
                    if position != 1:
                        signals.append(1)
                        position = 1
                    else:
                        signals.append(0)
                # Sell signal: price touches upper band
                elif close >= upper_band:
                    if position != -1:
                        signals.append(-1)
                        position = -1
                    else:
                        signals.append(0)
                else:
                    signals.append(0)
        
        return signals
