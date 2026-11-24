# Day 2 · Silver data contract

[Course home](../README.md) · [Execution record](../STATUS.md)

## Scope and grain

Exactly one row per trip_id. Source revision is 1 for the Day 2 base and late fixtures. Fields describe completed trips and do not by themselves form a leakage-safe ML feature set.

## `trip_id`

string · Non-empty unique business identity.

## `driver_id`

string · Must match one unique driver.

## `city`

string · Riyadh, Jeddah or Dammam.

## `start_utc / end_utc`

timestamp · Offset-aware input; UTC session; end strictly after start.

## `trip_date_local`

date · Start date in Asia/Riyadh, not ingestion date.

## `fare_sar`

decimal(12,2) · Non-negative SAR, two source decimals at most; no silent rounding.

## `distance_km`

decimal(12,2) · Strictly positive kilometers.

## `duration_seconds`

long · Full timestamp difference in whole seconds, strictly positive.

## `vehicle_type`

string · sedan or suv, from the unique driver dimension.

## `driver_rating`

decimal(3,1) · Between 0 and 5; descriptive fixture attribute, not point-in-time history.

## `source_revision`

integer · 1 today; do not derive from ingestion time.

## `_source_file / _source_sha256`

string · Stable source provenance retained in native Silver.

## `_payload_hash`

string · Native hash used for conflict detection; business comparison excludes operational metadata.

## Rejection policy

Reject unknown cities, missing keys, orphan drivers, invalid times, non-positive duration/distance, negative/non-finite/overflowing fares and excessive decimal precision. Stop before publishing an invalid native table; do not conceal failures by dropping rows. The seven quality fixture records are inspected in reference tests only today.
