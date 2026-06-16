"""
Portfolio tracking and management.
"""

import pandas as pd
from typing import Dict, List
from dataclasses import dataclass, field
from logger import setup_logger


@dataclass
class Position:
    """Represents a position in a security."""
    ticker: str
    quantity: float
    entry_price: float
    entry_date: pd.Timestamp
    
    def get_current_value(self, current_price: float) -> float:
        """Get current value of position."""
        return self.quantity * current_price
    
    def get_unrealized_pnl(self, current_price: float) -> float:
        """Get unrealized P&L."""
        return self.quantity * (current_price - self.entry_price)


class Portfolio:
    """
    Portfolio management and tracking.
    """
    
    def __init__(self, initial_capital: float):
        """
        Initialize portfolio.
        
        Args:
            initial_capital: Initial capital
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.equity_curve = []
        self.trades = []
        self.logger = setup_logger(__name__)
    
    def add_position(self, position: Position) -> None:
        """
        Add a position to portfolio.
        
        Args:
            position: Position to add
        """
        if position.ticker in self.positions:
            # Update existing position
            existing = self.positions[position.ticker]
            total_quantity = existing.quantity + position.quantity
            
            if total_quantity == 0:
                del self.positions[position.ticker]
            else:
                # Recalculate average entry price
                total_cost = (existing.quantity * existing.entry_price + 
                            position.quantity * position.entry_price)
                new_entry_price = total_cost / total_quantity
                existing.quantity = total_quantity
                existing.entry_price = new_entry_price
                existing.entry_date = position.entry_date
        else:
            self.positions[position.ticker] = position
    
    def remove_position(self, ticker: str) -> None:
        """
        Remove a position from portfolio.
        
        Args:
            ticker: Ticker symbol
        """
        if ticker in self.positions:
            del self.positions[ticker]
    
    def get_total_value(self, market_prices: Dict[str, float]) -> float:
        """
        Get total portfolio value.
        
        Args:
            market_prices: Current market prices {ticker: price}
            
        Returns:
            Total portfolio value
        """
        equity_value = self.cash
        
        for ticker, position in self.positions.items():
            if ticker in market_prices:
                equity_value += position.get_current_value(market_prices[ticker])
        
        return equity_value
    
    def get_unrealized_pnl(self, market_prices: Dict[str, float]) -> float:
        """
        Get total unrealized P&L.
        
        Args:
            market_prices: Current market prices
            
        Returns:
            Total unrealized P&L
        """
        unrealized_pnl = 0.0
        
        for ticker, position in self.positions.items():
            if ticker in market_prices:
                unrealized_pnl += position.get_unrealized_pnl(market_prices[ticker])
        
        return unrealized_pnl
    
    def record_trade(self, ticker: str, side: str, price: float, quantity: float, 
                    date: pd.Timestamp, commission: float) -> None:
        """
        Record a completed trade.
        
        Args:
            ticker: Ticker symbol
            side: 'BUY' or 'SELL'
            price: Execution price
            quantity: Quantity traded
            date: Trade date
            commission: Commission cost
        """
        self.trades.append({
            'date': date,
            'ticker': ticker,
            'side': side,
            'price': price,
            'quantity': quantity,
            'commission': commission,
            'total': price * quantity + commission
        })
    
    def reset(self) -> None:
        """
        Reset portfolio to initial state.
        """
        self.cash = self.initial_capital
        self.positions = {}
        self.equity_curve = []
        self.trades = []
