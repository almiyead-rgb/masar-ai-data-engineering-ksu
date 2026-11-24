# Day 5 · Use reporting and AI-ready data correctly

[Day 5](README.md) · [Notebook](STUDENT.ipynb) · [Table contracts](DATA_PRODUCTS.md)

## 1. Begin with one row per trip

`bi.fact_trips` holds the measures. Each `zone_key`, `driver_key` and `date_key` resolves to one row in its matching dimension. From fact to dimension the relationship is many-to-one; from dimension to fact it is one-to-many. Duplicate dimension keys can multiply facts.

GPS events have already been counted per trip before joining the fact. Do not join raw events into a fare sum. The compact date dimension contains the three observed dates, not a complete calendar for all time-intelligence calculations. [D5-3]

## 2. Read the actual SQL result

Lab 08 reads the selected fact-table version, registers `masar_day05_fact` in its Spark session and runs [bi_zone_summary.sql](sql/bi_zone_summary.sql). The printed `BI totals` contains each city proxy, trip count and fare total:

**Riyadh:** 25 trips · SAR 585.00.

**Jeddah:** 25 trips · SAR 625.20.

**Dammam:** 25 trips · SAR 670.40.

**Total:** 75 trips · SAR 1,880.60.

The SQL also calculates total and mean duration; the displayed summary selects the count and fare fields. Do not claim every SQL column was displayed. These are synthetic fixture results, not transport statistics.

## 3. Use consistent metrics

Fares are in SAR, distance in kilometres and duration in seconds. To combine group averages, divide total duration by total trip count; do not take an unweighted average of group means. Grouping uses the local trip-start date, even when a trip ends after midnight. [D5-4]

`zone_key` means a city proxy in this fixture. The hourly “demand” table counts observed starts; an absent hour does not establish zero demand.

## 4. Fix the AI decision time

The exercise cutoff is **June 4, 2026, 03:05 UTC / 06:05 Riyadh time**. Eligible trip ends fall within the preceding 24 hours, including the start boundary but excluding the cutoff. A source revision must also have been available by that cutoff.

The target hour is **04:00–05:00 UTC / 07:00–08:00 Riyadh time** that day: the next complete clock hour, not the next 60 minutes from 06:05. These are fixed scenario times, not your computer's current clock. [D5-5]

## 5. Separate occurrence from availability

A trip occurring on June 1 but arriving on June 4 was unavailable for a June 2 decision. `scenario_schedule.json` supplies the earliest availability of each source revision; replay does not make that revision newly available.

At this fixed cutoff, the supplied approved snapshot and schedule are compatible. Do not move the cutoff arbitrarily and assume that the latest corrected snapshot reconstructs every older decision: historical version selection would also be needed. Feast is a conceptual reference here, not an installed feature store. [D5-5]

## 6. Inspect the four permitted inputs

The teaching allowlist is `zone_key`, `completed_trips_24h`, `avg_duration_seconds_24h` and `history_available`. Keep cutoff, horizon and availability timestamps as audit context. Do not silently add future labels, trip/driver IDs, raw GPS or current-trip outcomes.

Each city has eight eligible completed trips. Historical mean durations are Riyadh **1,230.00 seconds**, Jeddah **1,350.00** and Dammam **1,470.00**. The notebook prints one feature example; inspect the corresponding export for all three. These values describe history, not predicted demand.

## 7. Leave unobserved labels unknown

All three label rows have `target_trip_count=NULL`, `label_status=UNOBSERVED` and a null label-availability time. The daily checks confirm this state; the notebook does not fit or score a model.

There are no observed supervised targets for this horizon. Replacing null with zero would assert complete observation of an empty hour, which the fixture does not provide. Further modelling would need observed outcomes, suitable history and separate validation; it is not required for final submission.

## 8. Export without overstating deployment

Lab 08 writes eight small CSV files, rereads their headers and values, and records their hashes. Keep null meaning and field types with the files. Blank label targets must not become zeros during import. [D5-6]

Import into a desktop BI tool is optional; its connector is not part of the verified notebook. No paid service, live dashboard, API or feature-store deployment is needed. Required evidence is the executed notebook, exports, SQL reconciliation and your explanation. Follow [completion](COMPLETION.md) and [submission](../project/SUBMISSION.md).
