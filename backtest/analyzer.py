"""
Performance analysis and metrics calculation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from dataclasses import dataclass
from logger import setup_logger


@dataclass
class BacktestResults:
    """Backtest performance results."""
    total_return: float
    annual_return: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_trade_return: float
    best_trade: float
    worst_trade: float
    
    def __str__(self):
        return f"""
        ===== BACKTEST RESULTS =====
        Total Return: {self.total_return:.2%}
        Annual Return: {self.annual_return:.2%}
        Sharpe Ratio: {self.sharpe_ratio:.2f}
        Sortino Ratio: {self.sortino_ratio:.2f}
        Max Drawdown: {self.max_drawdown:.2%}
        Win Rate: {self.win_rate:.2%}
        Profit Factor: {self.profit_factor:.2f}
        Total Trades: {self.total_trades}
        Winning Trades: {self.winning_trades}
        Losing Trades: {self.losing_trades}
        Avg Trade Return: {self.avg_trade_return:.2%}
        Best Trade: {self.best_trade:.2%}
        Worst Trade: {self.worst_trade:.2%}
        """


class BacktestAnalyzer:
    """
    Analyze backtest results and calculate metrics.
    """
    
    def __init__(self):
        self.logger = setup_logger(__name__)
    
    @staticmethod
    def calculate_metrics(equity_curve: List[float], trades: List[Dict]) -> BacktestResults:
        """
        Calculate comprehensive backtest metrics.
        
        Args:
            equity_curve: List of portfolio values over time
            trades: List of trade dictionaries
            
        Returns:
            BacktestResults object
        """
        if len(equity_curve) < 2:
            raise ValueError("Not enough data to calculate metrics")
        
        equity_array = np.array(equity_curve)
        returns = np.diff(equity_array) / equity_array[:-1]
        
        # Total return
        total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0]
        
        # Annual return (assuming 252 trading days per year for daily data)
        days = len(equity_curve) - 1
        years = days / 252 if days > 0 else 1
        annual_return = (equity_curve[-1] / equity_curve[0]) ** (1 / years) - 1 if years > 0 else 0
        
        # Sharpe ratio
        sharpe_ratio = BacktestAnalyzer._calculate_sharpe_ratio(returns)
        
        # Sortino ratio
        sortino_ratio = BacktestAnalyzer._calculate_sortino_ratio(returns)
        
        # Max drawdown
        max_drawdown = BacktestAnalyzer._calculate_max_drawdown(equity_curve)
        
        # Trade statistics
        if len(trades) > 0:
            trade_returns = [t.get('return', 0) for t in trades]
            winning_trades = len([t for t in trade_returns if t > 0])
            losing_trades = len([t for t in trade_returns if t < 0])
            win_rate = winning_trades / len(trades) if len(trades) > 0 else 0
            
            # Profit factor
            gross_profit = sum([t for t in trade_returns if t > 0])
            gross_loss = abs(sum([t for t in trade_returns if t < 0]))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            avg_trade_return = np.mean(trade_returns) if trade_returns else 0
            best_trade = max(trade_returns) if trade_returns else 0
            worst_trade = min(trade_returns) if trade_returns else 0
        else:
            winning_trades = 0
            losing_trades = 0
            win_rate = 0
            profit_factor = 0
            avg_trade_return = 0
            best_trade = 0
            worst_trade = 0
        
        return BacktestResults(
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(trades),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            avg_trade_return=avg_trade_return,
            best_trade=best_trade,
            worst_trade=worst_trade
        )
    
    @staticmethod
    def _calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio.
        
        Args:
            returns: Array of returns
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sharpe ratio
        """
        if len(returns) < 2 or np.std(returns) == 0:
            return 0
        
        excess_returns = returns - risk_free_rate / 252
        return np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    
    @staticmethod
    def _calculate_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sortino ratio (downside volatility only).
        
        Args:
            returns: Array of returns
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sortino ratio
        """
        if len(returns) < 2:
            return 0
        
        excess_returns = returns - risk_free_rate / 252
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or np.std(downside_returns) == 0:
            return 0
        
        return np.sqrt(252) * np.mean(excess_returns) / np.std(downside_returns)
    
    @staticmethod
    def _calculate_max_drawdown(equity_curve: List[float]) -> float:
        """
        Calculate maximum drawdown.
        
        Args:
            equity_curve: List of portfolio values
            
        Returns:
            Maximum drawdown as percentage
        """
        if len(equity_curve) < 2:
            return 0
        
        equity_array = np.array(equity_curve)
        running_max = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - running_max) / running_max
        max_drawdown = np.min(drawdown)
        
        return max_drawdown
