# main.py
from datetime import datetime
from price_model import DataLoader, ConfigData  # 替换为你的文件名
from graph_model import GraphModel

def main():
    # 加载数据
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    try:
        model_param = DataLoader.load_data('AAPL', start_date, end_date)
        config_data = ConfigData(model_param)
        graph_model = GraphModel(config_data)
        graph_model.display_statistics()
        graph_model.plot_price_chart()
        graph_model.plot_returns_distribution()
        graph_model.plot_volatility_analysis()
        graph_model.plot_cumulative_returns()
        graph_model.plot_summary_dashboard()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()