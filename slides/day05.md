# Day 5: Gold, AI/BI and final delivery

**SDA-DSC-214 · 20 slides · Meaad Al-Marri**

[Daily guide](../day05/README.md) · [Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/STUDENT.ipynb)

## Slide 1: Your project after Day 4

- You have 75 approved trips and 217 distinct events.
- The failed candidate and quarantine remain evidence.
- Today you build and consume the final products.

<details>
<summary>Explanation and references</summary>

Restore your Day 4 handoff in a new session if needed. Day 5 reads the approved Delta snapshots; it does not need the previous Kafka broker to remain alive. The project is already cumulative. The final labs prepare serving outputs, test a release failure and package the evidence you have built.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 2: Day 5 outcomes

- Define each product and its row grain.
- Reconcile BI and select time-appropriate AI inputs.
- Recover a failed candidate and submit a reproducible project.

<details>
<summary>Explanation and references</summary>

LO7 connects the Lakehouse to consumers and LO8 completes the integrated build. Quality controls continue to support LO6. Your deliverable includes both data and meaning: fields, units, keys, source versions and interpretation of null values. No additional unrelated final project is introduced.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 3: A data product has a contract

- State the consumer question.
- Define one row, its key, fields and units.
- Document checks and the selected input snapshots.

<details>
<summary>Explanation and references</summary>

The eight outputs have different purposes. A fact table, a driver-day summary and a feature table should not be judged by whether their raw row counts match. Their contracts explain what each count represents and which measures should reconcile. Read the release manifest instead of guessing a folder path.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 4: Facts, dimensions and grain

- Facts hold measures at a stated business grain.
- Dimensions provide unique keys and descriptions.
- Each fact should join to one intended dimension row.

<details>
<summary>Explanation and references</summary>

The trip fact has one row per trip_id. City, driver and date dimensions provide descriptions. Validate uniqueness before using a dimension in a report. The city field is a city proxy, not a measured neighborhood or service-zone boundary. Make that resolution visible in the contract.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 5: Aggregation changes row meaning

- 75 trip facts can become 18 driver-day groups.
- Sum trip_count to reconcile the population.
- Combine averages through totals and counts.

<details>
<summary>Explanation and references</summary>

A summary row can represent several trips. Comparing 18 groups with 75 trips does not show loss. For combined averages, use the sum of duration divided by the sum of trip count; an unweighted mean of unequal-size group averages can be wrong. Preserve the components needed for correct downstream aggregation.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 6: The GPS join boundary

- A trip can have several location events.
- Count distinct events per trip first.
- Left-join that one count to the trip fact.

<details>
<summary>Explanation and references</summary>

A direct join of raw event rows repeats trip-level fares. The safe path aggregates at the trip key before joining. The three late trips remain even if they have no recorded GPS events; their event count is zero. The final fact's recorded event total is 217, not 219 delivery receipts.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 7: BI reconciliation

- Each city has 25 trips.
- City fares sum to SAR 1,880.60.
- Check group assignments as well as the grand total.

<details>
<summary>Explanation and references</summary>

Riyadh totals 585.00 SAR, Jeddah 625.20 SAR and Dammam 670.40 SAR. Matching only the grand total can hide a value assigned to the wrong city. The supplied SQL executes against a registered fact view after the release is validated. Use the same units and trip-start-date definition when comparing reports.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 8: A feature has a decision time

- Use a stated cutoff and prediction horizon.
- Check when the event happened and when its revision was available.
- Keep future labels separate from model inputs.

<details>
<summary>Explanation and references</summary>

The fixed cutoff is 2026-06-04 at 06:05 Riyadh. The historical window is the prior 24 hours, using completed trips whose source revision was available by that cutoff. The target is the next complete hour,07:00–08:00 Riyadh. These are scenario settings, not the wall-clock date when you run the notebook.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 9: Quick activity: make the decision

- At a decision cutoff, which input is valid: completed trips already available in the past 24 hours, or the actual trip count in the next hour?
- Think: 1 minute. Compare: 2 minutes. Discuss: 2 minutes.

<details>
<summary>Explanation and references</summary>

Use the project terms rather than naming tools without a reason. State your choice and the assumption behind it. The activity is part of the explanation time and has no separate project mark.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/PRACTICE.md)

</details>

---

## Slide 10: Activity answer

- Use the completed trips whose source data was available by the cutoff. The actual future-hour count is a future label, not an input available at prediction time.

<details>
<summary>Explanation and references</summary>

Compare the reasoning as well as the final choice. If you selected another answer, identify which meaning of a row, time boundary or business rule led to it. The project will provide an observable example of this decision.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/PRACTICE.md)

</details>

---

## Slide 11: Historical inputs and unknown labels

- Each city has eight eligible completed trips.
- Feature rows summarize eligible historical data.
- Future targets remain NULL with UNOBSERVED status.

<details>
<summary>Explanation and references</summary>

