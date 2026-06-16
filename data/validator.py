"""
Data validation and preprocessing module.
"""

import pandas as pd
import numpy as np
from logger import setup_logger
from typing import Tuple

logger = setup_logger(__name__)


class DataValidator:
    """
    Validate and preprocess market data.
    """
    
    def __init__(self):
        self.logger = setup_logger(__name__)
    
    @staticmethod
    def validate_ohlcv(data: pd.DataFrame) -> bool:
        """
        Validate OHLCV data integrity.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            True if valid, False otherwise
        """
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        
        # Check columns
        if not all(col in data.columns for col in required_columns):
            return False
        
        # Check data types
        for col in required_columns:
            if not pd.api.types.is_numeric_dtype(data[col]):
                return False
        
        # Check for negative prices
        if (data[['open', 'high', 'low', 'close']] < 0).any().any():
            return False
        
        # Check for negative volume
        if (data['volume'] < 0).any():
            return False
        
        # Check OHLC relationships
        if (data['high'] < data['low']).any():
            return False
        
        if (data['high'] < data['open']).any() or (data['high'] < data['close']).any():
            return False
        
        if (data['low'] > data['open']).any() or (data['low'] > data['close']).any():
            return False
        
        return True
    
    @staticmethod
    def handle_missing_data(data: pd.DataFrame, method: str = 'forward_fill') -> pd.DataFrame:
        """
        Handle missing data points.
        
        Args:
            data: DataFrame with potential missing values
            method: 'forward_fill', 'backward_fill', or 'interpolate'
            
        Returns:
            DataFrame with missing values handled
        """
        data = data.copy()
        
        if method == 'forward_fill':
            data = data.fillna(method='ffill')
        elif method == 'backward_fill':
            data = data.fillna(method='bfill')
        elif method == 'interpolate':
            data = data.interpolate(method='linear')
        
        return data
    
    @staticmethod
    def remove_outliers(data: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
        """
        Remove outliers using z-score method.
        
        Args:
            data: DataFrame with OHLCV data
            threshold: Z-score threshold (default 3.0)
            
        Returns:
            DataFrame with outliers removed
        """
        data = data.copy()
        
        # Calculate returns
        returns = data['close'].pct_change()
        
        # Calculate z-scores
        z_scores = np.abs((returns - returns.mean()) / returns.std())
        
        # Mark outliers
        outlier_mask = z_scores > threshold
        
        # Remove outliers
        data = data[~outlier_mask]
        
        return data
    
    @staticmethod
    def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize OHLCV data (ensure consistent format).
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Normalized DataFrame with lowercase column names
        """
        data = data.copy()
        data.columns = data.columns.str.lower()
        
        # Ensure required columns exist
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Ensure index is datetime
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        # Sort by date
        data = data.sort_index()
        
        return data
