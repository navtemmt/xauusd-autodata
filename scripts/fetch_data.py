import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import json
from datetime import datetime

# Initialize TV datafeed (no credentials needed for free data)
tv = TvDatafeed()

def fetch_and_save_data(symbol, exchange, interval, n_bars=5000):
    """Fetch data from TradingView and save to CSV"""
    try:
        print(f"Fetching {symbol} data from {exchange}...")
        
        # Fetch data
        data = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=n_bars
        )
        
        if data is not None and not data.empty:
            # Create filename
            filename = f"data/{symbol}_data.csv"
            
            # Save to CSV
            data.to_csv(filename)
            print(f"Saved {len(data)} rows to {filename}")
            
            # Print summary
            print(f"Date range: {data.index[0]} to {data.index[-1]}")
            print(f"Columns: {list(data.columns)}")
            
            return True
        else:
            print(f"No data received for {symbol}")
            return False
            
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting data fetch...")
    print(f"Timestamp: {datetime.now()}")
    
    # Fetch XAUUSD data from OANDA
    success = fetch_and_save_data(
        symbol="XAUUSD",
        exchange="OANDA",
        interval=Interval.in_1_minute,
        n_bars=5000
    )
    
    if success:
        print("\nData fetch completed successfully!")
    else:
        print("\nData fetch failed!")
        exit(1)
