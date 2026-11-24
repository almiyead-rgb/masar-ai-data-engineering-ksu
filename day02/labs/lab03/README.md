# Lab 03 · Staging and incremental Silver

[Course home](../../../README.md) · [Execution record](../../../STATUS.md)

## One cumulative lab

Day 2 · LO3 and LO8 · Parts 3a and 3b. Use the actual Day 1 Delta output to build typed staging and incremental Silver. The dbt models apply the same transformation rules.

- [Read the concepts](../../CONCEPTS.md)

- [Follow the walkthrough](WALKTHROUGH.md)

- [Model design with dbt](../../DBT_GUIDE.md)

- [Executed independent reference](../../REFERENCE.ipynb)

- [Native Lab 3a](../../STUDENT.ipynb)

- [Native Lab 3b](../../STUDENT.ipynb)

- [Completion and handoff](../../COMPLETION.md)

## Inputs and outputs

Reuse the successful `mini_lakehouse/bronze/` workspace. The only new business arrivals today come from the fixed [late_trips.csv](../../../data/masar-small-v1/late_trips.csv). Save staging snapshots, `mini_lakehouse/silver/trips/`, actual scenario evidence and student/day02/LAB03_NOTES.md. These are output paths, not pre-existing tables in the source archive.

## Completion checks

Typed staging; preserved Bronze; unique driver keys; no missing driver references; conflict detection before deduplication; 72 base trips and 75 after late arrival; equal business digests on retries; actual Delta artifacts. The dbt demonstration still requires adapter configuration and real execution before that part is marked complete.

[Silver field contract](../../DATA_CONTRACT.md)
