# Day 4 · Event contract

[Day 4](README.md) · [Lab 05](labs/lab05/WALKTHROUGH.md) · [Shared data dictionary](../data/DICTIONARY.md)

## Two keys and two row meanings

**Transport row:** one received Kafka message position, uniquely identified by `(topic, partition, offset)`.

**Business event:** one observation identified by `event_id`.

Raw Bronze preserves intentional repeated observations at new transport positions. Compare event payloads before business deduplication: one event ID with conflicting content is an error, not permission to choose an arbitrary row.

## Payload fields

`event_id`: non-empty string.

`trip_id`: a trip in corrected Silver.

`event_ts`: parseable ISO timestamp with an explicit timezone.

`city`: Riyadh, Jeddah or Dammam.

`location`: finite numeric latitude in [-90, 90] and longitude in [-180, 180].

`synthetic`: exactly true.

The fixed source contract accepts only these payload fields and `lat`/`lon` inside location. The code checks the fixed sources and reconciles received contents against them. Broker headers and ingestion metadata belong to the receipt envelope, not the event payload.

## Unchanged source batches

`gps.ndjson`: 216 messages.

`gps_replay.ndjson`: two already known events.

`gps_late.ndjson`: one new event with an old timestamp.

Total: 219 received messages and 217 distinct events. The producer preserves each original JSON line without changing dates to today. The stream's raw table is separate from the Day 1 GPS table.

## Checkpoint and recovery boundaries

One full lab invocation owns a fresh topic, target and checkpoint. Its four query executions share the checkpoint and target; `query_id` is stable while `query_run_id` changes. Do not share that checkpoint between unrelated queries.

A sending intent is retained before publication; a partial send is not automatically resent. Keep original Kafka topic data and compatible checkpoint/destination together for resume. The handoff ZIP does not contain Kafka broker storage; see [transfer versus recovery](COMPLETION.md). [[S1, S2, S5](SOURCES.md)]

## What the final snapshot represents

After receiving all phases, the code reads raw Delta data as a bounded batch, rejects event-content conflicts and writes a distinct-event Delta snapshot. It preserves the late event and checks every event's trip relationship.

This exercise verifies the supplied sources and a clean restart. It does not test arbitrary production feeds, watermark execution, broker failover or authenticated multi-user access. Use [the local service setup](SETUP.md) and preserve the report paths.
