# Day 1: Architecture and Bronze

Keep the original data and explain your architecture choice.

**Outcomes:** LO1, LO2, LO8 · **20 slides** · **60-minute lab**

[Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/STUDENT.ipynb) · [Slides](../slides/day01.md) · [Concepts](CONCEPTS.md) · [Glossary](GLOSSARY.md)

## Before you begin

Start with the fixed source files and finish the readiness check. Use [the Colab setup](../docs/SETUP.md) and keep the shared synthetic source files unchanged. Read [execution evidence](../docs/VERIFICATION.md) for the scope of the published reference runs.

## What you learn

- Warehouse, data lake and Lakehouse
- Compute–storage separation and cost assumptions
- Bronze, Silver and Gold responsibilities
- Source provenance and receipt identity
- A small CSV/Delta scan comparison

## Your lab route

[Lab 01](labs/lab01/WALKTHROUGH.md) · [Lab 02](labs/lab02/WALKTHROUGH.md)

Run the daily notebook in order. Complete its short code or decision task and inspect the real component reports. Read the walkthrough to understand each operation instead of copying the full helper into extra cells. Keep one cumulative project throughout the week.

## Expected results

| Check | Expected value | Meaning |
|---|---|---|
| Trip receipts after redelivery | **144** | Two deliveries of the same 72-trip source. |
| Unique trip IDs | **72** | A business trip is different from a delivery receipt. |
| Drivers / GPS events | **6 / 216** | These inputs are not redelivered in this scenario. |

These values describe the fixed scenario. Your paths, timings and run identifiers can differ. Keep evidence of intentional rejection cases as well as successful cases. [Compare all days](../docs/EXPECTED_OUTPUTS.md).

## Activity and daily question

Use [the five-minute activity and question](PRACTICE.md). The activity and answer are slides 9–10; the lab question and model answer are slides 19–20. Use the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields to save your first answer and observed evidence in `student/day01/REFLECTION.md` before checking the model answer.

## Save your progress

- Executed Day 1 notebook
- student/day01/LAB01_NOTES.md and student/day01/LAB02_NOTES.md
- Architecture/cost decision and observed scan evidence
- Bronze counts and source metadata
- Day 1 GitHub bundle and handoff archive

The notebook save and full data handoff are different. Save your executed `day01/STUDENT.ipynb` to your fork; upload the small extracted files from `outputs/day01_github.zip`; retain `outputs/day01_handoff.zip` in Drive. [Saving guide](../docs/GIT_WORKFLOW.md) · [Completion and recovery](COMPLETION.md).
