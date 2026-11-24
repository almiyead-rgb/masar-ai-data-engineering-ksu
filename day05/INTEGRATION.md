# Day 5 · Complete the existing pipeline

[Day 5](README.md) · [Student notebook](STUDENT.ipynb) · [Completion](COMPLETION.md)

## Required route: continue, do not restart

Complete Day 4, then run the guided sections in [the Day 5 notebook](STUDENT.ipynb). Lab 07 reads the approved trip and event snapshots, builds their outputs and tests controlled recovery. Lab 08 validates the selected release, runs the reporting query and exports it. The final cell saves your working state.

You do not need to rerun all earlier labs, restart Kafka, repeat dbt or submit a second project to complete this day. Your earlier executed notebooks and reports remain part of the same submission.

## What connects the days?

Raw receipts → Bronze → typed staging → unique Silver trips → approved corrections → distinct streamed events and quality approval → eight serving tables → reporting and exports.

The input loader checks `reports/day04_quality_latest.json` and `reports/day04_stream_latest.json`, then reads the Delta paths named in them. It records both actual input versions and report hashes. Do not substitute the quarantine, a schema sandbox or a reference JSON file for these inputs.

## Understand the local release boundary

Each new candidate has its own folder under `mini_lakehouse/serving_releases/`. Each Delta table commits separately. The helper writes `release.json` only after all eight tables pass, and updates `reports/day05_gold_latest.json` last.

The reader follows that pointer, verifies its manifest and reads recorded table versions. A failed candidate can leave files on disk, but this reader does not select them. This is an application-level selection rule, not one atomic transaction across eight tables or a deployment to GitHub.

## Optional diagnostic: fresh all-days integration

[run_day05.py](../scripts/run_day05.py) also supports `--part integration`. This is an optional diagnostic route, not an additional daily task. It starts from fixed sources in a new marked workspace, requires the live local Kafka broker and the Spark/Delta/GX environment, and executes ten stages representing the same eight labs.

Use a separate complete repository copy for this diagnostic. Although previous output folders are retained, a successful new Bronze stage updates that copy's `outputs/day01_bronze_success.json` pointer. Running it in your active project would change which workspace later commands select.

## Read diagnostic results accurately

The optional runner records `reports/integration_stages.json` and stops descendants of a failed stage. Its status `PASSED_NATIVE_PATH_DBT_NOT_VALIDATED` means the native pipeline passed without executing dbt. Keep the separate Day 2 dbt result; do not relabel this status as full-course certification.

The daily notebook does not generate that optional integration journal. Its absence is not a missing Day 5 deliverable. Likewise, `check_submission.py` is an optional file inventory with its own metadata requirements, not the notebook's completion check or an automatic grade.

## Keep test scopes separate

Lab 07's good/fail/rebuild sequence occurs in one Spark session. The course's [saved verification](../docs/VERIFICATION.md) separately records two independent five-day notebook runs. Neither is a distributed load test, crash-recovery test or claim of model accuracy.

Finish with [the daily checklist](COMPLETION.md) and [the single final submission](../project/SUBMISSION.md).
