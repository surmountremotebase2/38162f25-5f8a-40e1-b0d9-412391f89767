from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    EMA Crossover Strategy:
    - Buys when short-term EMA crosses above long-term EMA
    - Sells when short-term EMA crosses below long-term EMA
    """
    
    def __init__(self):
        # Tickers for which we'll apply the strategy
        self.tickers = ["AAPL"]
    
    @property
    def interval(self):
        # Define the interval for the strategy
        return "1day"
    
    @property
    def assets(self):
        # Define the assets to trade
        return self.tickers

    @property
    def data(self):
        # No additional data required for this strategy
        return []
    
    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Calculate short-term and long-term EMAs
            short_term_ema = EMA(ticker, data["ohlcv"], length=12)
            long_term_ema = EMA(ticker, data["ohlcv"], length=26)
            
            if short_term_ema is None or long_term_ema is None:
                log(f"Insufficient data for {ticker}")
                allocation_dict[ticker] = 0
                continue
            
            # Check for EMA crossover; last two points to determine the direction
            if short_term_ema[-1] > long_term_ema[-1] and short_term_ema[-2] < long_term_ema[-2]:
                # Bullish signal
                log(f"Bullish crossover detected for {ticker}")
                allocation_dict[ticker] = 1
            elif short_term_ema[-1] < long_term_ema[-1] and short_term_ema[-2] > long_term_ema[-2]:
                # Bearish signal
                log(f"Bearish crossover detected for {ticker}")
                allocation_dict[ticker] = 0
            else:
                # No clear signal, maintain current position
                log(f"No crossover signal for {ticker}")
                allocation_dict[ticker] = 0.5  # This line is adjustable based on risk preference

        return TargetAllocation(allocation_dict)