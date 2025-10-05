import yfinance as yf
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod

@dataclass
class BaseData:
    ticker: str
    start_date: datetime
    end_date: datetime
    prices: pd.DataFrame = field(default_factory=pd.DataFrame)

    def __post_init__(self):
        if self.prices.empty:
            raise ValueError("Price data is empty")

    @property
    def get_prices(self):
        return self.prices

    @property
    def get_current_price(self):
        return self.prices["Close"].iloc[-1]

    @property
    def get_ticker(self):
        return self.ticker

    @property
    def get_type(self):
     return 'BaseType'
