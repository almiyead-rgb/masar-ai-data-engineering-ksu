# Day 5 · Understand the final data products

[Day 5](README.md) · [Notebook](STUDENT.ipynb) · [Glossary](GLOSSARY.md) · [References D5-1–D5-6](SOURCES.md)

## 1. Start from approved inputs

Your Day 4 outputs contain 75 approved trips and 217 distinct events. Day 5 reads those actual Delta tables and checks their prerequisite reports. It does not read the deliberately contaminated candidate. The original corrected fares total SAR 1,880.60 and must remain consistent in the final products.

## 2. A product answers a defined question

Silver identifies trusted trips. A Gold product answers a consumer question, such as trips per driver per local day. A data contract states fields, keys, units and interpretation. The [eight products](DATA_PRODUCTS.md) serve different purposes; they are not eight additional assignments.

## 3. Define the grain before counting

A fact row means one trip. A driver-day row means a driver/date group, which may include several trips. In this fixture, 75 fact rows become 18 driver-day groups; summing their `trip_count` still gives 75. Compare measures at compatible grains, not raw row counts. [D5-3]

## 4. Do not invent spatial detail or demand

The source has city names, not verified service-zone boundaries. `zone_resolution=city_proxy` makes this explicit. The hourly product's “demand” is observed trip starts, not all requests, cancellations or transport activity. Missing hourly groups do not certify zero demand.

## 5. Record the input snapshot

The helper chooses and records each Delta input version and reads it with `versionAsOf`. Products built from different moving versions can disagree even when each query is correct. The manifest makes the selected paths and versions inspectable. Required historical files must still exist. [D5-1]

## 6. Keep facts and dimensions distinct

`bi.fact_trips` stores trip measures and foreign keys. The date, driver and city dimensions store unique keys and descriptions. Each fact joins to one dimension row. Check dimension-key uniqueness and missing relationships before trusting a report. [D5-3]

## 7. Aggregate events before the fare join

A trip can have several GPS events. Joining all those events directly repeats the fare. Count the distinct events per trip first, then left-join that single count into the trip fact. The three late trips remain without events; the total recorded event count is 217, not 219 message receipts.

## 8. Keep reporting time and units explicit

Canonical timestamps remain UTC; daily reporting follows the trip start in Asia/Riyadh. A trip starting at 23:55 and ending after midnight belongs to its start date. Durations are seconds, distance kilometres and fares SAR. Changing the reporting date rule changes the metric, not merely its display.

## 9. Reconcile groups as well as totals

The fact and both Gold summaries must reconcile on trip counts, fares and durations. Check the city and driver-day groups too: the same grand total can hide values assigned to the wrong group. The SQL result is 25 trips per city, with different city fare totals. See [the reporting results](AI_BI_GUIDE.md).

## 10. Combine averages through their components

A combined mean duration is total duration divided by total trip count. An unweighted mean of group averages is generally wrong when group sizes differ. Preserve `total_duration_seconds` and `trip_count` for aggregation; use decimal monetary fields for fares. [D5-4]

## 11. An AI feature has a decision time

The fixed cutoff is June 4, 2026, 06:05 Riyadh time. Historical trip ends must fall in the prior 24-hour window and the source revision must be available by the cutoff. The target is the next complete hour, 07:00–08:00. These are scenario settings, not the date on which you run the notebook.

## 12. Occurrence is not availability

A June 1 trip arriving on June 4 cannot inform a June 2 decision. The supplied scenario schedule records availability by source revision. Filtering event time alone can admit information learned later. Historical reconstruction needs the appropriate version as well as its availability; the latest snapshot is not sufficient for every possible past cutoff. [D5-5]

## 13. Separate inputs, audit fields and labels

The allowed inputs are `zone_key`, `completed_trips_24h`, `avg_duration_seconds_24h` and `history_available`. Keep lineage and cutoff timestamps for audit. The future target belongs in the separate labels table. Do not select every column into model inputs simply because it exists.

## 14. Unknown is not zero

The fixture does not observe the target hour. Its three label rows remain null with `UNOBSERVED`. There are no observed supervised targets for fitting or scoring a model. A zero target would claim observed absence of trips; a null target states that the answer is not known from this data.

## 15. A release manifest controls this reader

Each of the eight path-based Delta tables commits independently. The helper writes fresh tables, validates all of them, then advances its own local manifest pointer. This prevents this reader from selecting an incomplete candidate; it does not create global multi-table atomicity or coordinate concurrent publishers. [D5-2]

## 16. Test recovery, not just the happy path

Lab 07 builds a good release, deliberately fails a candidate after one table, confirms the good pointer is unchanged, and rebuilds successfully. Compare canonical business-content hashes, not file names, durations or run IDs. This controlled same-session failure is not a machine crash or production recovery test.

## 17. Keep dependency checks and integration distinct

The daily path continues the accumulated work. A separate optional DAG runner starts from raw sources and blocks downstream stages after failure; it does not execute dbt. Neither installing dependencies nor passing a reference calculation proves native execution. Use the actual reports and [the correct scope](INTEGRATION.md).

## 18. Deliver data with its meaning

The eight CSV files are small local exports, not a deployed service. CSV loses Delta's type metadata; keep units and null interpretation beside it. Save your executed notebooks and notes separately from the output archive. The final submission is the same eight labs, credited to the programme and SDAIA Academy as described in [the submission guide](../project/SUBMISSION.md). [D5-6]
