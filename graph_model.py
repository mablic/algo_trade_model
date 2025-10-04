import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

class GraphModel:
    
    def __init__(self, config_data):
        self.config_data = config_data
    
    def plot_price_chart(self, figsize=(12, 6)):
        plt.figure(figsize=figsize)
        prices = self.config_data.get_prices
        
        plt.plot(prices.index, prices['Close'], linewidth=1.5, color='blue', label='Close Price')
        plt.title(f'{self.config_data.get_ticker} Price Chart', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_returns_distribution(self, figsize=(10, 6)):
        plt.figure(figsize=figsize)
        returns = self.config_data.get_log_returns
        
        plt.hist(returns, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(returns.mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {returns.mean():.4f}')
        plt.axvline(returns.mean() + returns.std(), color='orange', linestyle='--', linewidth=1)
        plt.axvline(returns.mean() - returns.std(), color='orange', linestyle='--', linewidth=1)
        
        plt.title(f'{self.config_data.get_ticker} Log Returns Distribution', fontsize=14, fontweight='bold')
        plt.xlabel('Log Returns', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_volatility_analysis(self, figsize=(12, 8)):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
        
        prices = self.config_data.get_prices
        returns = self.config_data.get_log_returns
        rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
        
        ax1.plot(prices.index, prices['Close'], color='blue', linewidth=1, label='Close Price')
        ax1.set_ylabel('Price ($)', color='blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.legend(loc='upper left')
        
        ax1_twin = ax1.twinx()
        ax1_twin.plot(rolling_vol.index, rolling_vol, color='red', linewidth=1, label='30D Rolling Vol')
        ax1_twin.set_ylabel('Volatility', color='red', fontsize=12)
        ax1_twin.tick_params(axis='y', labelcolor='red')
        ax1_twin.legend(loc='upper right')
        
        ax1.set_title(f'{self.config_data.get_ticker} Price and Rolling Volatility', fontsize=14, fontweight='bold')
        ax2.plot(returns.index, returns, linewidth=0.5, color='green', alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.set_ylabel('Log Returns', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_title('Daily Log Returns', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_cumulative_returns(self, figsize=(12, 6)):
        plt.figure(figsize=figsize)
        returns = self.config_data.get_log_returns
        cumulative_returns = (1 + returns).cumprod() - 1
        
        plt.plot(cumulative_returns.index, cumulative_returns * 100, 
                linewidth=2, color='green', label='Cumulative Returns')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        plt.title(f'{self.config_data.get_ticker} Cumulative Returns', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Returns (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_summary_dashboard(self):

        fig = plt.figure(figsize=(15, 10))
        
        gs = fig.add_gridspec(3, 2)
      
        ax1 = fig.add_subplot(gs[0, :])
        prices = self.config_data.get_prices
        ax1.plot(prices.index, prices['Close'], linewidth=1.5, color='blue')
        ax1.set_title('Price Chart', fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        ax2 = fig.add_subplot(gs[1, 0])
        returns = self.config_data.get_log_returns
        ax2.hist(returns, bins=40, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_title('Returns Distribution', fontweight='bold')
        ax2.set_xlabel('Log Returns')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(gs[1, 1])
        cumulative_returns = (1 + returns).cumprod() - 1
        ax3.plot(cumulative_returns.index, cumulative_returns * 100, linewidth=2, color='green')
        ax3.set_title('Cumulative Returns', fontweight='bold')
        ax3.set_ylabel('Returns (%)')
        ax3.grid(True, alpha=0.3)
        
        ax4 = fig.add_subplot(gs[2, :])
        rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
        ax4.plot(rolling_vol.index, rolling_vol, linewidth=1.5, color='red')
        ax4.set_title('30-Day Rolling Volatility', fontweight='bold')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Volatility')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.config_data.get_ticker} Analysis Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def display_statistics(self):
        stats = self.config_data.get_prices_stats()
        
        print(f"\n{'='*50}")
        print(f"{self.config_data.get_ticker} STATISTICS")
        print(f"{'='*50}")
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                if key in ['price_mean', 'price_std', 'current_price']:
                    print(f"{key:15}: ${value:>10.2f}")
                elif key in ['volatility']:
                    print(f"{key:15}: {value:>10.2%}")
                elif key in ['return_mean', 'return_std']:
                    print(f"{key:15}: {value:>10.4f}")
                else:
                    print(f"{key:15}: {value:>10}")
            else:
                print(f"{key:15}: {value}")