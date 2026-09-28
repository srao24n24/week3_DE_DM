# Day 1, Lab 1.1: Requirement matrix

| Case | Sources | Consumers | Latency | Volume | history | Governance needs |
|---|---|---|---|---|---|---|
| **A** Daily sales dashboard | ERP tables (structured) | BI analysts | Daily | Low to medium | 7 years | Only analysts should have access. Totals should match the ERP after each load. |
| **B** Clickstream plus product and order analytics | Clickstream events (semi-structured), product and order data (structured) | Data science and BI | Hourly | High | 3 years | User and session IDs could be personal data, so they need masking or restricted access. Data can only be kept 3 years. Need to track where data came from. |
| **C** Fraud detection | Streaming JSON events | Operations and ML | Seconds | High velocity | 90 days hot | Financial data, so access needs to be tight and logged. Has to respond fast. |
| **D** Regulatory finance reporting | Highly structured finance data | Finance and auditors | Daily | Medium | 10 years | Auditors need to be able to trace every number. History can't be changed quietly. Needs to reconcile to the source and be kept a long time. |

Note: The CSV doesn't give volume sizes or governance needs, so I inferred those from what each business does.