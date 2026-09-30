# Day 1, Lab 1.3: Processing Decision

| Case | Required latency | Choice | Acceptable delay | Why |
|---|---|---|---|---|
| **A** Daily sales dashboard | Daily | Batch | Ready before the business day morning starts | Nobody needs a daily dashboard faster than daily, and batch is simpler and cheaper. And it should be done nightly after the business day ends. |
| **B** Clickstream plus orders | Hourly | Micro-batch | Up to about an hour | The requirement is hourly, so streaming would cost more and be more complex for no reason. Small frequent batches are enough. |
| **C** Fraud detection | Seconds | Streaming | Few seconds | This is the only case where the data has to be processed as it comes in. Batch can't hit a seconds requirement. We have to catch any detection as fast as possible. |
| **D** Regulatory finance | Daily | Batch | Next day, once reconciliation checks pass | Being accurate matters more than being fast here, and a batch gives a clear point where the numbers get validated. |