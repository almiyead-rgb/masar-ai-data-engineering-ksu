# Lab 05 · Follow one event through the pipeline

[Day 4](../../README.md) · [Student notebook](../../STUDENT.ipynb) · [Event contract](../../STREAM_CONTRACT.md)

## 1. Prepare and open your existing workspace

Complete the notebook setup and **Prepare the local Kafka broker**, using [the setup guide](../../SETUP.md). `Continue workspace:` identifies your existing project folder. The streaming cell also verifies the Day 3 report and the corrected 75-trip Silver contents.

Inspect the three GPS source files without editing them: 216 base messages, two repeated events and one new late event. The optional reference notebook is not a prerequisite. The main notebook is your execution route.

## 2. Run the 05 cell once

The second code cell calls `run_stream_lab(spark, SOURCE, WORK)` and executes all four phases below. Do not create separate send commands between cells. Read the shared [streaming.py](../../../src/masar/streaming.py) functions to follow the implementation without copying them.

Each full invocation creates a topic named `masar-day04-<run_id>`, two partitions and a new destination/checkpoint pair. Existing topics are not deleted or reused silently.

## 3. Base: send and consume the original messages

`publish_fixture` records the sending intent before publishing each unchanged JSON line, with `trip_id` as its message key. It stores the acknowledged topic, partition and offset for each send. Producer retry protection does not eliminate deliberate new sends of the same event.

`consume_available` uses Spark's Kafka source and a Delta append sink. It saves `raw_json`, the transport key, message key, headers, broker timestamp and ingestion time. `availableNow=True` drains available input and ends this phase; the configured limit is 72 offsets per trigger. Base counts are **216 transport rows and 216 distinct events**. [[S1–S3, S5](../../SOURCES.md)]

## 4. Restart: resume without sending

The helper starts a new execution of the same query with the same checkpoint and Delta destination, without publishing new messages. Counts remain **216 / 216**. Compare `query_id`, `query_run_id` and `checkpoint`: query identity and checkpoint remain the same; execution identity changes.

The restart occurs inside this one notebook cell. Rerunning the whole cell creates another full experiment. Do not delete the checkpoint or alter starting offsets to force the expected result. This is a clean query-resume test, not a broker crash or failover test. [[S1, S2](../../SOURCES.md)]

## 5. Replay, then receive the late event

The replay file sends two existing observations again. Transport rows increase to **218**, but distinct events remain **216**. The late file then adds the new `SYN_E_LATE001` observation: **219 transport rows and 217 distinct events**.

An old event timestamp does not make that new event a duplicate. The lab keeps it; it does not execute a watermark experiment. The notebook prints:

`Transport rows: [216, 216, 218, 219]`

`Unique event IDs: [216, 216, 216, 217]`

## 6. Reconcile content as well as counts

The 13 checks compare acknowledged transport keys with consumed keys, exact source JSON lines with stored lines, query identities and checkpoint files, and distinct events with the source-derived expected content. They also verify that every event links to a trusted trip.

Conflicting payloads with one `event_id` are rejected before deduplication. After all phases, a batch read of raw Delta data is deduplicated into a new 217-event Delta snapshot. This is not a stateful streaming deduplication operator. Day 1 GPS ingestion is separate; do not combine it with this stream and count the same base events twice.

## 7. Find your evidence and continue

Open `WORK/reports/day04_stream_latest.json`. Its `raw_table` and `event_table` fields are relative to `WORK`. Under `reports/day04/<run_id>/`, retain the three producer receipts, four `consumer_*.json` reports and `streaming.json`. The checkpoint is under `checkpoints/day04/gps_<run_id>/`.

Explain the four phases in `student/day04/LAB05_NOTES.md`. Keep interrupted attempts and their messages; a partial acknowledgment is not proof of complete delivery. Continue to [Lab 06](../lab06/WALKTHROUGH.md), then save using [the daily checklist](../../COMPLETION.md).
