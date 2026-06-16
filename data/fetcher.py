"""
Data fetcher for downloading OHLCV data from yfinance.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import Optional
from logger import setup_logger

logger = setup_logger(__name__)


class DataFetcher:
    """
    Fetch market data from yfinance.
    """
    
    def __init__(self):
        self.logger = setup_logger(__name__)
    
    def fetch_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = '1h'
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data from yfinance.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval ('1m', '5m', '15m', '30m', '1h', '1d')
            
        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume
        """
        try:
            self.logger.info(f"Fetching {ticker} data from {start_date} to {end_date} at {interval} interval")
            
            # Download data
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False
            )
            
            # Rename columns to lowercase
            data.columns = data.columns.str.lower()
            
            # Handle single ticker
            if isinstance(data.columns, pd.Index):
                pass
            else:
                data = data[[ticker]]
            
            self.logger.info(f"Downloaded {len(data)} bars for {ticker}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {str(e)}")
            raise
    
    def fetch_multiple(
        self,
        tickers: list,
        start_date: str,
        end_date: str,
        interval: str = '1h'
    ) -> dict:
        """
        Fetch data for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            interval: Data interval
            
        Returns:
            Dictionary with ticker as key and DataFrame as value
        """
        data_dict = {}
        for ticker in tickers:
            try:
                data_dict[ticker] = self.fetch_data(ticker, start_date, end_date, interval)
            except Exception as e:
                self.logger.warning(f"Failed to fetch {ticker}: {str(e)}")
        
        return data_dict
