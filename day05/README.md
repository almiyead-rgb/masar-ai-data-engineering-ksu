# Day 5: Gold, AI/BI and final delivery

Publish understandable data products and submit your cumulative work.

**Outcomes:** LO6, LO7, LO8 · **20 slides** · **60-minute lab**

[Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/STUDENT.ipynb) · [Slides](../slides/day05.md) · [Concepts](CONCEPTS.md) · [Glossary](GLOSSARY.md)

## Before you begin

Restore your own `outputs/day04_handoff.zip` if this is a new Colab session. Continue with the successful state from Day 4. Use [the Colab setup](../docs/SETUP.md) and keep the shared synthetic source files unchanged. Read [execution evidence](../docs/VERIFICATION.md) for the scope of the published reference runs.

## What you learn

- Product contracts, facts, dimensions and grain
- BI reconciliation without multiplying fares
- Historical features and availability at decision time
- Unknown future labels versus zero
- Release validation, recovery and reproducible delivery

## Your lab route

[Lab 07](labs/lab07/WALKTHROUGH.md) · [Lab 08](labs/lab08/WALKTHROUGH.md)

Run the daily notebook in order. Complete its short code or decision task and inspect the real component reports. Read the walkthrough to understand each operation instead of copying the full helper into extra cells. Keep one cumulative project throughout the week.

## Expected results

| Check | Expected value | Meaning |
|---|---|---|
| Validated products / CSV exports | **8 / 8** | Read each product contract and release manifest. |
| Reconciled trips / fares | **75 / SAR 1,880.60** | Aggregated products reconcile to the same trusted trips. |
| Recorded GPS events | **217** | Count events by trip before joining them to fare measures. |
| AI feature / label rows | **3 / 3** | Feature rows use historical data. Future labels remain NULL with UNOBSERVED status. |

These values describe the fixed scenario. Your paths, timings and run identifiers can differ. Keep evidence of intentional rejection cases as well as successful cases. [Compare all days](../docs/EXPECTED_OUTPUTS.md).

## Activity and daily question

Use [the five-minute activity and question](PRACTICE.md). The activity and answer are slides 9–10; the lab question and model answer are slides 19–20. Use the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields to save your first answer and observed evidence in `student/day05/REFLECTION.md` before checking the model answer.

## Save your progress

- Executed Day 5 notebook
- student/day05/LAB07_NOTES.md and student/day05/LAB08_NOTES.md
- Eight product exports and release manifest
- BI reconciliation, AI feature checks and recovery evidence
- Final project README and five daily answers
- Final repository URL, branch and commit SHA

The notebook save and full data handoff are different. Save your executed `day05/STUDENT.ipynb` to your fork; upload the small extracted files from `outputs/day05_github.zip`; retain `outputs/day05_handoff.zip` in Drive. [Saving guide](../docs/GIT_WORKFLOW.md) · [Completion and recovery](COMPLETION.md).
