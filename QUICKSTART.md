# Quick Start Guide

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yongzyang/us-trading-system.git
cd us-trading-system
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Your First Backtest

### Basic Example

The easiest way to get started is to run the example backtest:

```bash
python run_backtest.py
```

This will:
1. Fetch AAPL hourly data for 2023
2. Run a Moving Average Crossover strategy
3. Display performance metrics

## Creating Your Own Strategy

### Step 1: Create a Strategy File

Create a new file `my_strategy.py` in the `strategy/` directory:

```python
from strategy.base import BaseStrategy
from strategy.indicators import calculate_sma, calculate_ema
import pandas as pd

class MyStrategy(BaseStrategy):
    def __init__(self, param1=10, param2=20):
        super().__init__("MyStrategy")
        self.param1 = param1
        self.param2 = param2
    
    def generate_signals(self, data: pd.DataFrame):
        """
        Generate buy/sell signals
        
        Return list of signals:
        - 1: Buy
        - -1: Sell
        - 0: Hold
        """
        signals = []
        
        # Your signal logic here
        for i in range(len(data)):
            # Example: simple momentum signal
            if data['close'].iloc[i] > data['close'].iloc[i-1]:
                signals.append(1)  # Bullish
            else:
                signals.append(-1)  # Bearish
        
        return signals
```

### Step 2: Run Backtest with Your Strategy

```python
from data.fetcher import DataFetcher
from backtest.engine import BacktestEngine
from strategy.my_strategy import MyStrategy

# Fetch data
fetcher = DataFetcher()
data = fetcher.fetch_data('AAPL', '2023-01-01', '2023-12-31', interval='1h')

# Create strategy
strategy = MyStrategy(param1=10, param2=20)

# Run backtest
engine = BacktestEngine(
    strategy=strategy,
    data=data,
    initial_capital=100000,
    commission=0.001,
    slippage=0.0005
)

results = engine.run()
print(results)
```

## Available Strategies

The system comes with three example strategies:

### 1. Moving Average Crossover

```python
from strategy.moving_average_strategy import MovingAverageStrategy

strategy = MovingAverageStrategy(short_window=5, long_window=20)
```

### 2. Momentum (RSI-based)

```python
from strategy.momentum_strategy import MomentumStrategy

strategy = MomentumStrategy(rsi_window=14, overbought=70, oversold=30)
```

### 3. Mean Reversion (Bollinger Bands)

```python
from strategy.mean_reversion_strategy import MeanReversionStrategy

strategy = MeanReversionStrategy(window=20, num_std=2.0)
```

## Available Technical Indicators

Use these in your strategies:

```python
from strategy.indicators import (
    calculate_sma,           # Simple Moving Average
    calculate_ema,           # Exponential Moving Average
    calculate_rsi,           # Relative Strength Index
    calculate_macd,          # MACD
    calculate_bollinger_bands,  # Bollinger Bands
    calculate_atr,           # Average True Range
    calculate_stochastic     # Stochastic Oscillator
)
```

## Customizing the Backtest

### Adjust Parameters

Edit `config.py` to customize:

```python
INITIAL_CAPITAL = 100000    # Starting capital
COMMISSION = 0.001         # 0.1% per trade
SLIPPAGE = 0.0005          # 0.05% slippage
MAX_POSITION_SIZE = 0.1    # 10% max per position
STOP_LOSS_PCT = 0.02       # 2% stop loss
TAKE_PROFIT_PCT = 0.05     # 5% take profit
```

### Change Data Source

Modify the backtest script:

```python
data = fetcher.fetch_data(
    ticker='MSFT',                    # Different stock
    start_date='2022-01-01',         # Different period
    end_date='2023-12-31',
    interval='1d'                    # Different timeframe
)
```

## Performance Analysis

The backtest returns detailed metrics:

- **Total Return**: Overall profit/loss percentage
- **Sharpe Ratio**: Risk-adjusted returns (higher is better)
- **Sortino Ratio**: Downside risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit / Gross loss
- **Trade Statistics**: Total, winning, and losing trades

## Troubleshooting

### No data downloaded

Make sure:
- Ticker symbol is correct (e.g., 'AAPL', not 'Apple')
- Date range is valid
- You have internet connection

### Strategy not generating signals

Check:
- Signal list length matches data length
- All required columns exist in DataFrame
- No NaN values in critical calculations

### Performance metrics seem off

Verify:
- Commission and slippage are reasonable
- Initial capital is sufficient for position sizing
- Stop loss and take profit percentages are realistic

## Next Steps

1. **Experiment with different strategies** - Try the example strategies on different stocks
2. **Create custom strategies** - Implement your own trading ideas
3. **Optimize parameters** - Find best parameters for each strategy
4. **Add more indicators** - Extend the indicators library
5. **Implement portfolio backtesting** - Trade multiple symbols simultaneously

## Resources

- [Technical Analysis Wikipedia](https://en.wikipedia.org/wiki/Technical_analysis)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)

## Support

For issues or questions, please open an issue on GitHub.

## Disclaimer

This system is for educational purposes only. Past performance does not guarantee future results. Always do your own research before trading.
