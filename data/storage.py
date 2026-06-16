"""
Data storage module for SQLite persistence.
"""

import sqlite3
import pandas as pd
from typing import Optional
from config import DATABASE_PATH
from logger import setup_logger
import os

logger = setup_logger(__name__)


class DataStorage:
    """
    SQLite database for storing market data.
    """
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.logger = setup_logger(__name__)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """
        Ensure database directory exists.
        """
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
    
    def save_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        interval: str = '1h'
    ) -> None:
        """
        Save OHLCV data to SQLite.
        
        Args:
            ticker: Stock ticker symbol
            data: DataFrame with OHLCV data
            interval: Data interval
        """
        try:
            table_name = f"{ticker}_{interval}".lower().replace('-', '_')
            
            with sqlite3.connect(self.db_path) as conn:
                data.to_sql(table_name, conn, if_exists='replace', index=True)
            
            self.logger.info(f"Saved {len(data)} bars for {ticker} at {interval} interval")
            
        except Exception as e:
            self.logger.error(f"Error saving data for {ticker}: {str(e)}")
            raise
    
    def load_data(
        self,
        ticker: str,
        interval: str = '1h'
    ) -> Optional[pd.DataFrame]:
        """
        Load OHLCV data from SQLite.
        
        Args:
            ticker: Stock ticker symbol
            interval: Data interval
            
        Returns:
            DataFrame with OHLCV data or None if not found
        """
        try:
            table_name = f"{ticker}_{interval}".lower().replace('-', '_')
            
            with sqlite3.connect(self.db_path) as conn:
                query = f"SELECT * FROM {table_name}"
                data = pd.read_sql_query(query, conn, index_col='Date', parse_dates=['Date'])
            
            self.logger.info(f"Loaded {len(data)} bars for {ticker} at {interval} interval")
            return data
            
        except Exception as e:
            self.logger.warning(f"Could not load data for {ticker}: {str(e)}")
            return None
    
    def delete_data(self, ticker: str, interval: str = '1h') -> None:
        """
        Delete data from database.
        
        Args:
            ticker: Stock ticker symbol
            interval: Data interval
        """
        try:
            table_name = f"{ticker}_{interval}".lower().replace('-', '_')
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                conn.commit()
            
            self.logger.info(f"Deleted data for {ticker} at {interval} interval")
            
        except Exception as e:
            self.logger.error(f"Error deleting data: {str(e)}")
            raise
