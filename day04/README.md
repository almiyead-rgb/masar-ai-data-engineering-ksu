# Day 4: Streaming, quality and governance

Receive events and stop defective data before serving it.

**Outcomes:** LO5, LO6, LO8 · **20 slides** · **60-minute lab**

[Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/STUDENT.ipynb) · [Slides](../slides/day04.md) · [Concepts](CONCEPTS.md) · [Glossary](GLOSSARY.md)

## Before you begin

Restore your own `outputs/day03_handoff.zip` if this is a new Colab session. Continue with the successful state from Day 3. Use [the Colab setup](../docs/SETUP.md) and keep the shared synthetic source files unchanged. Read [execution evidence](../docs/VERIFICATION.md) for the scope of the published reference runs.

## What you learn

- Kafka producers, topics, partitions and offsets
- Spark streaming and checkpoint restart
- Event time, arrival time and event identity
- Great Expectations quality gates and quarantine
- Freshness, volume, lineage and ownership

## Your lab route

[Lab 05](labs/lab05/WALKTHROUGH.md) · [Lab 06](labs/lab06/WALKTHROUGH.md)

Run the daily notebook in order. Complete its short code or decision task and inspect the real component reports. Read the walkthrough to understand each operation instead of copying the full helper into extra cells. Keep one cumulative project throughout the week.

## Expected results

| Check | Expected value | Meaning |
|---|---|---|
| Received message records | **219** | The experiment includes two replayed messages and one new late event. |
| Distinct events | **217** | The two identical replayed event IDs do not become new business events. |
| Quality candidate | **82 → rejected** | The candidate combines 75 trusted rows with seven deliberately defective rows. |
| Quarantine / revalidated | **7 / 75** | Record rejection reasons, then test a new clean candidate before approval. |

These values describe the fixed scenario. Your paths, timings and run identifiers can differ. Keep evidence of intentional rejection cases as well as successful cases. [Compare all days](../docs/EXPECTED_OUTPUTS.md).

## Activity and daily question

Use [the five-minute activity and question](PRACTICE.md). The activity and answer are slides 9–10; the lab question and model answer are slides 19–20. Use the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields to save your first answer and observed evidence in `student/day04/REFLECTION.md` before checking the model answer.

## Save your progress

- Executed Day 4 notebook
- student/day04/LAB05_NOTES.md and student/day04/LAB06_NOTES.md
- Kafka, checkpoint and distinct-event reports
- GX validation and quarantine reasons
- GOVERNANCE.md and monitoring observations
- Day 4 GitHub bundle and cumulative handoff archive

The notebook save and full data handoff are different. Save your executed `day04/STUDENT.ipynb` to your fork; upload the small extracted files from `outputs/day04_github.zip`; retain `outputs/day04_handoff.zip` in Drive. [Saving guide](../docs/GIT_WORKFLOW.md) · [Completion and recovery](COMPLETION.md).
