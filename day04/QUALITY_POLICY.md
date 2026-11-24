# Day 4 · Decide when data is approved

[Day 4](README.md) · [Lab 06](labs/lab06/WALKTHROUGH.md) · [Silver field contract](../day02/DATA_CONTRACT.md)

## Strict whole-candidate policy

`MASAR_QUALITY_V1` blocks a failed candidate from downstream use. It does not overwrite trusted Silver. The application explicitly isolates bad records; Great Expectations checks assertions and records validation results, not automatic repairs.

A clean subset from a failed candidate is not approved by that failed run. It must become a separately revalidated candidate before a new approved Delta snapshot is written.

## What must hold

Use the 12 business fields defined for Silver and one row per trip. This fixed fixture requires 75 rows, present and unique trip keys, known drivers, supported cities, valid timestamps, positive duration/distance, non-negative fare, valid driver attributes and a positive source revision.

The row policy also checks that duration matches the parsed timestamps and that the local trip date is consistent. Duplicate trip keys are rejected on every occurrence. Schema or volume failure can block the candidate even if many individual rows look valid.

## Seven root defects in the supplied test file

`MISSING_TRIP_ID`: missing trip key.

`INVALID_FARE`: negative fare.

`UNKNOWN_DRIVER`: driver absent from the dimension.

`INVALID_TIMESTAMP`: unparseable start time.

`INVALID_DURATION`: end before start.

`INVALID_DISTANCE`: zero distance.

`INVALID_CITY`: unsupported city.

These are the seven intentional root causes in `quality_cases.csv`, not a universal list of every possible defect. One row can fail several GX expectations. Preserve its root reasons and candidate context rather than counting assertions as rows.

## Three recorded decisions

**Trusted:** 75 corrected rows pass GX and the row policy.

**Mixed:** 82 rows fail; seven are written to quarantine with reasons.

**Rechecked:** the 75-row clean candidate passes a new GX validation and policy evaluation, then is written to Delta and read back.

Approval requires matching the complete original corrected business contents, not only the count or fare total. The saved quality report identifies the new approved table; never fabricate this report as a substitute for validation.

## Bounded execution and safe interpretation

The native wrapper collects a real Delta snapshot of at most 500 trips for GX Pandas validation. It records separate Checkpoint results and Data Docs for the three phases. Additional deterministic policy checks provide quarantine reasons. [[S6–S9](SOURCES.md)]

Do not lower thresholds, fill in an invented driver, edit timestamps or suppress assertions to obtain a pass. Fix the identified cause and validate a new candidate. Monitoring measures and their fixed scenario clock are explained separately in [observability](OBSERVABILITY.md).
