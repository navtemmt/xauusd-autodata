# XAUUSD Auto Data

🔄 Automated XAUUSD (Gold/USD) candlestick data fetcher using GitHub Actions

## Overview

This repository automatically fetches and updates XAUUSD (Gold/USD) candlestick data from OANDA exchange using TradingView's datafeed. The data is updated daily via GitHub Actions and stored as CSV files.

## Features

- ✅ **Automated Data Collection**: Fetches XAUUSD data daily at midnight UTC
- ✅ **Historical Data**: Retrieves up to 5000 bars of 1-hour candlestick data
- ✅ **Data Validation**: Includes automated checks for data quality
- ✅ **OANDA Exchange**: Uses reliable OANDA data source
- ✅ **GitHub Actions**: Fully automated via CI/CD pipeline

## Data Format

The data is stored in `data/XAUUSD_data.csv` with the following columns:

- **datetime**: Timestamp of the candlestick
- **open**: Opening price
- **high**: Highest price
- **low**: Lowest price
- **close**: Closing price
- **volume**: Trading volume

## Repository Structure

```
xauusd-autodata/
├── .github/
│   └── workflows/
│       └── fetch_data.yml    # GitHub Actions workflow
├── scripts/
│   ├── fetch_data.py         # Main data fetching script
│   └── check_data.py         # Data validation script
├── data/
│   └── XAUUSD_data.csv       # Generated XAUUSD data
└── README.md                  # This file
```

## How It Works

1. **Scheduled Execution**: GitHub Actions runs daily at 00:00 UTC
2. **Data Fetching**: `fetch_data.py` retrieves XAUUSD data from OANDA via TradingView
3. **Data Validation**: `check_data.py` verifies data integrity
4. **Automatic Commit**: Changes are automatically committed to the repository

## Manual Trigger

You can manually trigger the data fetch:

1. Go to the "Actions" tab
2. Select "Fetch XAUUSD Data" workflow
3. Click "Run workflow"

## Dependencies

- Python 3.10+
- pandas
- tradingview-datafeed

## Usage

To use the data in your projects:

```python
import pandas as pd

# Load the XAUUSD data
df = pd.read_csv('data/XAUUSD_data.csv', index_col=0, parse_dates=True)

# Display basic info
print(df.head())
print(f"Latest price: {df['close'].iloc[-1]}")
```

## License

This repository is for educational and research purposes.

## Credits

Based on the [1auto2](https://github.com/navtemmt/1auto2) template.
Data provided by OANDA via TradingView.
