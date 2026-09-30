from pathlib import Path
import pandas as pd

source = Path("provided_data/day2/orders_for_format_lab.csv")
output = Path("work/day2/data_output"); output.mkdir(parents = True, exist_ok = True)
orders = pd.read_csv(source, parse_dates = ["order_date", "last_modified"])

# --- Lab 2.1 ---
def profile_dataset(df, file_path):
    file_path = Path(file_path)
    print(f"\n----- {file_path.name} -----")
    print(f"rows: {df.shape[0]}")
    print(f"columns: {df.shape[1]}")
    print("types:")
    print(df.dtypes)
    print(f"file size on disk: {file_path.stat().st_size} bytes")

csv_path = Path("provided_data/day2/orders_for_format_lab.csv")
json_path = Path("provided_data/day2/orders_for_format_lab.json")

orders_json = pd.read_json(json_path)

profile_dataset(orders, csv_path)
profile_dataset(orders_json, json_path)

# --- Lab 2.2 ---
# TODO 1: write the DataFrame as uncompressed CSV, gzip CSV, JSON Lines and Parquet.
csv_path = output / "orders.csv"
csv_gz_path = output / "orders.csv.gz"
jsonl_path = output / "orders.jsonl"
parquet_path = output / "orders.parquet"

orders.to_csv(csv_path, index = False)
orders.to_csv(csv_gz_path, index = False)
orders.to_json(jsonl_path, orient = "records", lines = True)
orders.to_parquet(parquet_path)

print("-------------")
# --- Lab 2.3 ---
# TODO 3: record file sizes and row counts in format_comparison.csv.
results = []

csv_check = pd.read_csv(csv_path)
results.append({
    "format": "csv",
    "file_size_bytes": csv_path.stat().st_size,
    "row_count": csv_check.shape[0],
    "order_date_dtype": str(csv_check["order_date"].dtype)
})

csv_gz_check = pd.read_csv(csv_gz_path)
results.append({
    "format": "csv_gz",
    "file_size_bytes": csv_gz_path.stat().st_size,
    "row_count": csv_gz_check.shape[0],
    "order_date_dtype": str(csv_gz_check["order_date"].dtype)
})

jsonl_check = pd.read_json(jsonl_path, lines = True)
results.append({
    "format": "jsonl",
    "file_size_bytes": jsonl_path.stat().st_size,
    "row_count": jsonl_check.shape[0],
    "order_date_dtype": str(jsonl_check["order_date"].dtype)
})

parquet_check = pd.read_parquet(parquet_path)
results.append({
    "format": "parquet",
    "file_size_bytes": parquet_path.stat().st_size,
    "row_count": parquet_check.shape[0],
    "order_date_dtype": str(parquet_check["order_date"].dtype)
})

comparison = pd.DataFrame(results)
comparison.to_csv(output / "format_comparison.csv", index = False)
print(comparison)

print("-------------")
# --- Lab 2.4 ---
# TODO 2: read only order_id, order_date and order_status from Parquet.
read_only_orders = pd.read_parquet(parquet_path, columns = ("order_id", "order_date", "order_status" ))
print(f"Count of rows in read_only_orders: {read_only_orders.shape[0]}\nCount of columns in read_only_orders: {read_only_orders.shape[1]}")

print("-------------")
# --- Lab 2.5 ---
# TODO 4: partition Parquet output by order year and month.
orders["order_year"] = orders["order_date"].dt.year
orders["order_month"] = orders["order_date"].dt.month

partitioned_path = output / "orders_partitioned"
orders.to_parquet(partitioned_path, partition_cols = ["order_year", "order_month"])
print("Orders are in partitioned folders")

print("-------------")
# --- Lab 2.6 ---
answer6 = """
The reason order_id is a poor partition column is because every order has its own unique ID, so you would 
end up with one small folder per order, 600 folders for 600 rows, which is too many small files to 
manage. It also doesn't match how people actually queries data. order_date, split by year and month, 
works better because it naturally groups into a small number of folders, and it matches how people 
actually queries for data, like "orders from March," so you can jump straight to the right folder 
instead of scanning everything. A good partition column stays low in variety and matches how people 
actually filter, and order_date does that while order_id does not.
"""
print(answer6)

print("-------------")
# --- Lab 2.7 ---
answer7 = """
Bronze: Parquet, kept raw, not cleaned yet. Partition by the date it was loaded on, since that matches 
how we would re-run or check a specific days data, and keeps the folder count small as new data comes 
in daily.

Silver: Parquet, since the data is cleaned and typed now, and Parquet keeps those types instead of 
losing them like CSV or JSON does. Partition by order year and month, same as 2.5, since thats a good 
amount of folders and matches how people usually filter by date.

Gold: Parquet, still the best for fast reads by dashboards and BI tools. Partition by year and month 
again, or by could also be by state or category if thats what gets filtered more for that table. Keep 
the partitions a bit bigger since Gold tables are usually smaller, so too many small partitions would 
hurt more than help.
"""
print(answer7)