# Day 1: Architecture and Bronze

**SDA-DSC-214 · 20 slides · Meaad Al-Marri**

[Daily guide](../day01/README.md) · [Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/STUDENT.ipynb)

## Slide 1: Your Masar project

- A fictional transport company needs consistent trip reports.
- Build one Mini-Lakehouse across five evenings.
- Run in Colab and save your work to GitHub each day.

<details>
<summary>Explanation and references</summary>

The same project grows throughout the course. Its source files include trip records, drivers and location events. Repeated arrivals and later corrections will challenge the first results. Each lab adds one engineering capability and leaves evidence for the next day. You will submit the accumulated work on Day 5.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 2: Day 1 outcomes

- Compare architectures for a stated use case.
- Explain storage/compute separation and cost assumptions.
- Preserve raw receipts with source metadata.

<details>
<summary>Explanation and references</summary>

LO1 and LO2 frame the design decisions; LO8 begins with actual Bronze tables. The lab hour includes your first reflection and daily save. For course completion, all five attended days plus a project score of at least 70/100 are required. All five days without a project or below 70 lead to an attendance certificate only.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 3: The business question

- How many trips happened in each city?
- Which fare values are currently approved?
- Can you trace a reported value to its source?

<details>
<summary>Explanation and references</summary>

Start with the decision a consumer needs to make. A daily operational report and a rapid event alert may require different freshness. This project uses small synthetic data to make the engineering behavior inspectable. It does not establish real transport demand or a production service-level requirement.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 4: Warehouse, lake and Lakehouse

- Warehouse: governed analytical tables and query workloads.
- Lake: varied source data retained in open storage.
- Lakehouse: table-management capabilities over lake storage.

<details>
<summary>Explanation and references</summary>

These categories describe architectural emphasis, and actual products overlap. A warehouse can separate storage and compute and support AI workloads. A lakehouse does not automatically make data correct. Compare governance, data variety, consumers, team skills and operational needs for the specific use case.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 5: Choosing the architecture

- List the required inputs and consumers.
- Compare freshness, governance and operational effort.
- Explain why a small Lakehouse fits this exercise.

<details>
<summary>Explanation and references</summary>

For Masar, the educational objective is to combine raw retention, transformations, transactions and reusable outputs in one visible path. A simpler warehouse design may be appropriate for another problem. State one alternative and the condition that would make you choose it; do not present a universal winner.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 6: Compute and storage

- Compute processes queries and transformations.
- Storage preserves data beyond a compute session.
- Independent scaling changes both cost and operations.

<details>
<summary>Explanation and references</summary>

In cloud designs, durable storage can remain while compute capacity stops or changes. Local folders in this lab illustrate responsibilities but do not prove independent cloud scaling. In Colab, a deleted runtime also deletes its local files. Your handoff archive provides the recovery copy required by this teaching environment.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 7: Cost needs assumptions

- Compare equal workloads and the same storage volume.
- Include startup time and scheduling overhead.
- Use hypothetical teaching units, not provider prices.

<details>
<summary>Explanation and references</summary>

The cost exercise holds its storage assumption constant and compares billed compute hours. Its values are hypothetical and do not represent SAR or USD. Increasing work hours can change the conclusion. State the assumptions, the difference with its sign and one case in which the chosen schedule would stop being cheaper.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 8: Bronze, Silver and Gold

- Bronze preserves incoming records and provenance.
- Silver defines trusted business records.
- Gold serves a specific consumer question.

<details>
<summary>Explanation and references</summary>

The layer names describe responsibilities, not certifications. A file in a Gold folder can still be wrong. At each boundary, define the meaning of one row, its key, required fields, expected freshness and the checks that permit promotion. Today you implement the raw boundary; later days add trust and serving.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 9: Quick activity: make the decision

- Place each example in Bronze, Silver or Gold: original trip file; one validated row per trip; city revenue report.
- Think: 1 minute. Compare: 2 minutes. Discuss: 2 minutes.

<details>
<summary>Explanation and references</summary>

Use the project terms rather than naming tools without a reason. State your choice and the assumption behind it. The activity is part of the explanation time and has no separate project mark.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/PRACTICE.md)

</details>

---

## Slide 10: Activity answer

- Original trip file: Bronze. Validated trip table: Silver. City revenue report: Gold.

<details>
<summary>Explanation and references</summary>

Compare the reasoning as well as the final choice. If you selected another answer, identify which meaning of a row, time boundary or business rule led to it. The project will provide an observable example of this decision.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/PRACTICE.md)

</details>

---

## Slide 11: Three source grains

- Trip: one journey identified by trip_id.
- Driver: one synthetic driver identified by driver_id.
- Location event: one observation identified by event_id.

<details>
<summary>Explanation and references</summary>

