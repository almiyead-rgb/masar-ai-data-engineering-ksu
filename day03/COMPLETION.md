# Day 3: save and continue

## Inspect your result

| Check | Expected value | Meaning |
|---|---|---|
| Corrected trip fare | **SAR 23.00** | SYN_T0001 changes from SAR 18.00 at source revision 2. |
| Silver trips | **75** | A correction changes one trip instead of adding another. |
| Total fares | **SAR 1,880.60** | The correction adds SAR 5.00 once. |
| Correction replay | **Unchanged** | The same accepted correction does not add another SAR 5.00. |

Read the full stage report for expected failures and business-content checks. A matching total alone does not prove every relationship or field is correct.

## Preserve your work

1. Complete `student/day03/LAB04_NOTES.md`. Keep the daily answer in `student/day03/REFLECTION.md`.
2. Edit the note files printed by the notebook setup in Colab's Files panel, replace their PENDING prompts with your observations, and save the text files. Then run the notebook's save/export step after the day's writers and queries have stopped.
3. Save the executed notebook to your fork, retaining its small outputs.
4. Upload the extracted small evidence files from `outputs/day03_github.zip` to the same repository.
5. Save `outputs/day03_handoff.zip` to Drive. Keep earlier archives until assessment is complete.
6. Open GitHub and verify that today's notebook and evidence are visible.

The full handoff preserves cumulative output state, including Delta files/logs, reports, pointers and the separate Day 2 dbt evidence. The notebook itself is saved separately. Do not replace the full state archive with a pointer JSON file or a CSV export.

## Restore safely

In a new Colab session, run setup and restore your own successful handoff using the notebook helper. Use the restored local workspace before running the next stage. Do not rerun an earlier day over state already changed by a later day. Keep the unchanged source dataset and recorded content version.

Proceed to Day 4 only after the current stage checks pass.

[Daily saving instructions](../docs/GIT_WORKFLOW.md) · [Troubleshooting](../docs/TROUBLESHOOTING.md) · [Project rubric](../assessment/RUBRIC.md)
