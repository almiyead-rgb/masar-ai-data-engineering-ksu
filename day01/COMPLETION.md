# Day 1: save and continue

## Inspect your result

| Check | Expected value | Meaning |
|---|---|---|
| Trip receipts after redelivery | **144** | Two deliveries of the same 72-trip source. |
| Unique trip IDs | **72** | A business trip is different from a delivery receipt. |
| Drivers / GPS events | **6 / 216** | These inputs are not redelivered in this scenario. |

Read the full stage report for expected failures and business-content checks. A matching total alone does not prove every relationship or field is correct.

## Preserve your work

1. Complete `student/day01/LAB01_NOTES.md`, `student/day01/LAB02_NOTES.md`. Keep the daily answer in `student/day01/REFLECTION.md`.
2. Edit the note files printed by the notebook setup in Colab's Files panel, replace their PENDING prompts with your observations, and save the text files. Then run the notebook's save/export step after the day's writers and queries have stopped.
3. Save the executed notebook to your fork, retaining its small outputs.
4. Upload the extracted small evidence files from `outputs/day01_github.zip` to the same repository.
5. Save `outputs/day01_handoff.zip` to Drive. Keep earlier archives until assessment is complete.
6. Open GitHub and verify that today's notebook and evidence are visible.

The full handoff preserves cumulative output state, including Delta files/logs, reports, pointers and the separate Day 2 dbt evidence. The notebook itself is saved separately. Do not replace the full state archive with a pointer JSON file or a CSV export.

## Restore safely

In a new Colab session, run setup and restore your own successful handoff using the notebook helper. Use the restored local workspace before running the next stage. Do not rerun an earlier day over state already changed by a later day. Keep the unchanged source dataset and recorded content version.

Proceed to Day 2 only after the current stage checks pass.

[Daily saving instructions](../docs/GIT_WORKFLOW.md) · [Troubleshooting](../docs/TROUBLESHOOTING.md) · [Project rubric](../assessment/RUBRIC.md)
