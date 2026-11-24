# Data dictionary: Masar Small v1

[Course home](../README.md) · [Start here](../docs/START_HERE.md) · [Dataset files and integrity](README.md)

Use this dictionary when you inspect the source, select business keys and explain the output columns. The dataset describes a fictional mobility service in Riyadh, Jeddah and Dammam. All identifiers, trips, ratings and coordinates are synthetic.

The fixed starting inputs contain **72 trips, six drivers and 216 GPS events**. Other files introduce late trips, an approved correction, invalid records and a schema change. A delivery of a file and a business record inside that file have different identities.

## Trip source fields

The trip CSV files use the following fields. Bronze preserves the source values as strings; the Silver stage applies the [typed data contract](../day02/DATA_CONTRACT.md).

| Source field | Meaning | How you use it |
|---|---|---|
| `trip_id` | Synthetic trip business key, such as `SYN_T0001`. | Require a nonblank key. A conformed Silver table contains one authoritative row per trip. Repeated delivery of that ID does not create another trip. |
| `driver_id` | Synthetic foreign key into `drivers.csv`. | Require exactly one matching driver before joining descriptive fields. It is not a real person's identity. |
| `city` | City text. | Trim and normalize the value to `Riyadh`, `Jeddah` or `Dammam`. |
| `start_ts` | ISO 8601 trip-start timestamp with an explicit offset. | Parse to `start_utc`; derive the business date from the start in `Asia/Riyadh`. |
| `end_ts` | ISO 8601 trip-end timestamp with an explicit offset. | Parse to `end_utc`; require an end after the start. A completed trip's end is not information available at its start. |
| `fare_sar` | Synthetic fare in Saudi riyals. The valid fixture uses exact two-decimal values. | Keep exact decimal precision. The reference calculations use integer halalas or Decimal; native Silver uses `decimal(12,2)`. Reject negative, non-finite, overflowing or excessively precise values. |
| `distance_km` | Final trip distance in kilometres, with two decimal places in the fixture. | Require a positive value. A final distance is not a trip-start AI input. |

`schema_change.csv` also contains `surcharge_sar`. The schema-evolution experiment uses it in an isolated sandbox. It is not silently added to the continuing production-like Silver contract.

## Driver source fields

| Source field | Meaning | Contract |
|---|---|---|
| `driver_id` | Synthetic driver key, such as `SYN_D001`. | Unique and nonblank in the driver input. |
| `vehicle_type` | Synthetic vehicle category. | `sedan` or `suv`. |
| `driver_rating` | Synthetic reference rating on a 0–5 scale. | Descriptive reference data. The fixture does not provide rating history, so the course does not treat it as a historically available AI feature. |

## GPS event source fields

Each line in the NDJSON feed is a JSON event. The base feed contains three events per original trip.

| Source field | Meaning | Contract |
|---|---|---|
| `event_id` | Synthetic event business key. | Deduplicate business events by this key. Kafka offsets identify message positions and can differ for two deliveries of the same event. |
| `trip_id` | Trip associated with the event. | Links the event to a trip; it is not the event's unique key. |
| `city` | City recorded by the event. | Normalize and validate against the permitted cities. |
| `event_ts` | Event timestamp with explicit offset. | Convert to UTC for processing. Event time can differ from delivery time. |
| `location.lat` / `location.lon` | Coarse fictional latitude and longitude. | These values are educational coordinates. They do not identify an actual person or route. |
| `synthetic` | Explicit fixture marker. | `true` in the supplied base events. |

Bronze initially retains each GPS line as `raw_json`. Later native stages parse it; Silver GPS uses fields including `event_utc`, `latitude` and `longitude`. Inspect the notebook schema before querying a stage: source field names and conformed field names are intentionally different.

## Scenario metadata and availability

The [scenario schedule](masar-small-v1/scenario_schedule.json) defines the fixed teaching order and `available_at` timestamps. It is source-availability metadata, not a record of a real Kafka run or a watermark test.

| Field | Meaning |
|---|---|
| `revision` | Authoritative source revision assigned by the fixed scenario schedule. It is not inferred from a filename's modification time or from the current clock. Native Silver calls this `source_revision`. |
| `available_at` | When that scenario's delivery becomes available in the fixture. The AI input builder uses the earliest availability for a trip and revision; a replay does not create newer historical knowledge. |
| `file` / `name` | The source filename and scenario identifier. |

A higher approved revision can replace an older value. Two conflicting payloads at the same revision are rejected. On Day 3, revision 2 sets `SYN_T0001.fare_sar` to **23.00**, replacing revision 1's **18.00**. Replaying revision 2 leaves the value at 23.00.

## Generated fields are not source columns

| Field | Where you see it | Meaning |
|---|---|---|
| `_source_file` | Bronze and native Silver provenance | Source filename. |
| `_source_sha256` | Bronze and native Silver provenance | Integrity hash of the source file. |
| `_batch_id` | Bronze | Delivery identity. Several receipts may refer to the same business record. |
| `_ingested_at` | Bronze | Actual ingestion timestamp in UTC. It can differ between valid runs. |
| `_payload_hash` | Native Silver | Hash used to detect conflicting business payloads. It is separate from a file's hash. |
| `source_revision` | Native Silver | Approved business revision, derived from the scenario policy. |
| `trip_date_local` | Native Silver and serving products | Date of the trip **start** in Asia/Riyadh. A trip crossing midnight belongs to its start date. |
| `duration_seconds` | Native Silver and serving products | Full positive end-minus-start duration in whole seconds. |

Earlier conceptual examples use the names `trip_date_riyadh` and `duration_min` for the same local-start-date idea and a duration expressed in minutes. They are **not columns in the native Silver schema**. Use the exact native names and units above in your notebook. The final AI target in this course is a future hourly trip count, stored separately from its historical feature inputs; it is not `duration_min`.

## Read serving columns with their product contract

Day 5 publishes eight products with different grains. Their exact keys, units, null meaning and expected row counts are defined in [Data products](../day05/DATA_PRODUCTS.md) and [AI/BI input policy](../day05/AI_BI_GUIDE.md). In particular, `target_trip_count=NULL` with `label_status=UNOBSERVED` means future ground truth has not been observed. It does not mean zero demand.

This small fixture supports reasoning about pipeline correctness. It cannot establish production throughput, real demand, a model's predictive quality or legal compliance. Source-file replay alone does not establish Kafka delivery behavior; use the actual producer, consumer and checkpoint evidence from Day 4.
