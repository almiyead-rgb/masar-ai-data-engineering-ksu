# Lab 07 · Follow the good, failed and recovered builds

[Day 5](../../README.md) · **[Student notebook](../../STUDENT.ipynb)** · [Output definitions](../../DATA_PRODUCTS.md)

## 1. Open the continuing workspace

Complete the setup section in `day05/STUDENT.ipynb`. `Continue workspace:` identifies the existing `WORK` folder. On a new session, restore your own Day 4 handoff at the repository root before this step.

The pointer still has the Day 1 filename because the workspace is cumulative. Day 5 additionally needs the completed Day 4 reports and actual approved Delta tables; a Day 1-only workspace is not enough.

## 2. Run the Lab 07 cell once

The second code cell calls `run_recovery_exercise` from [serving.py](../../../src/masar/serving.py). It starts Spark without Kafka, performs the sequence below, prints four checks and stops Spark. Wait for that cell to finish before Lab 08.

The remaining steps explain what this same call does and which reports to inspect. You do not need to invoke the helper functions individually or supply a new dataset.

## 3. Verify and pin the two inputs

`load_validated_inputs` checks the Day 4 quality and stream reports, their required checks and fixed dataset identity. It reads the quality-approved table and distinct-event table named by those reports, records each current Delta version, then reads that version explicitly.

The approved trip contents must match the corrected 75 trips, and the event snapshot must contain 217 distinct events matching the source. The successful release's `inputs` object records paths, versions, row counts and hashes of the two prerequisite reports. The quarantined candidate is not an input.

## 4. Trace the Spark transformations

`build_frames` maps cities to explicit city proxies, counts distinct events per trip before joining, builds two Gold summaries and three dimensions plus the fact table, and prepares separate feature and label tables. See [all eight contracts](../../DATA_PRODUCTS.md).

Spark builds the fact rows and aggregates from actual Delta inputs. A separate source-derived calculation checks the results; it does not supply substitute rows to the native tables. Keep the one-trip grain when checking fares.

## 5. Select the first good release

Each table is written with `errorifexists` under a new release ID. The helper rereads Delta, checks schema and keys, and compares the canonical business contents. After all eight pass, it saves `mini_lakehouse/serving_releases/<release_id>/release.json` and updates `reports/day05_gold_latest.json`.

The manifest records each table's path, version, row count and content hash. Updating this local pointer means the supplied reader can select a complete release; it is not a global multi-table transaction. [D5-1, D5-2]

## 6. Inspect the intentional failure

A second candidate fails after writing its first table. Only the deliberate `InjectedFailure` is handled as expected. The helper checks that the previous pointer bytes are unchanged and rereads the former good release successfully.

Find the failure record under `reports/day05_failures/<candidate_id>.json`. It should identify the written table, the deliberate error, no completed release manifest and preservation of the previous pointer. Partial table files remain for diagnosis. Their existence is not a complete release, and an unrelated exception must not be ignored.

## 7. Check recovery and continue

A third build succeeds under a new ID. All eight logical-content hashes must match the first good release. Read `reports/day05_recovery.json`: `run_ids` contains the two successful IDs; all four `checks` must be true. The newest good release is now selected.

This is controlled recovery within one Spark session, not a simulated machine crash. In `student/day05/LAB07_NOTES.md`, explain the selected inputs, failed-candidate evidence and recovered release. Use [the daily practice](../../PRACTICE.md), then run [Lab 08](../lab08/WALKTHROUGH.md). Do not delete the failed candidate or manually move the pointer to it. [Optional diagnostics](../../INTEGRATION.md) are separate from this required route.
