# Lab 04 · Delta corrections and safe maintenance

[Day 3](../../README.md) · **[Run the daily notebook](../../STUDENT.ipynb)** · [Step-by-step guide](WALKTHROUGH.md)

## Two parts, one lab

**04a — Transactions:** correct the existing Silver trip, verify replay and stale-revision handling, read the previous version, and test a rejected write on a constrained copy.

**04b — Maintenance:** use new copies to test one schema change, compaction, deletion and restoration. Preview cleanup candidates without deleting files.

Both parts run inside `day03/STUDENT.ipynb`. Follow the setup, student task, 04a,04b, reflection and save sections in order. Keep one `student/day03/LAB04_NOTES.md`.

## Inputs

Use the completed Day 2 workspace: the 75-trip Delta Silver table, its report, the successful-workspace pointer and the existing Bronze driver data. The shared fixed sources are `correction.csv`, `schema_change.csv` and the negative-fare case in `quality_cases.csv`.

Only the approved correction changes the continuing Silver table. The other scenarios are isolated tests; they do not add faulty rows or a surcharge field to that table.

## Read, apply and explain

[Concepts and examples](../../CONCEPTS.md) · [Change rules](../../CHANGE_POLICY.md) · [Glossary](../../GLOSSARY.md) · [Application](WALKTHROUGH.md) · [Questions](../../PRACTICE.md).

[The calculation reference](../../REFERENCE.ipynb) is optional. Use the daily notebook for actual Spark and Delta execution. The shared functions in [delta_lab.py](../../../src/masar/delta_lab.py) are already called by the notebook; do not duplicate them in a second implementation.

## Complete the stage

Check the corrected 75-trip table, both parts’ reports and the handoff archive using [the completion checklist](../../COMPLETION.md). Keep the notebook’s real outputs and explain the observed change in your notes. [Saved execution evidence](../../verification.json).
