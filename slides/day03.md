# Day 3: Delta reliability and corrections

**SDA-DSC-214 · 20 slides · Meaad Al-Marri**

[Daily guide](../day03/README.md) · [Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/STUDENT.ipynb)

## Slide 1: Your project after Day 2

- Silver has 75 trips and SAR 1,875.60 in fares.
- Late-trip replays leave business content unchanged.
- Today you apply a correction and inspect table history.

<details>
<summary>Explanation and references</summary>

Continue from the Day 2 state, retaining its separate dbt evidence. Do not rerun Day 2 over a table already corrected on Day 3. The main correction affects one known trip. Experiments involving a surcharge, deletion or compaction use independent training copies so that the next day receives the approved trip table.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 2: Day 3 outcomes

- Explain a committed and a rejected Delta write.
- Apply a source-revision-aware correction.
- Read history and recover an isolated training copy.

<details>
<summary>Explanation and references</summary>

LO4 is the main outcome. You will connect transaction behavior to actual data and reports, supporting the quality controls in LO6 and the integrated build in LO8. Your evidence must show the value before and after correction, the unchanged result on replay and what happened when an invalid write was rejected.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 3: ACID at a table boundary

- Atomicity: the transaction commits as a whole or does not.
- Consistency and isolation operate with defined table rules.
- Durability depends on the storage environment.

<details>
<summary>Explanation and references</summary>

The lab observes committed writes and an intentionally rejected transaction while the local storage is available. ACID does not certify every business value or protect a deleted Colab VM. Separate the behavior of a Delta table from the durability of the machine hosting its files. The backup archive addresses the temporary runtime boundary.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 4: Two different versions

- source_revision orders approved business messages.
- A Delta version identifies a table commit.
- A commit can affect many business records.

<details>
<summary>Explanation and references</summary>

Do not use a table version as the revision of a trip. Source revision 2 means the upstream correction outranks revision 1 for that key. Delta version numbers describe transactions in the target table and can vary with valid rerun histories. Record both when explaining the correction and its audit trail.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 5: Schema enforcement

- The table expects named fields and data types.
- An incompatible write should stop.
- An approved schema change is a separate decision.

<details>
<summary>Explanation and references</summary>

A schema contract makes shape assumptions visible. It does not replace range, relationship or semantic checks. The exercise first shows enforcement, then demonstrates a controlled schema evolution on a sandbox. Keeping evolution deliberate prevents an accidental field change from silently becoming part of the serving contract.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 6: Constraints protect writes

- Use required-field and value constraints where appropriate.
- A negative fare violates this trip contract.
- Inspect the table again after rejection.

<details>
<summary>Explanation and references</summary>

A robust failure test checks more than an exception. Record the attempted invalid write, then reread the table and confirm its previous content remains intact. Zero fares are permitted here, so a non-negative rule is different from a strictly positive rule. Distance and duration follow their own positive-value contracts.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 7: MERGE needs an unambiguous source

- Match one candidate to each trip_id.
- Check conflicts before the update.
- Apply the approved newer business state.

<details>
<summary>Explanation and references</summary>

A merge is not a business-rule generator. Multiple conflicting source rows for the same target key require a documented decision before the operation. The helper validates candidates and compares source revisions. It preserves the trip grain while updating the corrected values; it does not insert a new business trip for a correction.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 8: Revision precedence

- Newer approved revision: apply the update.
- Older revision: keep the accepted value.
- Equal revision with different values: reject the conflict.

<details>
<summary>Explanation and references</summary>

Identical same-revision messages are safe replays. Conflicting messages at the same revision have no unambiguous authority under this policy. Do not resolve them merely by whichever row happens to arrive first. Preserve a clear error and the source information so the conflict can be investigated.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 9: Quick activity: make the decision

- Choose a response for each message: a newer approved revision; an older revision; the same revision with conflicting business values.
- Think: 1 minute. Compare: 2 minutes. Discuss: 2 minutes.

<details>
<summary>Explanation and references</summary>

Use the project terms rather than naming tools without a reason. State your choice and the assumption behind it. The activity is part of the explanation time and has no separate project mark.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/PRACTICE.md)

</details>

---

## Slide 10: Activity answer

- Apply the newer revision, leave the accepted value unchanged for the older revision, and reject the same-revision conflict for investigation.

<details>
<summary>Explanation and references</summary>

Compare the reasoning as well as the final choice. If you selected another answer, identify which meaning of a row, time boundary or business rule led to it. The project will provide an observable example of this decision.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/PRACTICE.md)

</details>

---

## Slide 11: The correction is a value

- SYN_T0001 changes from SAR 18.00 to SAR 23.00.
- The total rises once by SAR 5.00.
- Replaying the correction leaves SAR 23.00 unchanged.

<details>
<summary>Explanation and references</summary>

