"""
Example backtest runner.
"""

import pandas as pd
from data.fetcher import DataFetcher
from data.storage import DataStorage
from backtest.engine import BacktestEngine
from strategy.moving_average_strategy import MovingAverageStrategy
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """
    Run a sample backtest.
    """
    # Fetch data
    logger.info("Fetching market data...")
    fetcher = DataFetcher()
    data = fetcher.fetch_data(
        ticker='AAPL',
        start_date='2023-01-01',
        end_date='2023-12-31',
        interval='1h'
    )
    
    if len(data) == 0:
        logger.error("No data fetched")
        return
    
    logger.info(f"Data shape: {data.shape}")
    
    # Create strategy
    logger.info("Creating Moving Average strategy...")
    strategy = MovingAverageStrategy(short_window=5, long_window=20)
    
    # Run backtest
    logger.info("Running backtest...")
    engine = BacktestEngine(
        strategy=strategy,
        data=data,
        initial_capital=100000,
        commission=0.001,
        slippage=0.0005
    )
    
    results = engine.run()
    
    # Display results
    logger.info(results)
    
    # Display equity curve
    logger.info(f"Starting equity: ${engine.initial_capital:,.2f}")
    logger.info(f"Ending equity: ${engine.equity_curve[-1]:,.2f}")
    logger.info(f"Total return: {results.total_return:.2%}")
    

if __name__ == '__main__':
    main()
