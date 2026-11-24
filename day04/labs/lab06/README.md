# Lab 06 · Validate, quarantine and approve

[Day 4](../../README.md) · **[Student notebook](../../STUDENT.ipynb)** · [Walkthrough](WALKTHROUGH.md)

## Goal and inputs

Protect downstream tables from invalid candidates. Use the corrected Day 3 Silver table: **75 trips and SAR 1,880.60**. The separate `quality_cases.csv` file supplies seven intentional defects; it must not be appended to trusted Silver.

Read [the quality rules](../../QUALITY_POLICY.md). The shared [quality_gate.py](../../../src/masar/quality_gate.py) reads real Delta data and collects a bounded snapshot for GX Pandas validation. The 500-row limit is a classroom boundary, not a distributed-quality benchmark.

## Three separate validations

Run the **06** cell after Lab 05:

`trusted`: 75 rows, pass.

`mixed`: 82 rows, intentional failure; quarantine 7.

`rechecked`: a new 75-row candidate, pass before approval.

GX runs assertions and produces local Data Docs. The application code decides quarantine and approval; GX does not repair or move the rows automatically. The existing Silver table remains unchanged.

## Evidence and completion

Inspect the nine checks, seven quarantined records and `reports/day04_quality_latest.json`. Explain the failed candidate and the newly approved snapshot in `student/day04/LAB06_NOTES.md`; use the [daily reflection and quality questions](../../PRACTICE.md).

Update your existing governance notes using [the guide](../../GOVERNANCE.md), interpret [the monitoring measures](../../OBSERVABILITY.md), then run the notebook's handoff cell and follow [completion](../../COMPLETION.md).
