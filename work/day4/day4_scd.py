import pandas as pd
from pathlib import Path

source = Path("provided_data/day4/customer_snapshot_2026_09_01.csv")
source2 = Path("provided_data/day4/customer_snapshot_2026_09_02.csv")
output = Path("work/day4/data_output"); output.mkdir(parents = True, exist_ok = True)
snapshot_1 = pd.read_csv(source, parse_dates = ["signup_date", "last_modified"])
snapshot_2 = pd.read_csv(source2, parse_dates = ["signup_date", "last_modified"])

# --- Lab 4.1 ---
# TODO: build an initial dim_customer with surrogate key, effective dates and is_current.
dim_customer = snapshot_1.copy()
dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))
dim_customer["effective_from"] = pd.Timestamp("2026-09-01")
dim_customer["effective_to"] = pd.Timestamp("9999-12-31")
dim_customer["is_current"] = True

print(dim_customer[["customer_key", "customer_id", "customer_name", "city", "effective_from", "effective_to", "is_current"]])
print(f"\nrow count: {len(dim_customer)}")

dim_customer.to_csv(output / "dim_customer.csv", index = False)

# --- Lab 4.2 ---
# TODO: apply Type 1 to name/email corrections.
existing = snapshot_2[snapshot_2["customer_id"].isin(dim_customer["customer_id"])]

for _, row in existing.iterrows():
    current_row = dim_customer[(dim_customer["customer_id"] == row["customer_id"]) & (dim_customer["is_current"] == True)]
    current = current_row.iloc[0]

    name_changed = current["customer_name"] != row["customer_name"]
    email_changed = current["email"] != row["email"]

    if name_changed or email_changed:
        idx = current_row.index[0]
        dim_customer.loc[idx, "customer_name"] = row["customer_name"]
        dim_customer.loc[idx, "email"] = row["email"]

print(dim_customer[dim_customer["customer_id"] == 3])
print(f"\nrow count: {len(dim_customer)}")

# --- Lab 4.3 ---
# TODO: apply Type 2 to city/state/segment changes.
new_rows = []
next_key = dim_customer["customer_key"].max() + 1

for _, row in existing.iterrows():
    current_row = dim_customer[(dim_customer["customer_id"] == row["customer_id"]) & (dim_customer["is_current"] == True)]
    current = current_row.iloc[0]

    city_changed = current["city"] != row["city"]
    state_changed = current["state"] != row["state"]
    segment_changed = current["customer_segment"] != row["customer_segment"]

    if city_changed or state_changed or segment_changed:
        idx = current_row.index[0]
        dim_customer.loc[idx, "effective_to"] = pd.Timestamp("2026-09-02")
        dim_customer.loc[idx, "is_current"] = False

        new_row = row.copy()
        new_row["customer_key"] = next_key
        new_row["effective_from"] = pd.Timestamp("2026-09-02")
        new_row["effective_to"] = pd.Timestamp("9999-12-31")
        new_row["is_current"] = True
        new_rows.append(new_row)
        next_key += 1

dim_customer = pd.concat([dim_customer, pd.DataFrame(new_rows)], ignore_index = True)

print(dim_customer[dim_customer["customer_id"].isin([5, 9])][["customer_key", "customer_id", "city", "state", "customer_segment", "effective_from", "effective_to", "is_current"]].sort_values(["customer_id", "effective_from"]))
print(f"\nrow count: {len(dim_customer)}")

# --- Lab 4.4 ---
new_customers = snapshot_2[~snapshot_2["customer_id"].isin(dim_customer["customer_id"])]

next_key = dim_customer["customer_key"].max() + 1
inserted_rows = []

for _, row in new_customers.iterrows():
    new_row = row.copy()
    new_row["customer_key"] = next_key
    new_row["effective_from"] = pd.Timestamp("2026-09-02")
    new_row["effective_to"] = pd.Timestamp("9999-12-31")
    new_row["is_current"] = True
    inserted_rows.append(new_row)
    next_key += 1

dim_customer = pd.concat([dim_customer, pd.DataFrame(inserted_rows)], ignore_index = True)

print(dim_customer[dim_customer["customer_id"] == 101])
print(f"\nrow count: {len(dim_customer)}")
print((dim_customer["is_current"] == True).sum())

dim_customer.to_csv(output / "updated_dim_customer.csv", index = False)

# --- Lab 4.5 ---
# TODO: prove unchanged customers do not create extra rows.
row_counts = dim_customer.groupby("customer_id").size()

unchanged_ids = [cus_id for cus_id in snapshot_1["customer_id"] if cus_id not in [3, 5, 9]]

print(f"Row counts for a sample of unchanged customers: {row_counts[unchanged_ids]}")
print(f"All unchanged customers have exactly 1 row: {(row_counts[unchanged_ids] == 1).all()}")
print(f"Full row count distribution: \n{row_counts.value_counts()}")

# --- Lab 4.6 ---
# SELECT dc.customer_key FROM DimCustomer dc
# WHERE dc.customer_id = @order_customer_id AND @order_date >= dc.effective_from AND @order_date < dc.effective_to;

# --- Lab 4.7 ---
# Unknown member: If a fact row has a customer_id that isn't in DimCustomer yet, the fix is a placeholder row, 
# like customer_key = -1, with values like "Unknown" as shown in the reading. Facts that can't find a real match
# use that key instead of failing, so the sale still gets recorded.

# Late-arriving dimension: Sometimes a sale comes in before the customer's dimension row exists. The fix is to
# insert the dimension row right away using just the known customer_id, with "Unknown" placeholder values, and
# flag it as an inferred member (IsInferredMember = True), as shown in the reading. When the real customer data
# shows up later, that row gets updated in place and the flag is set back to False, no new row needed.
