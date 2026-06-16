"""
Technical indicators library.
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_sma(prices: pd.Series, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average.
    
    Args:
        prices: Series of prices
        window: Window size
        
    Returns:
        Series of SMA values
    """
    return prices.rolling(window=window).mean()


def calculate_ema(prices: pd.Series, window: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    
    Args:
        prices: Series of prices
        window: Window size
        
    Returns:
        Series of EMA values
    """
    return prices.ewm(span=window, adjust=False).mean()


def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index.
    
    Args:
        prices: Series of prices
        window: Window size (default 14)
        
    Returns:
        Series of RSI values (0-100)
    """
    deltas = np.diff(prices)
    seed = deltas[:window+1]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100. / (1. + rs)
    
    for i in range(window, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        
        up = (up * (window - 1) + upval) / window
        down = (down * (window - 1) + downval) / window
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
    
    return pd.Series(rsi, index=prices.index)


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        prices: Series of prices
        fast: Fast EMA window
        slow: Slow EMA window
        signal: Signal line window
        
    Returns:
        Tuple of (MACD, Signal line, Histogram)
    """
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd = ema_fast - ema_slow
    signal_line = calculate_ema(macd, signal)
    histogram = macd - signal_line
    
    return macd, signal_line, histogram


def calculate_bollinger_bands(prices: pd.Series, window: int = 20, num_std: float = 2.0) -> tuple:
    """
    Calculate Bollinger Bands.
    
    Args:
        prices: Series of prices
        window: Window size
        num_std: Number of standard deviations
        
    Returns:
        Tuple of (Upper band, Middle band, Lower band)
    """
    sma = calculate_sma(prices, window)
    std = prices.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return upper_band, sma, lower_band


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculate Average True Range.
    
    Args:
        high: Series of high prices
        low: Series of low prices
        close: Series of close prices
        window: Window size
        
    Returns:
        Series of ATR values
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()
    
    return atr


def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14, smooth: int = 3) -> tuple:
    """
    Calculate Stochastic Oscillator.
    
    Args:
        high: Series of high prices
        low: Series of low prices
        close: Series of close prices
        window: Window size
        smooth: Smoothing window
        
    Returns:
        Tuple of (K line, D line)
    """
    lowest_low = low.rolling(window=window).min()
    highest_high = high.rolling(window=window).max()
    
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    k_line = k_percent.rolling(window=smooth).mean()
    d_line = k_line.rolling(window=smooth).mean()
    
    return k_line, d_line
