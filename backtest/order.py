"""
Order management and execution.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class OrderType(Enum):
    """Order types."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(Enum):
    """Order status."""
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"


class OrderSide(Enum):
    """Order side (buy/sell)."""
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Order:
    """
    Order representation.
    """
    ticker: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    price: float
    timestamp: datetime
    limit_price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_price: Optional[float] = None
    filled_quantity: float = 0.0
    commission: float = 0.0
    
    def execute(self, execution_price: float, filled_quantity: float = None, commission: float = 0.0):
        """
        Execute the order.
        
        Args:
            execution_price: Price at which order is executed
            filled_quantity: Quantity filled (default: full quantity)
            commission: Commission cost
        """
        if filled_quantity is None:
            filled_quantity = self.quantity
        
        self.filled_price = execution_price
        self.filled_quantity = filled_quantity
        self.commission = commission
        self.status = OrderStatus.FILLED
    
    def get_total_cost(self) -> float:
        """
        Get total cost including commission.
        
        Returns:
            Total cost
        """
        if self.filled_price is None:
            return 0.0
        
        return self.filled_quantity * self.filled_price + self.commission
