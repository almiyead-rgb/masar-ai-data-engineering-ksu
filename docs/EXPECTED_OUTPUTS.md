# Compare your results

Use this page as the **expected-value contract** for the fixed `MASAR_SMALL_V1` dataset. The published [execution record](VERIFICATION.md) identifies actual tested runs and their environment. Your own notebook and reports are your evidence.

## Daily checkpoints

| Stage | Expected result | What it means |
|---|---|---|
| Initial source | 72 trips, 6 drivers, 216 GPS events | Different source grains |
| Day 1 Bronze replay | 144 trip receipts, 72 distinct trip IDs | Two deliveries of the same business trips |
| Day 2 base | 72 Silver trips; SAR 1,794.60 | Base population after deduplication |
| Day 2 late data | 75 Silver trips; SAR 1,875.60 | Three additional trips add SAR 81.00 |
| Day 2 final replay | 150 Bronze receipts;75 Silver trips | New delivery evidence without new business trips |
| Day 2 dbt phases | Counts 72,72,75,75 | Base, rerun, late, late_replay |
| Day 3 correction | SYN_T0001 fare 18.00→23.00;75 trips;SAR 1,880.60 | Apply the approved revision once |
| Day 3 correction replay | Fare remains 23.00 | No repeated addition of the difference |
| Day 4 stream | Receipts 216,216,218,219; distinct events 216,216,216,217 | Restart, duplicate deliveries and one late new event |
| Day 4 quality | Candidate 82 fails;7 quarantined; new 75candidate passes | Fail closed, preserve reasons, revalidate |
| Day 5 reporting | 75 trips;SAR 1,880.60;217 events | Consistent measures across products |

## Final products

| Product | Grain | Expected rows |
|---|---|---:|
| `gold.zone_hourly_demand` | Observed city proxy and UTC trip-start hour | 75 |
| `gold.driver_daily` | Driver and local trip-start date | 18 |
| `bi.dim_zone` | Unique city proxy key | 3 |
| `bi.dim_driver` | Unique driver key | 6 |
| `bi.dim_date` | Observed local date | 3 |
| `bi.fact_trips` | Unique trip ID | 75 |
| `ai.zone_hourly_features` | City, cutoff and prediction horizon | 3 |
| `ai.zone_hourly_labels` | City and prediction horizon | 3 |

Read [the product contracts](../day05/DATA_PRODUCTS.md). These names identify path-based products in the release manifest; do not assume they are automatically registered SQL tables.

## BI comparison

| City | Trips | Total fares(SAR) |
|---|---:|---:|
| Riyadh | 25 | 585.00 |
| Jeddah | 25 | 625.20 |
| Dammam | 25 | 670.40 |
| Total | 75 | 1,880.60 |

Aggregate distinct GPS events per trip before joining to fares. A direct trip-to-many-events join can repeat the fare.

## AI comparison

At the fixed cutoff `2026-06-04T03:05:00Z`(06:05Riyadh), each city has eight eligible completed trips in the historical window. Mean durations are Riyadh 1230 seconds, Jeddah 1350 seconds and Dammam 1470 seconds. The target horizon starts at 04:00UTC(07:00Riyadh). The future labels are **NULL** with **UNOBSERVED** status. They are not observed zeros, and this fixture does not produce a supervised-model accuracy score.

## Compare meaning before formatting

**Must satisfy the contract:** business keys, fields, row counts, decimal fare totals, accepted/rejected decisions and output relationships.

**Can vary:** runtime duration, startup time, temporary paths, execution UUIDs, file names and some transaction-version numbers after different correct rerun histories.

**Expected failures:** the invalid Delta write, the 82-row quality candidate and the deliberately failed serving candidate. Verify their protective behavior rather than deleting the failed record.

An expected value written in a document is not a fresh engine output. The reference notebooks/reports show their execution scope; retain your own run with the source version and runtime report.
