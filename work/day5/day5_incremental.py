import json
import pandas as pd
from pathlib import Path

s_initial = Path("provided_data/day5/orders_initial.csv")
s_incremental = Path("provided_data/day5/orders_incremental_2026_09_03.csv")
watermark_path = Path("provided_data/day5/watermark_state.json")
output = Path("work/day5/data_output"); output.mkdir(parents = True, exist_ok = True)

# --- Lab 5.2 ---
# TODO: load the initial target and stored watermark.
target = pd.read_csv(s_initial, parse_dates = ["order_date", "last_modified"])
incremental = pd.read_csv(s_incremental, parse_dates = ["order_date", "last_modified"])

with open(watermark_path) as f:
    watermark_state = json.load(f)

last_watermark = pd.Timestamp(watermark_state["last_watermark"])
eligible_batch = incremental[incremental["last_modified"] > last_watermark]

print(f"stored watermark: {last_watermark}")
print(f"incoming batch rows: {len(incremental)}")
print(f"eligible batch rows: {len(eligible_batch)}")
print(eligible_batch[["order_id", "last_modified"]])
print("-------------------------------")

# --- Lab 5.3 ---
# TODO: deduplicate the incremental batch by order_id using latest last_modified.
deduplicated_batch = (eligible_batch.sort_values("last_modified").drop_duplicates(subset = "order_id", keep = "last"))

print(f"eligible batch rows: {len(eligible_batch)}")
print(f"deduplicated batch rows: {len(deduplicated_batch)}")
print("-------------------------------")

# --- Lab 5.4 ---
# TODO: upsert inserts and updates; keep late-arriving business dates.
updates = deduplicated_batch[deduplicated_batch["order_id"].isin(target["order_id"])]
inserts = deduplicated_batch[~deduplicated_batch["order_id"].isin(target["order_id"])]

target = target[~target["order_id"].isin(updates["order_id"])]
target = pd.concat([target, updates, inserts], ignore_index = True)

print(f"updates: {len(updates)}")
print(f"inserts: {len(inserts)}")
print(f"target rows: {len(target)}")
print("-------------------------------")

check = target[target["order_id"] == 19999]
print(f"order 19999 in target:")
print(check[["order_id", "order_date", "last_modified"]].to_string(index = False))
print("-------------------------------")

# --- Lab 5.6 ---
# TODO: advance watermark only after successful reconciliation.
reconciliation_passed = len(target) == 101

print(f"reconciliation check: target has {len(target)} rows, expected 101")
print(f"reconciliation passed: {reconciliation_passed}")

if reconciliation_passed:
    new_watermark = deduplicated_batch["last_modified"].max()
    watermark_state["last_watermark"] = str(new_watermark)

    with open(watermark_path, "w") as f:
        json.dump(watermark_state, f, indent = 2)

    print(f"watermark advanced to: {new_watermark}")
    target.to_csv(output / "orders_target.csv", index = False)
else:
    print("reconciliation failed, watermark NOT advanced")

print("-------------------------------")

# --- Lab 5.7 ---
target_before_rerun = target.copy()

with open(watermark_path) as f:
    watermark_state_2 = json.load(f)

last_watermark_2 = pd.Timestamp(watermark_state_2["last_watermark"])

eligible_batch_2 = incremental[incremental["last_modified"] > last_watermark_2]
deduplicated_batch_2 = (eligible_batch_2.sort_values("last_modified").drop_duplicates(subset = "order_id", keep = "last"))

updates_2 = deduplicated_batch_2[deduplicated_batch_2["order_id"].isin(target["order_id"])]
inserts_2 = deduplicated_batch_2[~deduplicated_batch_2["order_id"].isin(target["order_id"])]

target_after_rerun = target[~target["order_id"].isin(updates_2["order_id"])]
target_after_rerun = pd.concat([target_after_rerun, updates_2, inserts_2], ignore_index = True)

print(f"eligible batch rows on rerun: {len(eligible_batch_2)}")
print(f"target rows before rerun: {len(target_before_rerun)}")
print(f"target rows after rerun: {len(target_after_rerun)}")

rows_match = len(target_before_rerun) == len(target_after_rerun)
content_match = target_before_rerun.sort_values("order_id").reset_index(drop = True).equals(target_after_rerun.sort_values("order_id").reset_index(drop = True))

print(f"row counts match: {rows_match}")
print(f"full content matches exactly: {content_match}")
print("-------------------------------")

# --- Lab 5.8 ---
# Watermark can't see deletes, since a deleted row just disappears, no last_modified left to catch it. The fix from the reading is a soft delete: the source flags
# the row with is_deleted = True instead of removing it, so it still shows up in the batch and gets picked up normally, reports just filter those out. CDC solves 
# it differently, it reads the database's own log and records the delete as its own event, so it actually catches that a delete happened instead of relying on a flag.
