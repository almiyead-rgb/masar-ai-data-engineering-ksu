# Lab 01 · Land and inspect raw feeds

[Course home](../../../README.md) · [Start here](../../../docs/START_HERE.md) · [Execution record](../../../STATUS.md)

## Contribution and status

Day 1 · LO1, LO8. [Open the combined learner notebook](../../STUDENT.ipynb). The source and native sections belong to this same lab. [Latest execution evidence and tested environment](../../../STATUS.md).

## Concept before code

[Read the detailed concept guide first](../../CONCEPTS.md)

## Exact input files

- [trips.csv](../../../data/masar-small-v1/trips.csv)

- [drivers.csv](../../../data/masar-small-v1/drivers.csv)

- [gps.ndjson](../../../data/masar-small-v1/gps.ndjson)

This is the first lab: start from these three fixed raw feeds. No earlier Bronze or Silver tables are required.

## Required workflow and checks

- Read the source manifest and verify file hashes before processing.

- Create real Delta Bronze tables with source and ingestion metadata.

- Replay trips without overwriting history and explain the intended Bronze growth.

- Record at least three quality risks; distinguish observed defects from risks.

## Save in the same project

- `mini_lakehouse/bronze/`

- `student/day01/LAB01_NOTES.md`

[Document the evidence](../../../templates/LAB_NOTES.md) — paths above describe learner deliverables, not a claim that generated tables already exist in this source tree.

## Stop, diagnose, preserve

Keep the full error and the last successful step. Do not replace the engine with an unrelated calculation, delete failing checks, or reset unrelated files. Ask through the course support route with a redacted error and version details.

## Detailed implementation now available

[Read the guided lab](WALKTHROUGH.md) · [Open the native notebook section](../../STUDENT.ipynb). Use the daily notebook for the full ordered lab and retain its actual outputs.
