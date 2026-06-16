"""
Utility functions for the trading system.
"""

import pandas as pd
import numpy as np
from typing import Union, List, Tuple
from datetime import datetime, timedelta


def calculate_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate simple returns from price series.
    
    Args:
        prices: Series of prices
        
    Returns:
        Series of returns
    """
    return prices.pct_change()


def calculate_cumulative_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate cumulative returns from price series.
    
    Args:
        prices: Series of prices
        
    Returns:
        Series of cumulative returns
    """
    return (1 + calculate_returns(prices)).cumprod() - 1


def calculate_drawdown(equity: pd.Series) -> Tuple[pd.Series, float]:
    """
    Calculate drawdown from equity curve.
    
    Args:
        equity: Series of portfolio equity
        
    Returns:
        Tuple of (drawdown series, max drawdown percentage)
    """
    running_max = equity.expanding().max()
    drawdown = (equity - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return drawdown, max_drawdown


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02, periods: int = 252) -> float:
    """
    Calculate Sharpe ratio.
    
    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate
        periods: Number of periods per year (252 for daily, 252*6.5 for hourly)
        
    Returns:
        Sharpe ratio
    """
    excess_returns = returns - risk_free_rate / periods
    return np.sqrt(periods) * excess_returns.mean() / excess_returns.std()


def calculate_sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02, periods: int = 252) -> float:
    """
    Calculate Sortino ratio (only downside volatility).
    
    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate
        periods: Number of periods per year
        
    Returns:
        Sortino ratio
    """
    excess_returns = returns - risk_free_rate / periods
    downside_returns = excess_returns[excess_returns < 0]
    downside_std = downside_returns.std()
    
    if downside_std == 0:
        return 0
    
    return np.sqrt(periods) * excess_returns.mean() / downside_std


def calculate_win_rate(trades: List[float]) -> float:
    """
    Calculate win rate from trade P&L.
    
    Args:
        trades: List of trade P&L values
        
    Returns:
        Win rate (0-1)
    """
    if len(trades) == 0:
        return 0
    
    winning_trades = sum(1 for p in trades if p > 0)
    return winning_trades / len(trades)


def calculate_profit_factor(trades: List[float]) -> float:
    """
    Calculate profit factor (gross profit / gross loss).
    
    Args:
        trades: List of trade P&L values
        
    Returns:
        Profit factor
    """
    if len(trades) == 0:
        return 0
    
    gross_profit = sum(p for p in trades if p > 0)
    gross_loss = abs(sum(p for p in trades if p < 0))
    
    if gross_loss == 0:
        return 0 if gross_profit == 0 else float('inf')
    
    return gross_profit / gross_loss


def format_currency(amount: float) -> str:
    """
    Format amount as currency.
    
    Args:
        amount: Dollar amount
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage.
    
    Args:
        value: Decimal value (0.05 for 5%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value*100:.{decimals}f}%"