The starting fixture has 72 trips, 6drivers and 216 GPS events. Each base trip has three events. Counting after a one-to-many join changes the unit of a row. Before calculating fares, ask whether you still have one row per trip. The field dictionary and source manifest define the exact training inputs.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 12: Receipt identity and trip identity

- A delivery records that data arrived.
- A trip_id identifies the business journey.
- Repeated delivery can increase Bronze without adding trips.

<details>
<summary>Explanation and references</summary>

Appending 72 trips again creates 144 receipt rows with 72 distinct business keys. Preserve that history so you can investigate arrivals. Do not drop a repeated row without examining whether it is identical, a later revision or a conflicting value. The distinction becomes a Silver rule on Day 2.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 13: Provenance at ingestion

- Keep the source filename and checksum.
- Record the batch ID and ingestion time.
- Keep the original values available for investigation.

<details>
<summary>Explanation and references</summary>

The Bronze implementation adds _source_file, _source_sha256, _batch_id and _ingested_at. A checksum helps identify the input content, while a batch ID identifies the ingestion attempt. Ingestion time differs from when the trip began. Read the metadata for one chosen synthetic trip in both deliveries.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 14: Spark and Delta

- Spark performs the computation.
- Delta manages table state and transactions.
- Business validity still needs explicit rules.

<details>
<summary>Explanation and references</summary>

The pipeline writes real Delta tables and reads their committed state. A CSV calculation or a plain Parquet file is not equivalent evidence. ACID protects transaction behavior; it does not define whether a fare is acceptable for your business. You will enforce those rules and test rejected writes on Day 3.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 15: A fair local scan comparison

- Compare 72 CSV rows with the matching 72-row Delta snapshot.
- Execute the work and reconcile results.
- Record timings as observations on this small sample.

<details>
<summary>Explanation and references</summary>

Do not compare the repeated 144-row Bronze table with the 72-row source and call it a fair scan test. The supplied experiment selects equal populations and checks logical results. Initialization, caching and sample size affect timing. A local observation cannot support a claim that one format is universally faster.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 16: Reading your first result

- The input manifest establishes the file release.
- The Delta output establishes table execution.
- Your explanation connects the evidence to the decision.

<details>
<summary>Explanation and references</summary>

Inspect both the source check and the generated Bronze report. They answer different questions. The source check establishes the input; the table report establishes what the engine wrote. Record one observed risk, such as a city-label variant, and distinguish it from a hypothetical future problem. Keep source files unchanged.

[Source 1](https://docs.databricks.com/aws/en/lakehouse/medallion) · [Source 2](https://docs.snowflake.com/en/user-guide/intro-key-concepts) · [Source 3](https://docs.delta.io/quick-start/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/CONCEPTS.md)

</details>

---

## Slide 17: Your 60-minute lab

- Inspect the source manifest and build Bronze.
- Run the receipt replay and matched scan/cost exercises.
- Record one architecture decision and compare your counts.

<details>
<summary>Explanation and references</summary>

Use 45 minutes for the guided execution and checks,5 minutes for your first answer,5 minutes for discussion and 5 minutes for saving. The notebook includes setup and a small student-authored task. Read the walkthrough and inspect the outputs. This work adds to your existing project rather than starting a new assignment.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 18: Compare and save

- Trip receipts after redelivery: 144
- Unique trip IDs: 72
- Drivers / GPS events: 6 / 216
- Save the notebook to GitHub and the full handoff to Drive.

<details>
<summary>Explanation and references</summary>

Expected checkpoints: Trip receipts after redelivery: 144. Two deliveries of the same 72-trip source. Unique trip IDs: 72. A business trip is different from a delivery receipt. Drivers / GPS events: 6 / 216. These inputs are not redelivered in this scenario. Save day01/STUDENT.ipynb with your outputs. Upload the extracted small files from outputs/day01_github.zip. Keep outputs/day01_handoff.zip on Drive. Compare business content; run IDs, paths and timings can differ. Complete your student/dayNN lab notes and shared project notes before saving; the bundle includes the student folder.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 19: Your end-of-lab question

- Bronze contains 144 trip receipts but only 72 distinct trip IDs. How many business trips have you observed, and why keep the receipts?
- Record your first answer and observed evidence in student/day01/REFLECTION.md.

<details>
<summary>Explanation and references</summary>

Work from your own run before reading the next slide. State the relevant grain, identity or time boundary. A count, fare, validation field or short query result can support your explanation. This reflection contributes one point to the 100-point project.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 20: Model answer

- You observed 72 distinct trips delivered twice. Preserve the 144 receipt records and their source metadata so you can explain arrivals. Silver will select the business record for each trip.

<details>
<summary>Explanation and references</summary>

Keep your initial answer and add a correction if needed. Explain the difference using a specific observed result from your notebook or report. The model answer is a learning reference, not a substitute for execution evidence.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---
