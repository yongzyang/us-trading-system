"""
Backtest engine for strategy simulation.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from datetime import datetime
from logger import setup_logger
from .portfolio import Portfolio, Position
from .analyzer import BacktestAnalyzer, BacktestResults
from .order import Order, OrderType, OrderSide, OrderStatus
from strategy.base import BaseStrategy
from config import COMMISSION, SLIPPAGE, MAX_POSITION_SIZE, STOP_LOSS_PCT, TAKE_PROFIT_PCT


class BacktestEngine:
    """
    Backtesting engine for trading strategies.
    """
    
    def __init__(
        self,
        strategy: BaseStrategy,
        data: pd.DataFrame,
        initial_capital: float = 100000,
        commission: float = COMMISSION,
        slippage: float = SLIPPAGE,
        max_position_size: float = MAX_POSITION_SIZE,
        stop_loss_pct: float = STOP_LOSS_PCT,
        take_profit_pct: float = TAKE_PROFIT_PCT
    ):
        """
        Initialize backtest engine.
        
        Args:
            strategy: Trading strategy instance
            data: OHLCV data
            initial_capital: Initial capital
            commission: Commission per trade
            slippage: Slippage percentage
            max_position_size: Max position size as % of portfolio
            stop_loss_pct: Stop loss percentage
            take_profit_pct: Take profit percentage
        """
        self.strategy = strategy
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.max_position_size = max_position_size
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
        self.portfolio = Portfolio(initial_capital)
        self.equity_curve = []
        self.logger = setup_logger(__name__)
        
        # Get ticker from data
        self.ticker = 'UNKNOWN'
        if hasattr(data.index, 'name') and data.index.name:
            self.ticker = data.index.name
    
    def run(self) -> BacktestResults:
        """
        Run the backtest.
        
        Returns:
            BacktestResults object
        """
        self.logger.info(f"Starting backtest for {self.strategy.name}")
        self.logger.info(f"Data points: {len(self.data)}")
        
        # Generate signals
        signals = self.strategy.generate_signals(self.data)
        
        if len(signals) != len(self.data):
            raise ValueError("Signal length does not match data length")
        
        # Simulate trading
        for i in range(len(self.data)):
            current_date = self.data.index[i]
            current_price = self.data['close'].iloc[i]
            signal = signals[i]
            
            # Update positions with stop loss / take profit
            self._update_risk_management(current_price, current_date)
            
            # Execute signal
            if signal == 1:  # Buy signal
                self._execute_buy_order(current_price, current_date)
            elif signal == -1:  # Sell signal
                self._execute_sell_order(current_price, current_date)
            
            # Record portfolio value
            market_prices = {self.ticker: current_price}
            portfolio_value = self.portfolio.get_total_value(market_prices)
            self.equity_curve.append(portfolio_value)
        
        # Calculate metrics
        results = BacktestAnalyzer.calculate_metrics(self.equity_curve, self.portfolio.trades)
        
        self.logger.info(f"Backtest completed")
        self.logger.info(results)
        
        return results
    
    def _execute_buy_order(self, price: float, date: pd.Timestamp) -> None:
        """
        Execute a buy order.
        
        Args:
            price: Current price
            date: Current date
        """
        if self.ticker in self.portfolio.positions:
            return  # Already holding position
        
        # Calculate position size
        portfolio_value = self.portfolio.get_total_value({self.ticker: price})
        position_value = portfolio_value * self.max_position_size
        
        # Account for commission and slippage
        execution_price = price * (1 + self.slippage)
        total_cost = position_value * (1 + self.commission)
        
        if total_cost > self.portfolio.cash:
            return  # Not enough cash
        
        quantity = position_value / price
        commission_cost = position_value * self.commission
        
        # Create and execute order
        order = Order(
            ticker=self.ticker,
            side=OrderSide.BUY,
            quantity=quantity,
            order_type=OrderType.MARKET,
            price=execution_price,
            timestamp=date
        )
        
        order.execute(execution_price, quantity, commission_cost)
        
        # Update portfolio
        self.portfolio.cash -= total_cost
        position = Position(
            ticker=self.ticker,
            quantity=quantity,
            entry_price=execution_price,
            entry_date=date
        )
        self.portfolio.add_position(position)
        self.portfolio.record_trade(self.ticker, 'BUY', execution_price, quantity, date, commission_cost)
        
        self.logger.debug(f"BUY: {quantity:.2f} shares @ {execution_price:.2f}")
    
    def _execute_sell_order(self, price: float, date: pd.Timestamp) -> None:
        """
        Execute a sell order.
        
        Args:
            price: Current price
            date: Current date
        """
        if self.ticker not in self.portfolio.positions:
            return  # No position to sell
        
        position = self.portfolio.positions[self.ticker]
        
        # Account for commission and slippage
        execution_price = price * (1 - self.slippage)
        quantity = position.quantity
        proceeds = quantity * execution_price
        commission_cost = proceeds * self.commission
        net_proceeds = proceeds - commission_cost
        
        # Create and execute order
        order = Order(
            ticker=self.ticker,
            side=OrderSide.SELL,
            quantity=quantity,
            order_type=OrderType.MARKET,
            price=execution_price,
            timestamp=date
        )
        
        order.execute(execution_price, quantity, commission_cost)
        
        # Update portfolio
        pnl = net_proceeds - (quantity * position.entry_price)
        self.portfolio.cash += net_proceeds
        self.portfolio.remove_position(self.ticker)
        
        trade_record = {
            'date': date,
            'ticker': self.ticker,
            'side': 'SELL',
            'price': execution_price,
            'quantity': quantity,
            'commission': commission_cost,
            'total': proceeds,
            'return': pnl / (quantity * position.entry_price) if position.quantity > 0 else 0
        }
        self.portfolio.trades.append(trade_record)
        
        self.logger.debug(f"SELL: {quantity:.2f} shares @ {execution_price:.2f}, PnL: {pnl:.2f}")
    
    def _update_risk_management(self, current_price: float, date: pd.Timestamp) -> None:
        """
        Update positions based on risk management rules.
        
        Args:
            current_price: Current price
            date: Current date
        """
        if self.ticker not in self.portfolio.positions:
            return
        
        position = self.portfolio.positions[self.ticker]
        unrealized_pnl = current_price - position.entry_price
        pnl_pct = unrealized_pnl / position.entry_price
        
        # Check stop loss
        if pnl_pct < -self.stop_loss_pct:
            self._execute_sell_order(current_price, date)
            self.logger.debug(f"Stop loss triggered at {pnl_pct:.2%}")
        
        # Check take profit
        elif pnl_pct > self.take_profit_pct:
            self._execute_sell_order(current_price, date)
            self.logger.debug(f"Take profit triggered at {pnl_pct:.2%}")
