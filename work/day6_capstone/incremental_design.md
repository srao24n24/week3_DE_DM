# Day 6: Retail Analytics Platform Incremental Load Design

**Watermark or CDC choise:** Watermark, based on last_modified. This data has a reliable last_modified column on every source table, and deletes aren't a primary concern for orders/payments in this scope, so CDC's extra complexity doesn't make the most sense.

**Deduplication:** Sort the incoming batch by last_modified ascending, then drop duplicate order_id rows, keeping the last occurrence, so the most recently modified version of any duplicated row wins.

**Upsert:** Split the deduplicated batch into rows whose order_id already exists in the target (which are updates) and rows that don't (are inserts). For updates, remove the row from the target before adding back the new version, so each order_id ends up with exactly one row. For inserts, append directly.

**Delete:** Watermark can't see deletes, since a deleted row just disappears, no last_modified left to catch it. The fix is a soft delete flag like is_deleted, instead of removing it, so it still shows up in the batch and gets picked up normally, reports just filter those out.

**Late Data:** A fact's order_date is never overwritten by its last_modified date. The watermark filter uses last_modified to decide what's new, but order_date is carried through unchanged, so a January order processed in May still reports correctly under January.

**Restart:** The watermark only advances after reconciliation confirms the load succeeded (target row count matches expected count). If reconciliation fails, the watermark stays at its old value and nothing is lost on the next run. Because the watermark only advances past data that was actually loaded, rerunning the same batch finds nothing eligible, so the target stays unchanged.

