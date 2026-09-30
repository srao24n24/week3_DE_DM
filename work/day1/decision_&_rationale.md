# Day 1, Lab 1.2: Decision and Rationale

## What ETL and ELT mean
- **ETL:** clean and transform the data before it gets loaded into its destination.
- **ELT:** load the raw data first, then transform it where it is stored.

| Case | Choice | Where transformation happens | Why |
|---|---|---|---|
| **A** Daily sales dashboard | ELT | In the warehouse with T-SQL, after the raw ERP data is loaded | The data is already structured and only refreshes daily, so there's no need to reshape it first. Keeping the raw copy also lets us reload and check against the ERP. |
| **B** Clickstream plus orders | ELT | In the lakehouse with Spark or SQL, after raw events land in Bronze | Clickstream is big and semi-structured, so it makes more sense to load it first and transform later. Data science also needs the raw events kept. |
| **C** Fraud detection | ETL | In the streaming engine as events arrive, before results are stored. Raw events are also archived. | Decisions have to happen in seconds, so the transformation has to happen before storing the data. Loading first and transforming later would be too slow as it must check at a high frequency. |
| **D** Regulatory finance | ETL | In a staging step before loading into the reporting store | Auditors should only see data that's already been checked and reconciled, and rejected records need to be traceable. Being in the staging step allows cleaned data to be checked. |