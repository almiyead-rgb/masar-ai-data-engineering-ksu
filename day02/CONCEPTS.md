# Day 2 · Concepts before code

[Course home](../README.md) · [Execution record](../STATUS.md)

## 1 · ETL and ELT describe where transformation happens

Extract obtains data; load lands it in a target; transform applies the required structure and meaning. In this course, ELT means keeping the raw inputs in Bronze first, then transforming them inside Spark. ETL can still be appropriate when the destination must never receive a prohibited field. Do not interpret ELT as permission to collect everything or retain it forever.

## 2 · Define the grain before touching the code

A Bronze receipt records an arrival, not a new business event. Day 1 intentionally stored the 72 trips twice: 144 receipt rows, 72 distinct trip_id values. Silver has one row per trip_id. Driver data has one row per driver_id. GPS has one row per event_id, with three events per base trip. These are different grains.

## 3 · Staging is a translation layer, not a second raw archive

stg_trips types and renames trip fields. stg_drivers standardizes driver attributes. stg_gps parses the nested JSON location into latitude and longitude. We keep source files and Bronze unchanged. Temporary staging views organize a query; the lab also writes isolated Delta staging snapshots so the transformations can be inspected after the session ends.

## 4 · Type conversion must not silently repair the facts

Fare uses decimal(12,2), distance uses decimal(12,2), and duration uses whole seconds. The course contract accepts at most two decimal places for fare and distance. A value such as 19.251 is rejected rather than rounded silently; 0.00 fare is permitted, but zero distance is not. Failed timestamp and numeric conversions are detected before publishing Silver. See official Spark casting sources.

## 5 · UTC storage and a local business date are separate decisions

06:00+03:00 becomes 03:00Z, once. Do not apply an extra three-hour subtraction after parsing an offset. The trip business date is the local start date in Asia/Riyadh, not the arrival date and not necessarily the UTC date. A trip starting at 00:30+03:00 on June 2 has a UTC start on June 1. Derive duration from complete timestamps, not from clock strings.

## 6 · Normalize only known labels

An explicit mapping converts " riyadh " to Riyadh and handles the three approved cities. There are ten differently formatted city values in the fixed base fixture. UnknownCity is not guessed into a valid city. Keep the raw city in staging and the original source in Bronze for traceability.

## 7 · Validate the right side before a join

Joining each trip to one unique driver should preserve the trip count. First reject duplicate driver keys, then check missing relationships with a left-anti join, then enrich. An inner join is not a repair strategy: it can hide unmatched trips. Joining the 72 base trips directly to 216 raw GPS events creates 216 joined rows; summing trip fares there would triple the total. Aggregate GPS to trip grain first when that output is needed.

## 8 · A duplicate and a correction are not the same thing

For Day 2, base and late records have source revision 1. Identical business payloads for the same trip are duplicates; conflicting payloads at the same revision stop processing. We do not silently choose the latest arrival as truth. A stable ordering of source file, source hash and batch id chooses provenance among identical receipts. Revision-aware correction is reserved for Day 3.

## 9 · Deduplicate before MERGE

MERGE needs a source that can be matched unambiguously to the target. Our source has one validated row per trip_id before insertion. Day 2 inserts new keys and leaves equal existing records unchanged; an existing key with different content raises an error. Merely declaring a unique_key in a model does not establish uniqueness; it must be tested. Official Delta/dbt references explain these mechanisms.

## 10 · Retry, rerun and redelivery have different meanings

Rerunning the transformation reads the same Bronze state. Retrying late_003 verifies that the same batch and payload already exist and does not append. Intentional redelivery uses late_replay_004 and appends three more Bronze receipts. In both cases Silver remains 75 business rows. Idempotency here concerns business content, not identical log versions, timestamps or execution durations.

## 11 · Late arrival is not a new trip date

The three late trips start on June 1 and cross midnight locally. They arrive in the fixed delivery schedule on June 4. The June 1 trip count changes from 24 to 27; June 2 and June 3 remain 24 each. Filtering only start_date greater than the latest processed trip date would miss them. The lab processes the supplied late batch explicitly; it is not a general-purpose event-time watermark implementation.

## 12 · Incremental does not automatically mean less scanning

This small lab incrementally changes the target but intentionally scans its tiny Bronze history when constructing candidates. It is not an optimized production incremental reader. At larger scale, source offsets, explicit lookback ranges and tested backfills reduce scanning. A narrow lookback can still miss very late data. Do not partition 75 rows merely to claim an optimization.

## 13 · Freshness needs a clock definition

Event time says when the trip occurred. _ingested_at says when this lab actually ingested a receipt. A synthetic historical fixture should not be declared broken simply because its events are months old today. Native dbt freshness against arrival timestamps and a deterministic teaching comparison against scenario_schedule are distinct tests. 

## 14 · Trust requires more than a green cell

Check schema, row count, key uniqueness, relationships, decimals, local dates and full business content. Compare the native Delta readback against independently calculated expectations. Preserve failures and real artifacts. This is a local, single-writer teaching system; it does not claim concurrent exactly-once ingestion or multi-table atomic transactions. Fare and completed duration are post-trip values: do not later use them as inputs to a prediction made before the trip ends.

[Official sources for Spark, Delta and dbt](SOURCES.md) · [Apply this in Lab 03](labs/lab03/WALKTHROUGH.md)

[Silver field contract](DATA_CONTRACT.md)
