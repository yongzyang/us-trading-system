"""
Configuration parameters for the trading system.
"""

# ============ Portfolio Configuration ============
INITIAL_CAPITAL = 100000  # Starting capital in dollars
COMMISSION = 0.001  # 0.1% commission per trade
SLIPPAGE = 0.0005  # 0.05% slippage cost

# ============ Risk Management ============
MAX_POSITION_SIZE = 0.1  # Max 10% of portfolio per position
STOP_LOSS_PCT = 0.02  # 2% stop loss
TAKE_PROFIT_PCT = 0.05  # 5% take profit
MAX_DRAWDOWN_PCT = 0.2  # 20% maximum drawdown before stopping

# ============ Data Configuration ============
DEFAULT_TIMEFRAME = '1h'  # Default timeframe for analysis
SUPPORTED_TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']

# ============ Strategy Configuration ============
DEFAULT_LOOKBACK_PERIOD = 100  # Default lookback period for indicators
WARMUP_PERIOD = 50  # Warmup bars before trading starts

# ============ Logging Configuration ============
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'logs/trading_system.log'

# ============ Database Configuration ============
DATABASE_PATH = 'data/trading_data.db'
