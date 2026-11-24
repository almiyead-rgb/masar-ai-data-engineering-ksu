# Day 4 · Glossary and pronunciation

[Course home](../README.md) · [Execution record](../STATUS.md)

## How to use

Pronunciation is approximate Arabic support, not a phonetic standard. Each entry gives the English term, explanation and a project example.

### Event

A recorded observation.

**Example:** One synthetic GPS observation.

### Producer

Sends messages to Kafka.

**Example:** publish_fixture sends unchanged JSON.

### Broker

Kafka server storing messages.

**Example:** One local broker in this lab.

### Consumer

Reads messages from a topic.

**Example:** Spark is the lab consumer.

### Topic

Named message channel.

**Example:** A fresh masar-day04 topic per run.

### Partition

Ordered lane inside a topic.

**Example:** Two partitions, not two replicas.

### Offset

Position within one partition.

**Example:** Offset 10 needs topic and partition.

### Message key

Value used for partition selection.

**Example:** trip_id is the message key.

### Acknowledgment

Confirmation of a send under its policy.

**Example:** Store actual producer offsets.

### Idempotence

Retry without repeating an intended effect.

**Example:** Transport idempotence does not deduplicate new sends.

### Checkpoint

Persisted streaming progress.

**Example:** Reuse the same Spark checkpoint for resume.

### Micro-batch

Small bounded increment in a stream.

**Example:** Read up to a configured offset limit per trigger.

### AvailableNow

Trigger that processes currently available input.

**Example:** A classroom stream can finish.

### Event time

Time stated by the observation.

**Example:** event_ts stays in June 2026.

### Processing time

Time the processing engine handles input.

**Example:** ingested_at is captured during execution.

### Late arrival

Input arriving after newer event-time data.

**Example:** The new late event has an old timestamp.

### Watermark

Progress threshold used by supported stateful operations.

**Example:** Not a wall-clock delete rule for Bronze.

### Deduplication

Removing identical repeated business records.

**Example:** 219 deliveries become 217 distinct events.

### Expectation

Testable assertion about data.

**Example:** Fare must not be negative.

### Expectation Suite

Named collection of quality assertions.

**Example:** The Silver suite covers keys and ranges.

### GX Checkpoint

Runner of validations and actions.

**Example:** Different from a Spark checkpoint.

### Quarantine

Isolated rejected rows with reasons.

**Example:** Seven deliberate quality probes.

### Data Docs

GX-generated validation documentation.

**Example:** Actual local HTML after Checkpoint execution.

### Freshness

Age of a stated data timestamp.

**Example:** Arrival age is not event age.

### Observability

Evidence used to understand pipeline behaviour.

**Example:** Progress, counts and quality reports.

### Lineage

Traceable path from source to output.

**Example:** Source hash → offset → Delta snapshot.

### Promotion gate

Decision controlling downstream use.

**Example:** A failed candidate is not promoted.

### Retention

How long data is kept for a purpose.

**Example:** A classroom setting is not a legal retention rule.
