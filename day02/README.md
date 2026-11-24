# Day 2: ELT and trusted Silver

Turn repeated receipts into reliable business records.

**Outcomes:** LO3, LO4, LO8 · **20 slides** · **60-minute lab**

[Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/STUDENT.ipynb) · [Slides](../slides/day02.md) · [Concepts](CONCEPTS.md) · [Glossary](GLOSSARY.md)

## Before you begin

Restore your own `outputs/day01_handoff.zip` if this is a new Colab session. Continue with the successful state from Day 1. Use [the Colab setup](../docs/SETUP.md) and keep the shared synthetic source files unchanged. Read [execution evidence](../docs/VERIFICATION.md) for the scope of the published reference runs.

## What you learn

- ETL versus ELT
- Types, timestamps and relationships
- Business keys and deterministic deduplication
- Late arrivals and idempotent processing
- dbt models, tests, freshness and lineage

## Your lab route

[Lab 03](labs/lab03/WALKTHROUGH.md)

Run the daily notebook in order. Complete its short code or decision task and inspect the real component reports. Read the walkthrough to understand each operation instead of copying the full helper into extra cells. Keep one cumulative project throughout the week.

## Expected results

| Check | Expected value | Meaning |
|---|---|---|
| Silver trips | **75** | 72 base trips plus three late trips; replay adds no business trips. |
| Total fares | **SAR 1,875.60** | SAR 1,794.60 plus SAR 81.00 of late-trip fares. |
| Final Bronze receipts | **150** | Receipts record the original deliveries and the late-batch redelivery. |
| dbt phase counts | **72, 72, 75, 75** | Base, rerun, late and late_replay. |

These values describe the fixed scenario. Your paths, timings and run identifiers can differ. Keep evidence of intentional rejection cases as well as successful cases. [Compare all days](../docs/EXPECTED_OUTPUTS.md).

## Activity and daily question

Use [the five-minute activity and question](PRACTICE.md). The activity and answer are slides 9–10; the lab question and model answer are slides 19–20. Use the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields to save your first answer and observed evidence in `student/day02/REFLECTION.md` before checking the model answer.

## Save your progress

- Executed Day 2 notebook
- student/day02/LAB03_NOTES.md and your SQL task
- Five Silver scenario checks
- Actual dbt report, model/test evidence and documentation
- Day 2 GitHub bundle and cumulative handoff archive

The notebook save and full data handoff are different. Save your executed `day02/STUDENT.ipynb` to your fork; upload the small extracted files from `outputs/day02_github.zip`; retain `outputs/day02_handoff.zip` in Drive. [Saving guide](../docs/GIT_WORKFLOW.md) · [Completion and recovery](COMPLETION.md).
