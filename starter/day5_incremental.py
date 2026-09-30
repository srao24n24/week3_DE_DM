import json
import pandas as pd

# TODO: load the initial target and stored watermark.
# TODO: deduplicate the incremental batch by order_id using latest last_modified.
# TODO: upsert inserts and updates; keep late-arriving business dates.
# TODO: advance watermark only after successful reconciliation.
