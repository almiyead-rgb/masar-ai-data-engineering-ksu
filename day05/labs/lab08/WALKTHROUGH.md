# Lab 08 · Read, reconcile and export

[Day 5](../../README.md) · **[Student notebook](../../STUDENT.ipynb)** · [AI/BI guide](../../AI_BI_GUIDE.md)

## 1. Continue after Lab 07

Run the third code cell, labelled **08**, after the recovery cell has passed. It calls `run_serving_lab`, checks the result, prints the reporting and AI examples, and stops its Spark session.

This cell performs the steps below automatically. The [shared implementation](../../../src/masar/serving.py) is the code to inspect; do not copy it into a parallel solution. No running Kafka broker is needed to read these completed Delta outputs.

## 2. Select the complete release

`read_release` follows `reports/day05_gold_latest.json`, checks the manifest hash and release ID, requires exactly the eight expected tables, and reads their recorded Delta versions. It compares actual row counts and logical contents with the manifest.

Do not read every release folder and combine the files: the failed candidate remains beside good releases for diagnosis. Product names such as `bi.fact_trips` map to paths in the manifest; they are not automatically available as named SQL tables in a new session.

## 3. Check the exports

The helper writes one CSV for each validated table under `reports/serving/<export_id>/`. It rereads each file, checks column names and row values, and records the row count and SHA-256. The `exports` object in `reports/day05_serving_latest.json` gives the exact paths.

For example, the fact file is `bi_fact_trips.csv`, and the labels file is `ai_zone_hourly_labels.csv`. Empty fields represent null; booleans are text. Keep [the contracts](../../DATA_PRODUCTS.md) so the recipient can restore types and units correctly. [D5-6]

## 4. Reconcile the Spark SQL summary

The same call registers the pinned fact table as `masar_day05_fact` and executes [the supplied SQL file](../../sql/bi_zone_summary.sql) while Spark is active. Inspect the printed `BI totals`: Dammam 25 / SAR 670.40, Jeddah 25 / SAR 625.20, Riyadh 25 / SAR 585.00.

Confirm the grand total of 75 trips and SAR 1,880.60. The fact's event counts sum to 217 because events were aggregated per trip before joining. The query is already executed by the cell; opening the SQL file is for reading, not an instruction to rerun it after the cell has stopped Spark.

## 5. Interpret the feature and label examples

The notebook prints one row from each AI table. At `as_of_utc=2026-06-04T03:05:00Z`, the Dammam example has eight completed trips and a historical mean duration of 1,470.00 seconds. Its `prediction_hour_utc` is 04:00 UTC; it is not a prediction value.

The corresponding label example has `target_trip_count=None` and `label_status=UNOBSERVED`. Inspect the two CSV exports for all three city rows. Refer to [the cutoff, availability rules and four-field allowlist](../../AI_BI_GUIDE.md). No model is trained or evaluated.

## 6. Check the report and archive

All 16 printed serving checks must pass. Open `reports/day05_serving_latest.json` and confirm that `source_release_id` identifies the selected successful release. Retain its export paths and hashes with the report.

Complete **Save this day** to create `outputs/day05_handoff.zip`. It includes the cumulative outputs, successful-workspace pointer and earlier dbt evidence. Save the executed notebook separately, upload the extracted small GitHub bundle and keep your earlier Drive archives as recovery points. If you rebuild Lab 07, run Lab 08 again before recreating the final archive.

## 7. Submit the work you have already built

Write your daily answer in `student/day05/REFLECTION.md` and your BI/AI run observations in `student/day05/LAB08_NOTES.md`, use [the final-day checklist](../../COMPLETION.md), and follow [the shared submission guide](../../../project/SUBMISSION.md). Include the programme, SDAIA Academy, its link and `#SDAIAAcademy` in the stated places.

Do not add a separate model, dashboard or new dataset to satisfy this lab. Do not force generated output folders into Git. The optional inventory and all-days diagnostic tools are not extra passing conditions; their limited roles are explained in [the integration guide](../../INTEGRATION.md).
