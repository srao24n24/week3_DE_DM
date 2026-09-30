from pathlib import Path
import pandas as pd

source = Path("provided_data/day2/orders_for_format_lab.csv")
output = Path("work/day2"); output.mkdir(parents=True, exist_ok=True)
orders = pd.read_csv(source, parse_dates=["order_date", "last_modified"])
# TODO 1: write the DataFrame as uncompressed CSV, gzip CSV, JSON Lines and Parquet.
# TODO 2: read only order_id, order_date and order_status from Parquet.
# TODO 3: record file sizes and row counts in format_comparison.csv.
# TODO 4: partition Parquet output by order year and month.