Think of the message as the approved state of the trip, not an instruction to add five every time it is received. This is why the final table remains 75 trips and 1,880.60 SAR. The experiment checks the full relevant business content as well as the selected fare and total.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 12: History, time travel and RESTORE

- History describes the table operations.
- Time travel reads an available older snapshot.
- RESTORE creates a new commit representing earlier state.

<details>
<summary>Explanation and references</summary>

Reading an earlier version does not change the current table. RESTORE changes the current state through a new transaction; it does not erase the fact that the intervening operations happened. Both require the relevant historical files. Apply recovery experiments to the isolated copy, not to the continuing corrected project table.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 13: Controlled schema evolution

- Approve the additional field explicitly.
- Observe the changed schema on a sandbox.
- Keep the serving fare definition unchanged.

<details>
<summary>Explanation and references</summary>

The exercise adds a surcharge field in an isolated scenario. A new column is not permission to change the meaning of an existing fare measure. Inspect the before/after schema and ensure the main corrected Silver table is still the next day's source. Document how a real consumer would learn about an approved contract change.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 14: Compaction and logical content

- OPTIMIZE changes the physical file layout.
- The logical rows should remain equivalent.
- A tiny sample cannot establish production performance.

<details>
<summary>Explanation and references</summary>

Inspect the compaction operation and verify business-content equality. File count and scan time answer different questions, and no speed improvement is guaranteed for a tiny dataset. Initialization and caching can dominate measured timings. Report only the observed result and the scope of the experiment.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 15: VACUUM and retained history

- The lab uses DRY RUN only.
- Keep the 168-hour safety threshold.
- Removing required files can break older-version reads.

<details>
<summary>Explanation and references</summary>

The exercise lists candidate files without deleting them. An empty candidate list is a valid result. Data-file retention and transaction-log retention are related but different settings. The 168-hour boundary is the training rule here; an organization's actual retention requirements need their own decision and dependencies.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 16: A useful recovery record

- State the attempted change and the table version.
- Show the expected rejection or recovered content.
- Keep the sandbox separate from the main project.

<details>
<summary>Explanation and references</summary>

Retain counts, business values, operation history and relevant source details. The controlled exercise uses one writer and local state. It does not test concurrent writers, broker failover or a machine crash. Clear scope makes your evidence more useful than an unqualified claim that the pipeline is production-ready.

[Source 1](https://docs.delta.io/delta-constraints/) · [Source 2](https://docs.delta.io/delta-update/) · [Source 3](https://docs.delta.io/delta-utility/) · [Source 4](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/CONCEPTS.md)

</details>

---

## Slide 17: Your 60-minute lab

- Apply the approved fare correction and replay it.
- Inspect rejected writes, schema changes and history.
- Test recovery on a copy and keep corrected Silver.

<details>
<summary>Explanation and references</summary>

Use 45 minutes for the guided execution and checks,5 minutes for your first answer,5 minutes for discussion and 5 minutes for saving. The notebook includes setup and a small student-authored task. Read the walkthrough and inspect the outputs. This work adds to your existing project rather than starting a new assignment.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 18: Compare and save

- Corrected trip fare: SAR 23.00
- Silver trips: 75
- Total fares: SAR 1,880.60
- Save the notebook to GitHub and the full handoff to Drive.

<details>
<summary>Explanation and references</summary>

Expected checkpoints: Corrected trip fare: SAR 23.00. SYN_T0001 changes from SAR 18.00 at source revision 2. Silver trips: 75. A correction changes one trip instead of adding another. Total fares: SAR 1,880.60. The correction adds SAR 5.00 once. Correction replay: Unchanged. The same accepted correction does not add another SAR 5.00. Save day03/STUDENT.ipynb with your outputs. Upload the extracted small files from outputs/day03_github.zip. Keep outputs/day03_handoff.zip on Drive. Compare business content; run IDs, paths and timings can differ. Complete your student/dayNN lab notes and shared project notes before saving; the bundle includes the student folder.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 19: Your end-of-lab question

- A trip fare changes from SAR 18 to SAR 23. If the correction is delivered again, should the fare become SAR 28?
- Record your first answer and observed evidence in student/day03/REFLECTION.md.

<details>
<summary>Explanation and references</summary>

Work from your own run before reading the next slide. State the relevant grain, identity or time boundary. A count, fare, validation field or short query result can support your explanation. This reflection contributes one point to the 100-point project.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---

## Slide 20: Model answer

- No. The approved value stays SAR 23. Revision-aware MERGE applies the accepted business state; it does not repeatedly add a correction difference.

<details>
<summary>Explanation and references</summary>

Keep your initial answer and add a correction if needed. Explain the difference using a specific observed result from your notebook or report. The model answer is a learning reference, not a substitute for execution evidence.

[Source 1](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/README.md) · [Source 2](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/docs/EXPECTED_OUTPUTS.md)

</details>

---
