import os
from datetime import datetime

import pandas as pd
from tvDatafeed import TvDatafeed, Interval

# Configuration
DATA_DIR = "data"
SYMBOL = "XAUUSD"
EXCHANGE = "FX"
INTERVAL = Interval.in_1_minute
N_BARS = 5000

# Initialize TradingView datafeed
tv = TvDatafeed()


def prepare_dataframe(data):
    """Convert TradingView data into a clean DataFrame with a datetime column."""
    data = data.copy().reset_index()

    # tvDatafeed normally returns a datetime index. Rename safely if needed.
    if "datetime" not in data.columns:
        data = data.rename(columns={data.columns[0]: "datetime"})

    data["datetime"] = pd.to_datetime(data["datetime"])

    return (
        data.drop_duplicates(subset=["datetime"], keep="last")
        .sort_values("datetime")
        .reset_index(drop=True)
    )


def merge_and_save(file_path, new_data):
    """Merge newly downloaded candles into an existing CSV without duplicates."""
    if os.path.exists(file_path):
        old_data = pd.read_csv(file_path, parse_dates=["datetime"])

        combined = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )

        combined["datetime"] = pd.to_datetime(combined["datetime"])

        combined = (
            combined.drop_duplicates(subset=["datetime"], keep="last")
            .sort_values("datetime")
            .reset_index(drop=True)
        )

        net_new_rows = len(combined) - len(old_data)
        action = "Updated"
    else:
        combined = new_data.copy()
        net_new_rows = len(combined)
        action = "Created"

    combined.to_csv(file_path, index=False)

    print(
        f"{action}: {file_path} | "
        f"{len(combined)} total rows | "
        f"{max(0, net_new_rows)} net new rows"
    )

    return combined


def split_by_month_and_update(data, symbol):
    """Split fetched candles by month and incrementally update monthly files."""
    data = data.copy()
    data["year_month"] = data["datetime"].dt.strftime("%Y-%m")

    monthly_dir = os.path.join(DATA_DIR, f"{symbol}_{INTERVAL.name}")
    os.makedirs(monthly_dir, exist_ok=True)

    month_count = 0

    for year_month, month_data in data.groupby("year_month"):
        month_file = os.path.join(monthly_dir, f"{year_month}.csv")

        month_data = (
            month_data.drop(columns=["year_month"])
            .drop_duplicates(subset=["datetime"], keep="last")
            .sort_values("datetime")
            .reset_index(drop=True)
        )

        merge_and_save(month_file, month_data)
        month_count += 1

    print(f"Monthly files processed: {month_count}")


def fetch_and_save_data(symbol, exchange, interval, n_bars=5000):
    """Fetch recent TradingView candles and incrementally store them in CSV files."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)

        print(f"Fetching {symbol} data from {exchange}...")
        print(f"Interval: {interval} | Requested bars: {n_bars}")

        raw_data = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=n_bars
        )

        if raw_data is None or raw_data.empty:
            print(f"No data received for {symbol}.")
            return False

        data = prepare_dataframe(raw_data)

        print(f"Fetched rows: {len(data)}")
        print(f"Fetched range: {data['datetime'].min()} to {data['datetime'].max()}")
        print(f"Columns: {list(data.columns)}")

        # Master file: retains all data gathered across previous runs.
        master_file = os.path.join(DATA_DIR, f"{symbol}_data.csv")
        merged_master = merge_and_save(master_file, data)

        print("\nUpdating monthly files...")
        split_by_month_and_update(data, symbol)

        print(
            f"\nMaster CSV range: "
            f"{merged_master['datetime'].min()} to "
            f"{merged_master['datetime'].max()}"
        )

        return True

    except Exception as error:
        print(f"Error fetching/updating {symbol}: {error}")
        return False


if __name__ == "__main__":
    print("Starting incremental data update...")
    print(f"Local timestamp: {datetime.now()}")

    success = fetch_and_save_data(
        symbol=SYMBOL,
        exchange=EXCHANGE,
        interval=INTERVAL,
        n_bars=N_BARS
    )

    # Keep a persistent log of scheduled/manual runs.
    with open("run_log.txt", "a", encoding="utf-8") as log_file:
        status = "SUCCESS" if success else "FAILED"
        log_file.write(
            f"{datetime.utcnow().isoformat()} UTC | "
            f"{status} | {SYMBOL} | {EXCHANGE} | "
            f"{INTERVAL.name} | requested_bars={N_BARS}\n"
        )

    if success:
        print("\nData update completed successfully.")
    else:
        print("\nData update failed.")
        raise SystemExit(1)
