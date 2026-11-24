# Day 2: ELT and trusted Silver

**SDA-DSC-214 · 20 slides · Meaad Al-Marri**

[Daily guide](../day02/README.md) · [Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/STUDENT.ipynb)

## Slide 1: Your project after Day 1

- Bronze preserves 144 trip receipts for 72 trip IDs.
- Drivers and location events have their own grains.
- Today you create trusted Silver and dbt evidence.

<details>
<summary>Explanation and references</summary>

Restore your own Day 1 handoff if Colab has started a new runtime. Confirm that the pointer and the actual Delta folders both exist. The project continues from the same source release. Typing fields is the first transformation; it does not itself remove duplicate receipts.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 2: Day 2 outcomes

- Design the Bronze-to-Silver ELT path.
- Handle keys, relationships, replays and late arrivals.
- Run and explain dbt models and tests.

<details>
<summary>Explanation and references</summary>

LO3 is the main objective, with Delta practice supporting LO4 and the cumulative build supporting LO8. By the end, your trusted table should contain 75 trips and 1,875.60 SAR. You will prove the replay behavior and retain separate dbt evidence rather than assuming that a Python transformation proves dbt ran.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 3: ETL and ELT

- Extract obtains the source data.
- Load preserves it in a destination.
- Transform applies structure and business meaning.

<details>
<summary>Explanation and references</summary>

Masar uses ELT by keeping raw records in Bronze before applying Spark transformations. ETL can still be appropriate when the destination must never receive a prohibited field or needs a transformed input. The order follows the requirements. ELT does not mean that every available field should be collected or retained forever.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 4: The Silver contract

- One row represents one trip_id.
- Fares use decimal values and durations use seconds.
- Every trip must have a valid driver relationship.

<details>
<summary>Explanation and references</summary>

Read DATA_CONTRACT.md before changing code. A schema gives a field a type, while the contract also defines its meaning, unit and valid relationship. Zero fares are allowed by this fixture; negative fares are not. Distances and durations must be positive. A missing driver key requires investigation before enrichment.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 5: Staging translates the fields

- Parse timestamps and retain their intended timezone meaning.
- Normalize known city labels.
- Check casts and required values before choosing a record.

<details>
<summary>Explanation and references</summary>

The source contains known label variants such as surrounding spaces and lower-case letters. Normalize them in staging while retaining raw Bronze. A failed cast can become a missing value, so test the result. Canonical timestamps use UTC while business dates follow the trip start in Asia/Riyadh.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 6: Joins can change the result

- A duplicate driver key can multiply trip rows.
- A missing driver can remove or leave an unmatched trip.
- Check keys and relationships before using the join.

<details>
<summary>Explanation and references</summary>

Do not assume that a join preserves the left-hand count. First establish uniqueness in the driver table and identify missing relationships. A valid many-to-one trip-to-driver join preserves the trip-grain population. Use count and key checks before and after enrichment, then inspect representative business values.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 7: Duplicates and conflicts

- Identical receipts can map to one business record.
- A later revision can represent an approved change.
- Equal revisions with different values need investigation.

<details>
<summary>Explanation and references</summary>

Blindly dropping duplicates by trip_id can select the wrong fare. The current Day 2 inputs have identical replayed values; Day 3 introduces correction precedence. Explain the chosen ordering and check for conflicts before merging. A deterministic choice is valuable only when its business rule is correct.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 8: Late arrival and event date

- Occurrence time describes when a trip happened.
- Arrival time describes when the pipeline received it.
- Reports and incremental filters can need different clocks.

<details>
<summary>Explanation and references</summary>

Three June 1 trips arrive in the fixed scenario on June 4. The trip-date report should assign them to June 1. An incremental arrival filter must still include them. Filtering only trips whose business date equals today would miss historical late data and may return nothing for this fixed dataset.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 9: Quick activity: make the decision

- Choose the trip business key: driver_id, trip date or trip_id. Explain one collision the wrong key would create.
- Think: 1 minute. Compare: 2 minutes. Discuss: 2 minutes.

<details>
<summary>Explanation and references</summary>

Use the project terms rather than naming tools without a reason. State your choice and the assumption behind it. The activity is part of the explanation time and has no separate project mark.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/PRACTICE.md)

</details>

---

## Slide 10: Activity answer

- Use trip_id. A driver can complete many trips and a date can contain many trips, so neither uniquely identifies a trip.

<details>
<summary>Explanation and references</summary>

Compare the reasoning as well as the final choice. If you selected another answer, identify which meaning of a row, time boundary or business rule led to it. The project will provide an observable example of this decision.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/PRACTICE.md)

</details>

---

## Slide 11: Idempotent business processing

- Rerunning the same logical input preserves the result.
- New delivery receipts can exist without new trips.
- Compare business content, not only a row count.

<details>
<summary>Explanation and references</summary>

