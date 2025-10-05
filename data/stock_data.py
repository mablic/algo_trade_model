import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from data.base_data import BaseData

@dataclass
class StockData(BaseData):
    log_returns: pd.Series = field(default_factory=pd.Series)
    volatility: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        if self.log_returns.empty and not self.prices.empty:
            self.calculate_log_returns()
    
    def calculate_log_returns(self):
        if self.prices.empty or 'Close' not in self.prices.columns:
            raise ValueError("Prices data is missing or invalid")
        close_prices = self.prices['Close']
        self.log_returns = np.log(close_prices/ close_prices.shift(1)).dropna()

        if not self.log_returns.empty:
            self.volatility = self.log_returns.std() * np.sqrt(252)

    @property
    def get_volatility(self):
        return self.volatility
    
    @property
    def get_log_returns(self):
        return self.log_returns

    @property
    def get_type(self):
     return "StockType"

    def get_prices_stats(self):
        close_prices = self.prices["Close"]
        returns = self.log_returns

        stats = {
            'current_price': self.get_current_price,
            'price_mean': close_prices.mean(),
            'price_std': close_prices.std(),
            'return_mean': returns.mean(),
            'return_std' : returns.std(),
            'volatility' : self.get_volatility,
            'data_points' : len(close_prices),
        }

        return stats  