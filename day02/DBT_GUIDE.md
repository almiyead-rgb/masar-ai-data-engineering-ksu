# Lab 03 · Understand and run dbt

[Day 2](README.md) · [Student notebook](STUDENT.ipynb) · [Project files](dbt/README.md)

## 1. Give each tool a clear role

Spark executes SQL; Delta manages table transactions; dbt organizes SQL models, dependencies, tests and documentation through its Spark adapter. `source()` refers to an existing source table. `ref()` links one model to another. Neither function ingests the raw CSV.

## 2. Follow the six-model graph

`stg_trips`: typed trip receipts.

`stg_drivers`: unique, standardized drivers.

`stg_gps`: parsed and validated events.

`int_trip_candidates`: one validated candidate per trip.

`silver_trips`: incremental Delta table.

`mart_city_daily`: one summary per city and local trip date.

Trips and drivers feed the candidate model, then Silver, then the city/day summary. GPS is a separately tested branch; raw events are not joined into trip fares. Explore [models/](dbt/models/) without copying the same SQL into multiple files.

## 3. Use the notebook runner

After 03a and 03b, run the dbt cell in the same daily notebook. `run_dbt_lab(ROOT)` creates an isolated workspace, copies actual Day 1 Delta snapshots while preserving their receipt timestamps, and invokes dbt in one local Spark session. It needs no cloud account, token or Thrift server.

Do not run `dbt build` in a separate process for this setup: its in-memory catalog would not contain the registered source tables. Generated files stay under the printed dbt workspace, not in the tracked `day02/dbt/` project or your continuing Silver table.

## 4. Validate before merging

Each phase builds staging, runs domain/relationship/conflict checks, checks source freshness, builds the remaining models and tests, then reads Delta back. A failed pre-merge check stops the phase. A failed later test does not turn multiple models into one rolled-back transaction.

Read [schema.yml](dbt/models/schema.yml) for key and null tests, and [tests/](dbt/tests/) for seven SQL tests. Trip receipts intentionally repeat `trip_id`; driver keys, candidate keys and Silver trip keys must be unique. A `unique_key` configuration is not itself a uniqueness test. [D2-3, D2-6, D2-8]

## 5. Look back on arrival time

[silver_trips.sql](dbt/models/silver/silver_trips.sql) filters candidates using `_ingested_at` relative to the latest target timestamp minus three days. It does not filter by the trip event date. A historical trip arriving now can therefore be included.

The candidate model first ranks the complete small source history, after conflict checks, so a replayed older revision cannot replace a newer one. This prioritizes correctness for the small fixture; it is not a claim of optimized scanning at production scale. [D2-6]

## 6. Distinguish backfill from a full rebuild

The supplied late-trip batch is the required backfill exercise: retain the older business date and count each trip once. `--reprocess-all` is an optional runner switch that removes the ingestion-window filter while retaining conflict and revision rules. It covers available history only; it cannot recreate records absent from the sources.

It is not `--full-refresh` and does not delete previous work. Leave `--include-correction` off during Day 2; that optional validation belongs to a later stage. No extra submission is required.

## 7. Interpret freshness correctly

The current classroom settings in [sources.yml](dbt/models/sources.yml) warn after 24 hours and fail after 48 hours, using the actual `_ingested_at`. These are exercise settings, not an organizational SLA. Warnings remain visible; errors stop the phase. Do not replace old receipt timestamps with the current time to force success.

The runner invokes `dbt source freshness` separately before each build; `dbt build` does not include it automatically. Historical trip dates are not arrival timestamps. When resuming old inputs, preserve them and use a new Day 1 workspace for a fresh end-to-end attempt. [D2-7, D2-8]

## 8. Compare the four printed results

The [executed notebook](STUDENT.ipynb) records:

`base`: 72 trips, SAR 1,794.60.

`rerun`: 72 trips, SAR 1,794.60.

`late`: 75 trips, SAR 1,875.60.

`late_replay`: 75 trips, SAR 1,875.60.

Check your own output and the returned `PASSED_DBT_NATIVE` status. The runner compares complete business rows and summary totals with an independent reference and verifies real Delta files. Different log timestamps or invocation IDs are expected across runs.

## 9. Retain the lineage documentation

The catalog must describe six real model relations and three source tables. Its schema metadata is read from Spark; temporary session views are not persistent project tables. Each command retains its own target directory and invocation identity.

Keep `index.html`, `manifest.json` and `catalog.json` together under `dbt/commands/documentation/target/` in the printed dbt workspace. The daily handoff includes them. Explain the model connections and your replay results in `student/day02/LAB03_NOTES.md`.

[References D2-1–D2-8](SOURCES.md) · [Completion and handoff](COMPLETION.md) · [Day 2 execution evidence](verification.json)
