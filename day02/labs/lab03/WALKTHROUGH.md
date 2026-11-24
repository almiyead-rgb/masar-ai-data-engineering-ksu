# Lab 03 · Build Silver step by step

[Day 2](../../README.md) · [**Student notebook**](../../STUDENT.ipynb) · [Field rules](../../DATA_CONTRACT.md)

## 1. Open the correct workspace

Complete the setup section in `day02/STUDENT.ipynb`. It checks the fixed dataset, the environment and the successful Day 1 pointer. `Continue workspace:` should identify your existing output folder.

Use the complete repository. On a new session, restore your own Day 1 handoff first. Do not substitute a CSV for a missing Delta table. This day reads the original snapshots: trips version 1, drivers version 0 and GPS version 0.

## 2. Part 03a: type and standardize the data

Run **Lab 03a: stage and validate**. `run_staging_lab` prepares three Delta snapshots: `stg_trips`, `stg_drivers` and `stg_gps`. Inspect the printed sample and the checks before continuing.

Expected staging counts: **144 trip receipts, 6 drivers and 216 GPS events**. A repeated trip in the sample is correct at this point: typing is not deduplication. For example, the two receipts for `SYN_T0001` both retain the fare `18.00`.

Known city labels are standardized, decimal values are checked and timestamp offsets are parsed once. The trip date remains its local start date in Asia/Riyadh, even when the corresponding UTC date differs.

## 3. Check relationships before choosing a row

The shared implementation rejects duplicate driver keys and missing driver relationships before enrichment. A valid trip-to-driver join preserves the receipt count. Conflicting business values at the same source revision also stop processing; they are not ordinary duplicates.

Only identical receipts are reduced using a deterministic ordering. You obtain one candidate per `trip_id`. Do not join the 216 raw GPS events directly into a fare total: each base trip has three events, so that join would count its fare three times.

Read `validate_staging` and `silver_candidates` in [the shared implementation](../../../src/masar/silver.py). These functions are already called by the notebook; you do not need to copy them into new cells.

## 4. Part 03b: build Silver and test replays

Run **Lab 03b: merge late data safely**. It validates the staging report, creates or verifies the Silver Delta table, and checks five scenarios. Each row below gives **Bronze receipts / Silver trips / total fares in SAR**.

Base: **144 / 72 / 1,794.60**

Transform rerun: **144 / 72 / 1,794.60**

Late batch `late_003`: **147 / 75 / 1,875.60**

Retry the same batch: **147 / 75 / 1,875.60**

New delivery `late_replay_004`: **150 / 75 / 1,875.60**

Day 2 MERGE inserts missing keys and leaves identical existing business rows unchanged. [Delta and dbt references](../../SOURCES.md) explain why the source key must be unambiguous before MERGE.

## 5. Explain the late-arrival result

The three late trips add **SAR 81.00**. They belong to June 1, 2026 even though the scenario delivers them on June 4. Counts by local trip date become **27, 24 and 24** for June 1, 2 and 3.

A filter such as `trip_date_local = current_date()` asks for trips occurring today; it does not ask which records arrived since the previous run. With this historical fixture it may return no rows at all. The dbt model uses the ingestion clock for its lookback instead.

Open `reports/day02_silver.json` under the printed workspace to inspect all five scenario records. Successful checks compare full business content, not just counts. Transaction versions and runtime durations may differ between correct runs.

## 6. Run dbt in the same daily notebook

Read [the dbt guide](../../DBT_GUIDE.md), then run **Lab 03: run dbt**. The runner uses isolated copies of the original Bronze snapshots. It does not replace the Silver table that will continue to Day 3.

Inspect the returned status `PASSED_DBT_NATIVE` and the four printed phases: `base`, `rerun`, `late` and `late_replay`. The row counts are **72, 72, 75, 75**; the corresponding totals are **1,794.60, 1,794.60, 1,875.60, 1,875.60 SAR**.

The report also verifies the generated catalog against **six real models and three real source tables**. The separate same-batch retry is exercised by 03b; it is not a missing fifth dbt phase.

## 7. Read the models and tests

Open [stg_trips.sql](../../dbt/models/staging/stg_trips.sql) to trace field conversion and [silver_trips.sql](../../dbt/models/silver/silver_trips.sql) to inspect the three-day ingestion lookback. Use [schema.yml](../../dbt/models/schema.yml) for key/null tests and [tests/](../../dbt/tests/) for the seven SQL tests. Record what `source()` and `ref()` connect.

In this pinned local-session setup, use the notebook runner rather than starting `dbt build` in an unrelated process. See the guide for the freshness clock, retained documentation and the optional all-history reprocessing switch.

## 8. Save the stage and handle errors safely

Complete the **Save this day** section to create `outputs/day02_handoff.zip`. It contains the successful-workspace pointer, your cumulative Delta files and reports, and the isolated dbt workspace with its generated documentation. Save the executed notebook and `student/day02/LAB03_NOTES.md` separately.

If a check fails, stop at that cell and retain its message. Do not delete previous outputs, bypass assertions or rerun Day 2 over a table already corrected on Day 3. Use [the completion and recovery guidance](../../COMPLETION.md).

[The calculation reference](../../REFERENCE.ipynb) is optional; it helps explain the expected values but is not another required execution route.
