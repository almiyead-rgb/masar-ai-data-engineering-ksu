# Lab 06 · Make the quality decision explicit

[Day 4](../../README.md) · [Student notebook](../../STUDENT.ipynb) · [Quality rules](../../QUALITY_POLICY.md)

## 1. Run Lab 06 after streaming

The **Lab 06: reject, quarantine and revalidate** section calls `run_quality_lab(spark, SOURCE, WORK)`. It verifies the real Day 3 Silver table and report before evaluating quality. The starting population is 75 unique trips with SAR 1,880.60 in fares.

Read [quality_gate.py](../../../src/masar/quality_gate.py) and [the policy](../../QUALITY_POLICY.md) alongside this guide. The notebook already calls the shared implementation; do not duplicate it. Follow the setup, student tasks, streaming, quality, reflection and save sections in order.

## 2. Understand what GX validates

The helper reads Delta and collects a bounded snapshot, no more than 500 trip rows, into Pandas. GX checks the 12 business columns, expected count, missing values, unique trip keys, known drivers, permitted categories and numeric/time relationships.

Additional row-policy checks parse timestamps, explain root defects and determine whether approval is allowed. This combines actual GX checks with explicit application rules; it is not distributed GX validation on an unlimited Spark table.

A GX Checkpoint runs validation and actions such as Data Docs generation. It is unrelated to Spark's streaming checkpoint directory. [[S6–S9](../../SOURCES.md)]

## 3. Trusted: validate the existing 75 trips

The `trusted` phase must pass both GX and the row policy. It saves its own Checkpoint result and local HTML Data Docs. No source rows are modified.

All 75 rows being valid is not enough if the required population were missing rows. The exact 75-row requirement belongs to this fixed dataset, not to every real pipeline.

## 4. Mixed: observe the intended failure

The helper adds the seven supplied test rows to a **new staging candidate**, not to trusted Silver. This creates 82 rows. GX and the policy must reject that candidate.

Read the seven root reasons: `MISSING_TRIP_ID`, `INVALID_FARE`, `UNKNOWN_DRIVER`, `INVALID_TIMESTAMP`, `INVALID_DURATION`, `INVALID_DISTANCE` and `INVALID_CITY`. One root defect can trigger several GX assertions; do not expect exactly seven failed GX expectations.

## 5. Quarantine with reasons

The application writes seven rejected records to a separate Delta quarantine table and reads it back. The printed table includes `candidate_row`, `trip_id`, `reason_codes`, `raw_business_json`, `rule_version` and `candidate_path`.

`raw_business_json` preserves the projected candidate row for diagnosis; it is not the original CSV text. Original source files remain separate and unchanged. A missing trip ID can appear as null. Do not fill it with an invented ID or discard the failure evidence.

## 6. Rechecked: validate again before approval

The 75 accepted rows become a **new candidate** and receive their own `rechecked` GX result and row-policy evaluation. Only after both pass and the full business contents match trusted Silver does the helper write a new approved Delta snapshot.

Check `Approved rows: 75` and all nine checks. The approved fare total remains SAR 1,880.60. The failed candidate is not relabeled as successful, and the original Silver table is not overwritten.

## 7. Read the reports and Data Docs

Open `WORK/reports/day04_quality_latest.json`. The fields `candidate_table`, `quarantine_table`, `approved_table` and `reports` locate this run's data and reports relative to `WORK`.

Under the reported directory, each of `gx_trusted/`, `gx_mixed/` and `gx_rechecked/` contains `checkpoint_result.json` and its GX project. Use the `data_docs` paths in `gx_results` relative to that phase's GX folder to open the generated `index.html`. Keep the whole folder so its linked assets and validation pages remain available.

Interpret `distribution` and `scenario_freshness` using [monitoring](../../OBSERVABILITY.md). Scenario dates are fixed historical teaching inputs, not measured live-delivery latency.

## 8. Save the approved state

Record the reconciliation `82 = 75 + 7`, reasons and approval decision in `student/day04/LAB06_NOTES.md`. Update your existing governance notes using [the guide](../../GOVERNANCE.md). Then complete **Save this day** and follow [the handoff checklist](../../COMPLETION.md).

A failed mixed-candidate result is expected; an unexpected exception or missing Data Docs is not. Preserve errors and prior outputs. Rerunning the full quality cell creates a separate candidate, quarantine and validation context rather than repairing old evidence in place.
