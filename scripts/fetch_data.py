import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import json
from datetime import datetime
import os

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
            
            # Split by month and save each month's data
            print("\nSplitting data by month...")
            split_by_month(data, symbol)
            
            return True
        else:
            print(f"No data received for {symbol}")
            return False
            
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        return False

def split_by_month(data, symbol):
    """Split DataFrame by month and save each month's data as a separate file"""
    try:
        # Ensure index is datetime
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        # Group by year and month
        grouped = data.groupby([data.index.year, data.index.month])
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Save each month's data
        for (year, month), group in grouped:
            # Format filename as goldusd_YYYY-MM.csv
            filename = f"data/goldusd_{year:04d}-{month:02d}.csv"
            group.to_csv(filename)
            print(f"Saved {len(group)} rows to {filename}")
        
        print(f"\nTotal: {len(grouped)} monthly files created")
        
    except Exception as e:
        print(f"Error splitting data by month: {str(e)}")

if __name__ == "__main__":
    print("Starting data fetch...")
    print(f"Timestamp: {datetime.now()}")
    
    # Fetch XAUUSD data from OANDA
    success = fetch_and_save_data(
        symbol="XAUUSD",
        exchange="FX",
        interval=Interval.in_1_minute,
        n_bars=5000
    )
    
    if success:
        print("\nData fetch completed successfully!")
    else:
        print("\nData fetch failed!")
        exit(1)
