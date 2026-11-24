# Lab 04 · Correct, inspect and recover

[Day 3](../../README.md) · **[Student notebook](../../STUDENT.ipynb)** · [Change rules](../../CHANGE_POLICY.md)

## 1. Open the Day 2 workspace

Complete the setup section in `day03/STUDENT.ipynb`. The printed `Continue workspace:` identifies your continuing workspace. The notebook also checks the Day 2 Silver report and actual table contents before the transaction experiment.

The starting table has 75 unique trips and SAR 1,875.60 in total fares. Restore your own Day 2 handoff at the repository root when changing sessions. A pointer without its Delta folders is incomplete. Do not rebuild Silver from the optional reference notebook.

## 2. Run 04a and read the correction

Run the second code cell, which calls `run_transactions_lab`. It reads the existing Delta table, records its current version, and lands `correction.csv` as a separate Bronze receipt. The scenario assigns source revision 2; that revision is not a field invented inside the original CSV.

For `SYN_T0001`, the fare changes from **SAR 18.00 to SAR 23.00**. The table still contains **75 trips**; its total rises by SAR 5.00 to **SAR 1,880.60**. Inspect `before` and `after_correction` in the printed result. These objects show actual versions, schema, row counts and business-content hashes.

## 3. Understand the three replay decisions

The same 04a cell tests these cases:

**Same correction again:** retain SAR 23.00 and 75 trips.

**Older revision arrives:** ignore the old SAR 18.00 value.

**Same revision, conflicting fare:** reject the transient SAR 24.00 probe before MERGE.

The shared [revision_merge_delta function](../../../src/masar/delta_lab.py) enforces this application policy and checks source/target key uniqueness. Delta does not automatically know which business revision is authoritative. Compare `after_correction`, `after_replay` and `after_stale_replay` in `reports/day03_transactions.json`; their business-content hashes must agree. Physical versions need not match.

## 4. Read the past and inspect a rejected write

04a reads the version recorded before correction using `versionAsOf`. The earlier row has the SAR 18.00 fare; current Silver has SAR 23.00. Reading history does not replace the current table.

It then creates an independent copy with fare and key-presence constraints. One append contains a valid probe and the negative-fare case `SYN_BAD002`. The expected constraint violation rejects the whole write. Check `constraint_probe.committed_table_unchanged` and the before/after state in the report.

An expected constraint message can appear in logs while the cell completes successfully. The intended rejection and unchanged committed table are the evidence; an unrelated exception or an uncaught notebook error is not a pass.

## 5. Run 04b: change a copy’s schema

Run the third code cell, which calls `run_maintenance_lab` after 04a passes. It creates a new copy containing the other 74 trips, excluding `SYN_T0002`. This avoids duplicating an existing trip when its extended row is added.

The first append of `schema_change.csv` is rejected because `surcharge_sar` is unexpected. A second append explicitly allows that field for this write with `mergeSchema=true`. Inspect the maintenance report: **75 unique trips, 74 null surcharges and one surcharge of SAR 2.00**.

The surcharge is a separate field, not a change to `fare_sar`. The original Silver schema and its corrected fares remain unchanged. Do not enable automatic schema evolution for the whole session.

## 6. Inspect compaction and recovery

In a separate compaction copy, 04b records `numFiles` and `sizeInBytes` before and after `OPTIMIZE`. It checks that business values are unchanged. Read the `optimize` object in the report; record what happened rather than claiming a guaranteed speedup.

A different recovery copy follows **75 → 74 → 75 rows**: create the copy, delete `SYN_T0001`, then restore the pre-delete state. Inspect the printed `recovery` object and history. RESTORE creates a later commit; it does not turn the version number backward. These operations do not delete a row from the continuing Silver table.

## 7. Preview cleanup only

The final maintenance operation is `VACUUM ... RETAIN 168 HOURS DRY RUN` on the recovery copy. Check the printed `vacuum` object: `dry_run_only` is true and `files_deleted_by_vacuum` is zero. An empty candidate list is expected for newly created files.

Keep retention safeguards enabled. Do not remove Parquet files or edit `_delta_log` manually. Actual cleanup can remove files needed to read or restore older versions; it is outside this exercise. See [D5 and D8](../../SOURCES.md).

## 8. Save evidence and continue

Read `reports/day03_transactions.json` and `reports/day03_maintenance_latest.json` under the printed `WORK` path. Record your explanation in `student/day03/LAB04_NOTES.md`; use [the questions](../../PRACTICE.md) as prompts.

Complete **Save this day** to create `outputs/day03_handoff.zip`, including cumulative outputs and the earlier dbt evidence. Keep the executed notebook separately and upload the extracted small GitHub bundle to your repository. Retain earlier Drive archives as recovery points.

If 04a has already completed, rerunning it verifies the current corrected table and uses its saved report; it does not repeat every historical test. 04b makes fresh copies on each run. For a completely fresh experiment, keep the old workspace and repeat the earlier days in a new workspace. Follow [the completion checklist](../../COMPLETION.md).