The Silver exercise checks the base, transform rerun, late batch, same-batch retry and new late redelivery. Counts alone can hide changed fares or swapped city assignments. Inspect the checked business fields and the totals together. A new delivery can grow Bronze while Silver stays at the same 75 keys.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 12: The five Silver scenarios

- Base and transform rerun: 72 trips, SAR 1,794.60.
- Late batch: 75 trips, SAR 1,875.60.
- Retries and redelivery: still 75 trips.

<details>
<summary>Explanation and references</summary>

The receipt counts progress 144, 144, 147, 147, 150. The same committed batch retry does not add receipts; a new delivery ID records another arrival. Both routes must preserve the 75 business trips after the late batch. Record what changed at each layer and why those changes differ.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 13: dbt models and dependencies

- A model expresses a transformation.
- source() refers to a declared existing source.
- ref() connects one model to another.

```sql
{{ source('bronze', 'trips') }}
{{ ref('stg_trips') }}
```

<details>
<summary>Explanation and references</summary>

The actual dbt exercise uses six models and three source tables. source() does not ingest a CSV by itself; the runner prepares the relations first. ref() allows dbt to establish dependencies and resolve relation names. Follow one field from staging through the Silver model into the city-day mart.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 14: dbt tests and freshness

- Test keys, missing values and relationships.
- Reconcile marts with their input population.
- Measure freshness using a named arrival clock.

<details>
<summary>Explanation and references</summary>

The supplied project contains generic tests and seven SQL tests. Source freshness is a separate operation from a build. The exercise uses ingestion time and a fixed scenario clock, with documented warning and error thresholds. A test checks a stated condition; a pass does not prove that every possible business rule was examined.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 15: Incremental lookback

- The course uses a three-day ingestion lookback.
- The business key still controls the MERGE result.
- Older corrections can require deliberate reprocessing.

<details>
<summary>Explanation and references</summary>

An incremental filter reduces the scanned source, while the key and merge behavior control duplicate effects. These are different responsibilities. A bounded lookback can miss a change arriving outside its policy window. The supplied optional all-history reprocessing path makes that limitation explicit rather than hiding it.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 16: Separate the two implementations

- PySpark creates the continuing Silver table.
- dbt demonstrates the same principles in an isolated workspace.
- Retain real dbt results for assessment.

<details>
<summary>Explanation and references</summary>

The dbt runner uses copies of the original Bronze snapshots and does not replace the corrected main project state. It runs within its documented Spark-session context. Starting an unrelated dbt process can lose the in-memory source catalog. Inspect the actual base/rerun/late/late_replay reports and preserve the generated documentation.

[Source 1](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.getdbt.com/docs/build/incremental-models) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/CONCEPTS.md)

</details>

---

## Slide 17: Your 60-minute lab

- Prepare staging and check types, keys and relationships.
- Run base, rerun, late and redelivery scenarios.
- Run the real dbt models and inspect their tests.

<details>
<summary>Explanation and references</summary>

Use 45 minutes for the guided execution and checks,5 minutes for your first answer,5 minutes for discussion and 5 minutes for saving. The notebook includes setup and a small student-authored task. Read the walkthrough and inspect the outputs. This work adds to your existing project rather than starting a new assignment.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 18: Compare and save

- Silver trips: 75
- Total fares: SAR 1,875.60
- Final Bronze receipts: 150
- Save the notebook to GitHub and the full handoff to Drive.

<details>
<summary>Explanation and references</summary>

Expected checkpoints: Silver trips: 75. 72 base trips plus three late trips; replay adds no business trips. Total fares: SAR 1,875.60. SAR 1,794.60 plus SAR 81.00 of late-trip fares. Final Bronze receipts: 150. Receipts record the original deliveries and the late-batch redelivery. dbt phase counts: 72, 72, 75, 75. Base, rerun, late and late_replay. Save day02/STUDENT.ipynb with your outputs. Upload the extracted small files from outputs/day02_github.zip. Keep outputs/day02_handoff.zip on Drive. Compare business content; run IDs, paths and timings can differ. Complete your student/dayNN lab notes and shared project notes before saving; the bundle includes the student folder.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 19: Your end-of-lab question

- Silver has 75 trips after three late trips arrive. Will replaying that same late data increase the result to 78?
- Record your first answer and observed evidence in student/day02/REFLECTION.md.

<details>
<summary>Explanation and references</summary>

Work from your own run before reading the next slide. State the relevant grain, identity or time boundary. A count, fare, validation field or short query result can support your explanation. This reflection contributes one point to the 100-point project.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 20: Model answer

- No. Silver stays at 75 because the replay carries the same trip IDs and identical business values. Receipt counts may increase for a new delivery; the business count must not.

<details>
<summary>Explanation and references</summary>

Keep your initial answer and add a correction if needed. Explain the difference using a specific observed result from your notebook or report. The model answer is a learning reference, not a substitute for execution evidence.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---
