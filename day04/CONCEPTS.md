# Day 4 · Understand streaming and quality

[Day 4](README.md) · [Student notebook](STUDENT.ipynb) · [Glossary](GLOSSARY.md) · [References S1–S14](SOURCES.md)

## Connect each idea to an observed result

Follow one event from its original JSON line to the 217-event snapshot, then follow one invalid trip to quarantine. Use [Lab 05](labs/lab05/WALKTHROUGH.md) and [Lab 06](labs/lab06/WALKTHROUGH.md) for the steps and report paths. The existing 75 corrected trips remain the project's trusted starting point.

## 1. Streaming can have a bounded exercise

An event records an observation, such as one synthetic location reading. The source file supplies repeatable messages to a real producer; it is not a broker. Spark's `availableNow` trigger processes available input in micro-batches and terminates, so the classroom run can finish. [S1, S2]

## 2. Producer, broker and consumer have different jobs

The Python producer sends; Kafka stores; Spark consumes and writes Delta. Check all three boundaries: an acknowledgment, consumed offsets and committed output. A listening port proves none of these business results. [S1, S3, S5]

## 3. A partition is an ordered lane

The lab topic has two partitions and uses `trip_id` as the message key. This routes one trip consistently while the partition configuration and partitioner remain unchanged. Order within a partition does not imply a single order across the topic. Two partitions are not two replicas. [S5, S13]

## 4. Keep two identities

`(topic, partition, offset)` identifies a transport position. `event_id` identifies a business observation. Replaying two existing events creates two new transport positions without creating two new observations. That is why 218 deliveries can represent 216 events. [S1; Masar event contract]

## 5. Retry protection is not business deduplication

The producer enables idempotence and requests acknowledgments for transport retries. A deliberate new `send` is still a new send. Business duplicates and conflicts need their own policy. With one broker and replication factor one, `acks='all'` does not create multi-broker resilience. [S5, S13]

## 6. Bronze preserves receipt evidence

Keep `raw_json` and transport metadata. The Day 4 stream has a separate path from Day 1's GPS ingestion. Combining both blindly would double-count the base observations. Read the selected event snapshot for downstream work, not every raw delivery.

## 7. A checkpoint stores query progress

Reuse the same compatible query, checkpoint, source and destination to resume. `startingOffsets` initializes a new query; it does not reset an existing checkpoint. The broker's topic data and Spark's checkpoint are different storage objects. [S1, S2]

## 8. Explain the clean restart result

Restart without sending leaves 216 transport rows. Query identity stays the same; execution identity changes. This test happens inside the streaming cell. Re-executing the whole cell starts a new experiment. These checks do not demonstrate broker failover, crash stress or uninterrupted service during every failure. [S2; lab checks]

## 9. Name the timestamp you measure

`event_ts` belongs to the observation. `broker_timestamp` is Kafka metadata whose meaning depends on timestamp policy. `ingested_at` records processing into Bronze. Do not call all three event time or compare them with an unstated reference clock. [S1]

## 10. Late is different from invalid

The supplied late event has an older timestamp and a new ID. It adds one observation. Invalid coordinates, a missing key and an unknown trip are different defects. Keep the timing decision separate from field-validity checks. See [the event contract](STREAM_CONTRACT.md).

## 11. Do not invent a watermark experiment

Watermarks help bound state for supported event-time operations; they are not a universal wall-clock deletion rule. This lab does not apply a watermark. It preserves raw messages, rejects conflicting event contents, then batch-deduplicates the completed raw snapshot. Retaining the late event therefore does not demonstrate watermark behavior. [S2]

## 12. Define quality before approval

State the row grain, required fields, keys, ranges and relationships. The trip snapshot needs one row per trip, positive distance and duration, non-negative fare and a known driver. Schema correctness alone does not prove those business rules. Use [the explicit quality policy](QUALITY_POLICY.md).

## 13. Distinguish the two Checkpoints

An Expectation is a testable assertion; a Suite groups assertions; a GX Checkpoint runs validations and actions. It is not Spark's stored streaming progress. Here GX runs on a bounded Pandas snapshot collected from real Delta data and writes local Data Docs. [S6–S9]

## 14. Reject, quarantine and revalidate

The mixed candidate contains 82 rows. Its whole-candidate check fails, and the application quarantines seven defective records with reasons. The remaining 75 rows must pass a fresh validation as a new candidate before approval. GX does not automatically repair rows or move them into quarantine.

## 15. Count validity is not row validity

Sixty individually valid trips are still incomplete for this 75-trip fixture. Check volume, schema, freshness and distribution as different signals. The teaching constants are not a production service-level agreement. [Monitoring](OBSERVABILITY.md) identifies each clock, denominator and baseline.

## 16. Reconcile observed output

In the saved native notebook, transport counts are 216, 216, 218 and 219; distinct-event counts are 216, 216, 216 and 217. The quality result reconciles `82 = 75 + 7`; approved fares remain SAR 1,880.60. Compare your run with its own reports, not with an invented success flag. [Saved execution evidence](verification.json).

## 17. Governance makes decisions traceable

Document the purpose, responsible roles, source-to-output lineage, permitted use and retention decision. A folder named restricted is not authorization. The local broker binds to loopback but does not implement multi-user access control or TLS. Use [the governance guide](GOVERNANCE.md) to separate implemented controls from design proposals.

## 18. Keep the privacy boundary clear

Use only the supplied synthetic fixtures; do not import real GPS traces, customer trips or identifiers. A synthetic flag does not anonymize real input. For a real deployment, consult the relevant organization's privacy and access rules and the official SDAIA references. A local lab pass is not a legal-compliance assessment. [S10–S12]