An unknown future label is not an observed zero. The fixture has no observed target-hour outcomes for supervised model fitting or accuracy measurement. Keep allowed inputs separate from audit fields and labels. The mean historical durations are 1,230, 1,350 and 1,470seconds for Riyadh, Jeddah and Dammam respectively.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 12: The eight products

- Gold: hourly city observations and driver-day summaries.
- BI: trip facts plus city, driver and date dimensions.
- AI: historical features and separate label-status rows.

<details>
<summary>Explanation and references</summary>

Expected row counts are 75, 18, 3, 6, 3, 75, 3 and 3in the documented product order. The hourly demand name means observed trip starts here, not every customer request or measured market demand. The three label-status rows document missing future truth. Product names are path-based manifest entries, not automatically registered SQL tables.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 13: A local release manifest

- Record the selected input versions.
- Write and validate all candidate tables.
- Advance the reader pointer only after successful validation.

<details>
<summary>Explanation and references</summary>

Each Delta table has its own commit. The local release protocol prevents this project reader from selecting a partially built candidate. It is not a single global transaction across eight tables, and it does not coordinate concurrent production publishers. Record the scope accurately when explaining the recovery demonstration.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 14: Controlled failure and recovery

- Build a valid release.
- Fail a new candidate after its first table.
- Keep the valid pointer, then recover and compare content.

<details>
<summary>Explanation and references</summary>

The exercise confirms that an incomplete candidate does not replace the previous selected release. A successful rebuild receives a new identity but should have matching canonical business content. Compare the data contracts and hashes rather than volatile timestamps or directory names. This is a controlled failure, not a machine-crash test.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 15: Export data with its meaning

- Create eight small CSV exports.
- Keep units, keys and null interpretation beside them.
- Preserve Delta state separately for continued work.

<details>
<summary>Explanation and references</summary>

CSV is convenient for inspecting or handing a small result to a consumer, but it does not carry the full Delta schema or transaction history. The writer represents missing values as empty fields. Keep the data-product contract and release manifest with the exports so a consumer does not interpret an empty target as zero.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 16: Your final submission

- Complete student/PROJECT_README.md and link it from your root README.
- Identify the final repository, branch and commit SHA.
- Keep the full state archive available for private review.

<details>
<summary>Explanation and references</summary>

The 100-point rubric rewards working components and explanations. All five attended days and at least 70 project points are required to pass. All five days with no project or below 70 earn attendance-only certification. Include the programme, instructor attribution, SDAIA Academy link and hashtag in your README and submission message. The instructor announces the private submission channel and deadline. The final project write-up lives in student/PROJECT_README.md, alongside your cumulative student evidence.

[Source 1](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema) · [Source 2](https://docs.delta.io/delta-batch/) · [Source 3](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/CONCEPTS.md)

</details>

---

## Slide 17: Your 60-minute lab

- Build the eight products from approved inputs.
- Inspect controlled release failure and recovery.
- Run the BI/AI consumer checks and prepare your final submission.

<details>
<summary>Explanation and references</summary>

Use 45 minutes for the guided execution and checks,5 minutes for your first answer,5 minutes for discussion and 5 minutes for saving. The notebook includes setup and a small student-authored task. Read the walkthrough and inspect the outputs. This work adds to your existing project rather than starting a new assignment.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 18: Compare and save

- Validated products / CSV exports: 8 / 8
- Reconciled trips / fares: 75 / SAR 1,880.60
- Recorded GPS events: 217
- Save the notebook to GitHub and the full handoff to Drive.

<details>
<summary>Explanation and references</summary>

Expected checkpoints: Validated products / CSV exports: 8 / 8. Read each product contract and release manifest. Reconciled trips / fares: 75 / SAR 1,880.60. Aggregated products reconcile to the same trusted trips. Recorded GPS events: 217. Count events by trip before joining them to fare measures. AI feature / label rows: 3 / 3. Feature rows use historical data. Future labels remain NULL with UNOBSERVED status. Save day05/STUDENT.ipynb with your outputs. Upload the extracted small files from outputs/day05_github.zip. Keep outputs/day05_handoff.zip on Drive. Compare business content; run IDs, paths and timings can differ. Complete your student/dayNN lab notes and shared project notes before saving; the bundle includes the student folder.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 19: Your end-of-lab question

- bi.fact_trips has 75 rows, but ai.zone_hourly_features has three. Does that mean 72 trips were lost?
- Record your first answer and observed evidence in student/day05/REFLECTION.md.

<details>
<summary>Explanation and references</summary>

Work from your own run before reading the next slide. State the relevant grain, identity or time boundary. A count, fare, validation field or short query result can support your explanation. This reflection contributes one point to the 100-point project.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 20: Model answer

- No. The products have different grain and time windows. The fact table has one row per trip; features have one row per city, cutoff and prediction horizon, using only eligible historical data.

<details>
<summary>Explanation and references</summary>

Keep your initial answer and add a correction if needed. Explain the difference using a specific observed result from your notebook or report. The model answer is a learning reference, not a substitute for execution evidence.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---
