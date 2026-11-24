# Day 5 · Eight output tables

[Day 5](README.md) · [Notebook](STUDENT.ipynb) · [AI/BI guide](AI_BI_GUIDE.md)

## Read the contract before the file

The names below identify products within a release, not eight extra labs or automatically registered SQL tables. Their Delta paths are under `mini_lakehouse/serving_releases/<release_id>/`. Read the selected release manifest rather than guessing a folder.

[TABLE_COLUMNS and TABLE_KEYS](../src/masar/serving_reference.py) define the exact columns and keys; [build_frames](../src/masar/serving.py) creates the actual Spark outputs. Counts below describe the fixed synthetic fixture, not production targets. Fares use SAR with two decimal places, distances kilometres and durations seconds.

## 1. gold.zone_hourly_demand

**Grain:** one observed city proxy and UTC trip-start hour.

**Key:** `zone_key + hour_utc`.

**Other fields:** `hour_local`, `trip_count`, `total_fare_sar`, `total_duration_seconds`.

**Fixture:** 75 groups; summed trip counts equal 75.

`hour_local` carries the +03:00 display offset. Only observed hours appear. The name “demand” means observed trip starts here, not all requests or measured market demand. Having 75 rows is coincidental for this fixture; a group can contain several trips in other data.

## 2. gold.driver_daily

**Grain:** one driver and local trip-start date.

**Key:** `driver_key + trip_date_local`.

**Measures:** `trip_count`, `total_fare_sar`, `total_duration_seconds`.

**Fixture:** 18 groups.

Sum the measures to reconcile with the same 75 trips and SAR 1,880.60; do not compare the 18 group rows directly with the trip count.

## 3. bi.dim_zone

**Grain and key:** one unique `zone_key`.

**Descriptions:** `city` and `zone_resolution`.

**Fixture:** three rows: `Z_RIYADH`, `Z_JEDDAH` and `Z_DAMMAM`.

`zone_resolution=city_proxy` states the real level of this teaching definition. The data does not establish neighbourhoods or service-zone boundaries.

## 4. bi.dim_driver

**Grain and key:** one unique `driver_key`.

**Other fields:** `driver_id` and `vehicle_type`.

**Fixture:** six synthetic drivers.

The simple natural key equals the synthetic source ID. This dimension does not implement changing-dimension history. Its descriptive fields are not automatically approved AI inputs.

## 5. bi.dim_date

**Grain and key:** one local date, keyed by integer `date_key` in YYYYMMDD form.

**Other fields:** `date_local`, `year`, `month`, `day`.

**Fixture:** June 1, 2 and 3, 2026.

The date follows the trip start in Asia/Riyadh. This compact dimension covers observed dates only; it is not a full BI calendar.

## 6. bi.fact_trips

**Grain and key:** one unique `trip_id`.

**Dimension keys:** `driver_key`, `zone_key`, `date_key`.

**Values:** `start_utc`, `fare_sar`, `distance_km`, `duration_seconds`, `gps_event_count`.

**Fixture:** 75 rows.

Events are counted per trip before the join. The three late trips remain even without GPS events; their recorded event count is zero. Total recorded events are 217. No raw coordinates are exported in this table.

## 7. ai.zone_hourly_features

**Grain and key:** one `zone_key + as_of_utc + prediction_hour_utc`.

**Historical values:** `completed_trips_24h`, `avg_duration_seconds_24h`, `history_available`.

**Audit fields:** `history_window_start_utc` and `max_source_available_at_utc`, alongside the cutoff and horizon.

**Fixture:** three rows.

Include trips ending in `[cutoff − 24 hours, cutoff)` whose source revision was available by the cutoff. If eligible history is absent, the count is 0, the mean is null and `history_available=false`; this does not prove zero real-world activity. Read [the fixed cutoff and input allowlist](AI_BI_GUIDE.md).

## 8. ai.zone_hourly_labels

**Grain and key:** one `zone_key + prediction_hour_utc`.

**Other fields:** `target_trip_count`, `label_status`, `label_available_at_utc`.

**Fixture:** three rows, all `UNOBSERVED`, with null targets and null label-availability times.

These rows document unavailable future ground truth. They are not three training examples with a zero target. The allowed inputs and future labels must remain separate.

## Retain versions and export meaning

The release manifest records each table's path, Delta version, row count and canonical-content hash. Lab 08 rereads those versions and exports one CSV per product, replacing dots in the product name with underscores.

The small CSV writer represents `None` as an empty field and writes booleans as text. CSV does not carry the Delta schema: preserve this contract, units and null meaning. A file hash checks integrity, not the truth of an execution claim. See [D5-6](SOURCES.md) and [completion](COMPLETION.md).
