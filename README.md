# US Trading System - High Frequency Intraday Backtesting

A professional-grade backtesting system for high-frequency intraday US stock trading strategies.

## Features

- 📊 **Minute-level Data**: Support for 1min, 5min, 15min, 30min, 60min timeframes
- 🎯 **Strategy Framework**: Easy-to-use base class for custom strategies
- ⚡ **High-Performance Backtest Engine**: No look-ahead bias, realistic order execution
- 📈 **Risk Management**: Position sizing, stop-loss, take-profit, drawdown control
- 📉 **Performance Analytics**: Sharpe ratio, Sortino ratio, max drawdown, win rate, and more
- 💡 **Example Strategies**: Momentum, Mean Reversion, Moving Average Crossover
- 🗄️ **SQLite Storage**: Efficient data persistence and retrieval

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yongzyang/us-trading-system.git
cd us-trading-system

# Install dependencies
pip install -r requirements.txt
```

### Run a Sample Backtest

```bash
python run_backtest.py
```

This will run a Moving Average Crossover strategy on AAPL with sample data and display performance metrics.

## Project Structure

```
us-trading-system/
├── data/                          # Data acquisition and storage
│   ├── __init__.py
│   ├── fetcher.py                # Fetch OHLCV data from yfinance
│   ├── storage.py                # SQLite data persistence
│   └── validator.py              # Data validation and preprocessing
├── strategy/                      # Strategy framework and examples
│   ├── __init__.py
│   ├── base.py                   # Abstract base strategy class
│   ├── indicators.py             # Technical indicators library
│   ├── momentum_strategy.py       # Momentum strategy example
│   ├── mean_reversion_strategy.py # Mean reversion strategy example
│   └── moving_average_strategy.py # MA crossover strategy example
├── backtest/                      # Backtesting engine
│   ├── __init__.py
│   ├── engine.py                 # Core backtest engine
│   ├── portfolio.py              # Portfolio tracking
���   ├── order.py                  # Order management and execution
│   └── analyzer.py               # Performance analysis
├── risk/                          # Risk management
│   ├── __init__.py
│   └── manager.py                # Position sizing and risk control
├── config.py                      # Configuration parameters
├── logger.py                      # Logging setup
├── utils.py                       # Utility functions
├── run_backtest.py               # Example backtest runner
├── requirements.txt              # Python dependencies
├── QUICKSTART.md                 # Quick start guide
└── .gitignore                    # Git ignore file
```

## Key Components

### Data Layer
- **Fetcher**: Downloads minute-level OHLCV data using yfinance
- **Storage**: Efficiently stores and retrieves data from SQLite
- **Validator**: Ensures data quality and handles preprocessing

### Strategy Framework
- **Base Strategy**: Abstract class for custom strategy implementation
- **Indicators**: Comprehensive technical indicator library (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic)
- **Example Strategies**: Ready-to-use momentum, mean reversion, and moving average strategies

### Backtest Engine
- **Engine**: Simulates trading with realistic execution
- **Portfolio**: Tracks cash, positions, and equity curve
- **Order**: Manages market and limit orders with proper execution
- **Analyzer**: Calculates performance metrics and statistics

### Risk Management
- Position sizing based on portfolio risk
- Stop-loss and take-profit logic
- Maximum drawdown control
- Risk per trade calculations

## License

MIT License - Feel free to use and modify!

## Disclaimer

This backtesting system is for educational and research purposes. Past performance does not guarantee future results.