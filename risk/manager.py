"""
Risk management functions.
"""

import numpy as np
from typing import Tuple
from logger import setup_logger

logger = setup_logger(__name__)


class RiskManager:
    """
    Risk management utilities.
    """
    
    @staticmethod
    def calculate_position_size(
        portfolio_value: float,
        entry_price: float,
        stop_loss_price: float,
        risk_per_trade: float = 0.02
    ) -> float:
        """
        Calculate position size based on risk per trade.
        
        Args:
            portfolio_value: Total portfolio value
            entry_price: Entry price
            stop_loss_price: Stop loss price
            risk_per_trade: Risk as % of portfolio
            
        Returns:
            Position size in shares
        """
        risk_amount = portfolio_value * risk_per_trade
        price_risk = abs(entry_price - stop_loss_price)
        
        if price_risk == 0:
            return 0
        
        position_size = risk_amount / price_risk
        return position_size
    
    @staticmethod
    def calculate_kelly_criterion(
        win_rate: float,
        avg_win: float,
        avg_loss: float
    ) -> float:
        """
        Calculate Kelly criterion for optimal position sizing.
        
        Args:
            win_rate: Winning trade percentage
            avg_win: Average winning trade size
            avg_loss: Average losing trade size
            
        Returns:
            Kelly fraction (0.0 to 1.0)
        """
        if avg_loss == 0:
            return 0
        
        loss_rate = 1 - win_rate
        kelly = (win_rate * avg_win - loss_rate * avg_loss) / avg_win
        
        # Limit to 0.25 (quarter Kelly) for safety
        kelly = max(0, min(kelly, 0.25))
        
        return kelly
    
    @staticmethod
    def calculate_max_drawdown_risk(
        returns: np.ndarray,
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Value at Risk (VaR) based on historical returns.
        
        Args:
            returns: Array of historical returns
            confidence_level: Confidence level (0.95 = 5% VaR)
            
        Returns:
            VaR as negative percentage
        """
        var = np.percentile(returns, (1 - confidence_level) * 100)
        return var
