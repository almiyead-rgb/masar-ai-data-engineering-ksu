# Lab 05 · Receive and reconcile events

[Day 4](../../README.md) · **[Student notebook](../../STUDENT.ipynb)** · [Walkthrough](WALKTHROUGH.md)

## Goal and inputs

Trace real Kafka messages into a Delta table and explain delivery identity versus event identity. Start the broker using [setup](../../SETUP.md), and retain the successful Day 3 table and reports.

Use the three unchanged shared files: `gps.ndjson` (216 messages), `gps_replay.ndjson` (2 repeated events), and `gps_late.ndjson` (1 new late event). The [event contract](../../STREAM_CONTRACT.md) defines their fields.

## One notebook cell, four observed phases

After setup, run the **05** cell. The shared [streaming.py](../../../src/masar/streaming.py) code performs base ingestion, clean restart, deliberate replay and late arrival in order.

Transport rows: **216, 216, 218, 219**.

Distinct events: **216, 216, 216, 217**.

The checkpoint and destination remain the same within those four phases. Running the entire cell again creates a fresh topic and checkpoint; it is not the same restart test.

## Evidence and next step

Inspect the 13 checks, event preview and `reports/day04_stream_latest.json` under `WORK`. Retain the producer receipts, four consumer reports, checkpoint files and 217-event Delta snapshot.

Record the four message/event counts and explain checkpoint restart in `student/day04/LAB05_NOTES.md`. Use the [daily practice page](../../PRACTICE.md) to test your reasoning. Then continue to [Lab 06](../lab06/README.md) in the same daily notebook. There is no separate project or required reference notebook.
