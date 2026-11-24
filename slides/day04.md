# Day 4: Streaming, quality and governance

**SDA-DSC-214 · 20 slides · Meaad Al-Marri**

[Daily guide](../day04/README.md) · [Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/STUDENT.ipynb)

## Slide 1: Your project after Day 3

- Silver has 75 corrected trips and SAR 1,880.60.
- Today you receive location events through Kafka.
- A quality gate controls which candidate can move forward.

<details>
<summary>Explanation and references</summary>

Restore the Day 3 handoff in a fresh Colab runtime. Keep the approved trip table separate from the contaminated quality candidate. The event path uses the synthetic GPS messages through an actual broker and Spark source. By the end, Day 5 will receive approved trip and distinct-event Delta snapshots.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 2: Day 4 outcomes

- Trace a message from producer to Delta.
- Explain checkpoint restart and business event identity.
- Validate, quarantine, monitor and document governance.

<details>
<summary>Explanation and references</summary>

LO5 covers event ingestion, LO6 covers quality, observability and governance, and LO8 continues the project. You need evidence at the producer, broker/offset and output boundaries. The intentionally failed quality candidate is part of the correct experiment; your job is to show that it cannot replace approved data.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 3: Producer, broker and consumer

- The producer sends a message.
- Kafka stores records in a topic.
- Spark consumes records and writes Delta.

<details>
<summary>Explanation and references</summary>

A source NDJSON file makes the messages repeatable but is not a substitute for Kafka. The notebook uses a real producer and broker. A successful socket connection alone does not establish delivery. Inspect producer acknowledgments, consumer offsets and the resulting table records to connect the stages.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 4: Topics, partitions and offsets

- A topic groups event records.
- A partition provides an ordered sequence.
- An offset identifies a record within its partition.

<details>
<summary>Explanation and references</summary>

The lab uses two partitions and a trip-based message key. Ordering within a partition is not a total order across all topic records. Two partitions are not two replicas. This local one-broker experiment illustrates ingestion behavior without claiming multi-broker resilience.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 5: Streaming in a bounded lab

- AvailableNow processes the currently available input.
- Micro-batches commit results to the sink.
- The query can stop after the available work finishes.

<details>
<summary>Explanation and references</summary>

A bounded trigger lets you exercise a real streaming source in a classroom time window. It does not turn the broker into a file reader or simulate consumer results. The query uses the matching Spark Kafka connector and records progress. Inspect what the trigger consumed before proceeding to the next scenario.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 6: A checkpoint records progress

- Keep the compatible source, destination and checkpoint.
- Restarting the query can continue from recorded offsets.
- A deleted broker is a different recovery problem.

<details>
<summary>Explanation and references</summary>

Inside the same session, the experiment stops and restarts a compatible query while the source topic remains. Reusing a checkpoint after replacing the topic with an empty new one is not the same test. A fresh Colab VM requires a new Day 4 experiment from the Day 3 handoff, not a fabricated successful resume.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 7: Transport identity and event identity

- Transport: topic, partition and offset.
- Business: event_id and its approved payload.
- Repeated delivery does not always mean a new observation.

<details>
<summary>Explanation and references</summary>

Two separately sent records can have different offsets while carrying the same event. Producer idempotence handles a particular retry boundary; it does not remove every deliberate repeated send. The application must also inspect duplicate event IDs and reject conflicting content rather than silently selecting one version.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 8: Event time and arrival time

- event_ts describes when the observation happened.
- Ingestion metadata describes pipeline receipt.
- Late and invalid are separate conditions.

<details>
<summary>Explanation and references</summary>

An older timestamp with a new event ID can be valid late data. Missing IDs, impossible coordinates or unknown trips are different defects. State which clock a freshness measure uses. The supplied exercise materializes distinct events from a completed raw snapshot; it does not demonstrate a watermark-based state eviction policy.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 9: Quick activity: make the decision

- Two Kafka messages have different offsets but the same event_id and identical payloads. How many deliveries and business events do they represent?
- Think: 1 minute. Compare: 2 minutes. Discuss: 2 minutes.

<details>
<summary>Explanation and references</summary>

Use the project terms rather than naming tools without a reason. State your choice and the assumption behind it. The activity is part of the explanation time and has no separate project mark.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/PRACTICE.md)

</details>

---

## Slide 10: Activity answer

- They represent two deliveries and one distinct business event. Transport offsets identify records in a partition; event_id identifies the business event.

<details>
<summary>Explanation and references</summary>

Compare the reasoning as well as the final choice. If you selected another answer, identify which meaning of a row, time boundary or business rule led to it. The project will provide an observable example of this decision.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/PRACTICE.md)

</details>

---

## Slide 11: Four streaming phases

- Base and clean restart: 216 receipts, 216 events.
- Two replayed messages: 218 receipts, 216 events.
- One late new event: 219 receipts, 217 events.

