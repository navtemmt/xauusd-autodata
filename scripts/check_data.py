import pandas as pd
import os
from datetime import datetime

def check_data_file(symbol):
    """Check if data file exists and print summary"""
    filename = f"data/{symbol}_data.csv"
    
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return False
    
    try:
        # Read the CSV file
        df = pd.read_csv(filename, index_col=0, parse_dates=True)
        
        print(f"\n✅ {symbol} Data Summary:")
        print(f"   File: {filename}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Date Range: {df.index[0]} to {df.index[-1]}")
        print(f"   Latest Close: {df['close'].iloc[-1]:.2f}")
        print(f"   File Size: {os.path.getsize(filename) / 1024:.2f} KB")
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            print(f"   ⚠️  Missing values: {missing}")
        else:
            print(f"   ✓ No missing values")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading {filename}: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print(f"Data Check Report")
    print(f"Generated: {datetime.now()}")
    print("=" * 50)
    
    # Check XAUUSD data
    success = check_data_file("XAUUSD")
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All data files verified successfully!")
    else:
        print("❌ Some data files are missing or corrupted!")
        exit(1)
    print("=" * 50)
