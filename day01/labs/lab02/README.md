# Lab 02 · Cost and local scan evidence

[Course home](../../../README.md) · [Start here](../../../docs/START_HERE.md) · [Execution record](../../../STATUS.md)

## Contribution and status

Day 1 · LO2, LO8. [Open the combined learner notebook](../../STUDENT.ipynb). The source and native sections belong to this same lab. [Latest execution evidence and tested environment](../../../STATUS.md).

## Concept before code

[Read the detailed concept guide first](../../CONCEPTS.md)

## Exact input files

- [trips.csv](../../../data/masar-small-v1/trips.csv)

Use the successful Bronze workspace from Lab 01. Compare the original CSV with Delta version 0 so both scans contain the same 72 trips.

## Required workflow and checks

- State every assumption and separate hypothetical teaching units from currency.

- Compare always-on and scheduled operation, including overhead and a counterexample.

- Measure actual Spark scans with equal-result checks and query plans.

- Report observed timings without promising a speed-up on a tiny dataset.

## Save in the same project

- `student/BENCHMARKS.md`

- `student/day01/LAB02_NOTES.md`

[Document the evidence](../../../templates/LAB_NOTES.md) — paths above describe learner deliverables, not a claim that generated tables already exist in this source tree.

## Stop, diagnose, preserve

Keep the full error and the last successful step. Do not replace the engine with an unrelated calculation, delete failing checks, or reset unrelated files. Ask through the course support route with a redacted error and version details.

## Detailed implementation now available

[Read the guided lab](WALKTHROUGH.md) · [Open the native notebook section](../../STUDENT.ipynb). Use the daily notebook for the full ordered lab and retain its actual outputs.