<details>
<summary>Explanation and references</summary>

Query identity persists during the compatible restart while the execution identity changes. The two explicit replayed messages become new transport positions but not new observations. The late event adds a new ID. Keep the original Day 1 GPS table and Day 4 stream receipt table separate so they are not accidentally counted together.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 12: A quality contract

- Check required fields, keys and relationships.
- Check values using the correct units and bounds.
- Check whole-candidate completeness as well as individual rows.

<details>
<summary>Explanation and references</summary>

A schema-correct snapshot can still have missing trips, duplicates or invalid values. Sixty individually valid rows would be incomplete for the 75-trip fixture. The quality policy defines both row rules and candidate-level checks. A fixed teaching threshold is not an automatically valid production SLA.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 13: Great Expectations in the project

- Expectations express testable assertions.
- A Suite groups expectations.
- A GX Checkpoint runs validations and actions.

<details>
<summary>Explanation and references</summary>

A GX Checkpoint is different from Spark's streaming checkpoint. The exercise validates a bounded Pandas snapshot collected from actual Delta data, then retains validation results and Data Docs. Great Expectations does not automatically repair values or quarantine rows; the surrounding application performs those actions using explicit reasons.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 14: Reject, quarantine, revalidate

- Reject the 82-row mixed candidate.
- Quarantine seven defective rows with reasons.
- Validate a new 75-row candidate before approval.

<details>
<summary>Explanation and references</summary>

The safe response to a failed whole-candidate check is to block its promotion. After separating invalid rows, run the quality rules again on the clean candidate. Do not assume that removing seven rows is enough. Preserve the original approved table and show which new candidate became eligible for downstream use.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 15: Operational observations

- Volume: did you receive the expected population?
- Freshness: which clock and reference time are compared?
- Run health: where did processing succeed or stop?

<details>
<summary>Explanation and references</summary>

A run can be technically successful while serving stale or incomplete data. The exercise uses fixed scenario times so the comparison remains reproducible. Distinguish old event time from recent delivery time. Record the measured value, its denominator or baseline, and the action the threshold would trigger.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 16: Governance decisions you can explain

- Purpose and owner: why the product exists and who decides.
- Lineage and access: where values came from and who may use them.
- Retention: what you keep, where and for how long.

<details>
<summary>Explanation and references</summary>

Use synthetic data only. In GOVERNANCE.md, separate implemented technical checks from proposed organizational controls. A folder label is not an authorization mechanism, and a local lab pass is not a compliance certification. Keep public source/evidence separate from private attendance, identity and grading records.

[Source 1](https://kafka.apache.org/40/getting-started/quickstart/) · [Source 2](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html) · [Source 3](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/CONCEPTS.md)

</details>

---

## Slide 17: Your 60-minute lab

- Start local Kafka and run the four event phases.
- Run the GX gate, quarantine and revalidation.
- Record one monitoring observation and governance decision.

<details>
<summary>Explanation and references</summary>

Use 45 minutes for the guided execution and checks,5 minutes for your first answer,5 minutes for discussion and 5 minutes for saving. The notebook includes setup and a small student-authored task. Read the walkthrough and inspect the outputs. This work adds to your existing project rather than starting a new assignment.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 18: Compare and save

- Received message records: 219
- Distinct events: 217
- Quality candidate: 82 → rejected
- Save the notebook to GitHub and the full handoff to Drive.

<details>
<summary>Explanation and references</summary>

Expected checkpoints: Received message records: 219. The experiment includes two replayed messages and one new late event. Distinct events: 217. The two identical replayed event IDs do not become new business events. Quality candidate: 82 → rejected. The candidate combines 75 trusted rows with seven deliberately defective rows. Quarantine / revalidated: 7 / 75. Record rejection reasons, then test a new clean candidate before approval. Save day04/STUDENT.ipynb with your outputs. Upload the extracted small files from outputs/day04_github.zip. Keep outputs/day04_handoff.zip on Drive. Compare business content; run IDs, paths and timings can differ. Complete your student/dayNN lab notes and shared project notes before saving; the bundle includes the student folder.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 19: Your end-of-lab question

- A candidate contains 82 rows and fails because seven are invalid. How can you safely use the other 75?
- Record your first answer and observed evidence in student/day04/REFLECTION.md.

<details>
<summary>Explanation and references</summary>

Work from your own run before reading the next slide. State the relevant grain, identity or time boundary. A count, fare, validation field or short query result can support your explanation. This reflection contributes one point to the 100-point project.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 20: Model answer

- Block the failed candidate, quarantine the seven rows with reasons, create a clean 75-row candidate, and run the quality gate again before approving it.

<details>
<summary>Explanation and references</summary>

Keep your initial answer and add a correction if needed. Explain the difference using a specific observed result from your notebook or report. The model answer is a learning reference, not a substitute for execution evidence.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---
