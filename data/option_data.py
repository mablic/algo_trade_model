import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
from dataclasses import dataclass, field
from data.stock_data import StockData
from datetime import datetime

@dataclass
class OptionData(StockData):
    delta: float = 0.0
    gamma: float = 0.0
    vega: float = 0.0
    theta: float = 0.0
    rho: float = 0.0
    option_type: str = 'call'  
    strike_price: float = 0.0
    risk_free_rate: float = 0.05
    time_to_maturity: float = 0.0
    expiration_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        super().__post_init__()
        self.calculate_time_to_maturity()
        self.calculate_greeks()

    def calculate_d1_d2(self):
        S = self.get_current_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.get_volatility

        if T <= 0:
            return 0, 0

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    def calculate_greeks(self):
        d1, d2 = self.calculate_d1_d2()
        S = self.get_current_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate
        sigma = self.get_volatility

        if T <= 0:
            # Option expired
            self.delta = 0.0
            self.gamma = 0.0
            self.vega = 0.0
            self.theta = 0.0
            self.rho = 0.0
            return

        # Delta
        if self.option_type == 'call':
            self.delta = stats.norm.cdf(d1)
        else:  # put
            self.delta = stats.norm.cdf(d1) - 1

        # Gamma (same for calls and puts)
        self.gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))

        # Vega (same for calls and puts)
        self.vega = S * stats.norm.pdf(d1) * np.sqrt(T) / 100

        # Theta (per day)
        if self.option_type == 'call':
            self.theta = (-S * stats.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                - r * K * np.exp(-r * T) * stats.norm.cdf(d2)) / 365
        else:
            self.theta = (-S * stats.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                + r * K * np.exp(-r * T) * stats.norm.cdf(-d2)) / 365

        # Rho
        if self.option_type == 'call':
            self.rho = K * T * np.exp(-r * T) * stats.norm.cdf(d2) / 100
        else:
            self.rho = -K * T * np.exp(-r * T) * stats.norm.cdf(-d2) / 100

    def calculate_time_to_maturity(self):
        current_date = datetime.now()
        days_to_maturity = (self.expiration_date - current_date).days
        self.time_to_maturity = max(days_to_maturity / 365.25, 0.001)

    @property
    def get_type(self):
        return 'OptionData'

    def get_option_price(self):
        d1, d2 = self.calculate_d1_d2()
        S = self.get_current_price
        K = self.strike_price
        T = self.time_to_maturity
        r = self.risk_free_rate

        if self.option_type == 'call':
            price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
        else:  # put
            price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
        
        return price

    def get_greeks_dict(self):
        return {
            'delta': self.delta,
            'gamma': self.gamma,
            'vega': self.vega,
            'theta': self.theta,
            'rho': self.rho
        }

    def update_time_to_maturity(self):
        self.calculate_time_to_maturity()
        self.calculate_greeks()

    def get_option_info(self):
        return {
            'ticker': self.ticker,
            'option_type': self.option_type,
            'strike_price': self.strike_price,
            'expiration_date': self.expiration_date,
            'time_to_maturity': self.time_to_maturity,
            'current_underlying_price': self.get_current_price,
            'option_price': self.get_option_price(),
            'volatility': self.get_volatility,
            'risk_free_rate': self.risk_free_rate,
            'greeks': self.get_greeks_dict()
        }