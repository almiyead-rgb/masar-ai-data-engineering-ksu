# Day 3 · Change and safety policy

[Course home](../README.md) · [Execution record](../STATUS.md)

## Operational scope

The only approved business change to trusted Silver is correction.csv, assigned source_revision=2, for SYN_T0001. Preserve every raw source file. Do not rerun insert-only Day 2 transformations over Day 3 corrections.

## Revision decision table

- Missing key → insert a valid new trip.

- Higher revision → update.

- Same revision + identical payload → preserve values.

- Lower revision → ignore stale data.

- Same revision + different payload → stop before MERGE.

## Sandbox boundary

Constraint probes, schema evolution, compaction and DELETE/RESTORE are written into fresh `sandbox/day03/` tables with independent data files. These are not shallow clones. The helper rejects maintenance paths outside that directory, parent traversal and symlinks.

## Protected operations

Do not edit `_delta_log`, remove Parquet files manually, overwrite previous runs, or turn off retention safety. VACUUM in this lab is dry-run only with at least 168 hours. A successful dry run is not proof that any expired files were deleted.

## Expected failure means a specific failure

A negative test passes only when the intended schema/constraint error occurs and the table’s committed state remains unchanged. Unexpected engine errors are re-raised. The negative-fare test includes one valid row in the same write to check that partial acceptance does not occur.

## What to compare

Expected current values: 75 unique trips, 1880.60 SAR, one source revision 2. Compare the canonical business digest; do not compare physical filenames or elapsed times across runs. The schema sandbox has an extra field, but trusted Silver keeps its existing contract.

## Restart without losing work

A completed 4a rerun rechecks current values without claiming to repeat historical tests. 4b creates new copies each time. An incomplete attempt or a changed later-day table is preserved and reported, not reset silently. Restore a fresh end-to-end workspace for a clean full repeat; retain the previous attempt for diagnosis.
