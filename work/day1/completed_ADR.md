# Architecture decision record

**Case B: Raw clickstream plus product and order analytics**

*Business objective:* Give BI and data science teams analytics on customer behavior and orders by combining clickstream events with product and order data.

*Sources and formats:* Clickstream events (semi-structured JSON) and product and order data (structured tables).

*Required latency:* Hourly.

*Consumers:* Data science (needs raw and cleaned data) and BI (needs cleaned data).

*Recommended store:* Lakehouse

*Processing:* Batch

*Pattern:* ELT

*Proposed Bronze Silver Gold responsibilities:*
- Bronze: raw clickstream JSON and raw product and order data, exactly as received. Nothing is dropped.
- Silver: parse the JSON into columns, remove duplicates, standardize timestamps, filter test or bot traffic, match customer and product keys, and set aside bad records.
- Gold: analytics tables for BI (like sessions by product) and cleaned tables for data science.

*Security governance and quality considerations:*
- Security: user and session IDs may be personal data, so label them with a sensitivity label and restrict access. Give workspace roles to only the people who need each layer, so raw Bronze data is limited to engineers and approved data scientists.
- Governance: use Purview Audit to log who accessed the data, use Fabric lineage to trace Gold back to Bronze, and follow the 3-year retention limit.
- Quality: check for nulls and duplicates in Silver, and compare row counts between layers for each batch.

*Decision rationale and rejected alternative:*
- Rationale: The data is both semi-structured and structured, and the users are data science and BI. A lakehouse handles both kinds of data, suits data science, and fits the Bronze/Silver/Gold setup. With ELT the raw events land first and get transformed inside the lakehouse, so the raw data stays available. Hourly micro-batches are enough for the latency.
- Rejected alternative: A warehouse handles structured data, so the raw clickstream would have to be flattened before landing, and data science would lose the raw data.
- Also considered: Streaming was rejected because the requirement is hourly, so it adds cost and complexity for not needed.

NOTE: https://learn.microsoft.com/en-us/fabric/governance/governance-compliance-overview 