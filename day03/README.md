# Day 3: Delta reliability and corrections

Apply a correction once and keep a trustworthy history.

**Outcomes:** LO4, LO6, LO8 · **20 slides** · **60-minute lab**

[Open in Colab](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/STUDENT.ipynb) · [Slides](../slides/day03.md) · [Concepts](CONCEPTS.md) · [Glossary](GLOSSARY.md)

## Before you begin

Restore your own `outputs/day02_handoff.zip` if this is a new Colab session. Continue with the successful state from Day 2. Use [the Colab setup](../docs/SETUP.md) and keep the shared synthetic source files unchanged. Read [execution evidence](../docs/VERIFICATION.md) for the scope of the published reference runs.

## What you learn

- ACID transactions and the Delta log
- Schema enforcement and approved evolution
- Constraints and rejected writes
- Source revision versus Delta version
- MERGE, time travel and isolated maintenance

## Your lab route

[Lab 04](labs/lab04/WALKTHROUGH.md)

Run the daily notebook in order. Complete its short code or decision task and inspect the real component reports. Read the walkthrough to understand each operation instead of copying the full helper into extra cells. Keep one cumulative project throughout the week.

## Expected results

| Check | Expected value | Meaning |
|---|---|---|
| Corrected trip fare | **SAR 23.00** | SYN_T0001 changes from SAR 18.00 at source revision 2. |
| Silver trips | **75** | A correction changes one trip instead of adding another. |
| Total fares | **SAR 1,880.60** | The correction adds SAR 5.00 once. |
| Correction replay | **Unchanged** | The same accepted correction does not add another SAR 5.00. |

These values describe the fixed scenario. Your paths, timings and run identifiers can differ. Keep evidence of intentional rejection cases as well as successful cases. [Compare all days](../docs/EXPECTED_OUTPUTS.md).

## Activity and daily question

Use [the five-minute activity and question](PRACTICE.md). The activity and answer are slides 9–10; the lab question and model answer are slides 19–20. Use the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields to save your first answer and observed evidence in `student/day03/REFLECTION.md` before checking the model answer.

## Save your progress

- Executed Day 3 notebook
- student/day03/LAB04_NOTES.md
- Correction, stale-revision and conflict evidence
- Rejected write and history/recovery results
- Day 3 GitHub bundle and cumulative handoff archive

The notebook save and full data handoff are different. Save your executed `day03/STUDENT.ipynb` to your fork; upload the small extracted files from `outputs/day03_github.zip`; retain `outputs/day03_handoff.zip` in Drive. [Saving guide](../docs/GIT_WORKFLOW.md) · [Completion and recovery](COMPLETION.md).
