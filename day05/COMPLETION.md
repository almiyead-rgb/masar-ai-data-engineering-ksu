# Day 5: save and continue

## Inspect your result

| Check | Expected value | Meaning |
|---|---|---|
| Validated products / CSV exports | **8 / 8** | Read each product contract and release manifest. |
| Reconciled trips / fares | **75 / SAR 1,880.60** | Aggregated products reconcile to the same trusted trips. |
| Recorded GPS events | **217** | Count events by trip before joining them to fare measures. |
| AI feature / label rows | **3 / 3** | Feature rows use historical data. Future labels remain NULL with UNOBSERVED status. |

Read the full stage report for expected failures and business-content checks. A matching total alone does not prove every relationship or field is correct.

## Preserve your work

1. Complete `student/day05/LAB07_NOTES.md`, `student/day05/LAB08_NOTES.md`. Keep the daily answer in `student/day05/REFLECTION.md`.
2. Edit the note files printed by the notebook setup in Colab's Files panel, replace their PENDING prompts with your observations, and save the text files. Then run the notebook's save/export step after the day's writers and queries have stopped.
3. Save the executed notebook to your fork, retaining its small outputs.
4. Upload the extracted small evidence files from `outputs/day05_github.zip` to the same repository.
5. Save `outputs/day05_handoff.zip` to Drive. Keep earlier archives until assessment is complete.
6. Open GitHub and verify that today's notebook and evidence are visible.

The full handoff preserves cumulative output state, including Delta files/logs, reports, pointers and the separate Day 2 dbt evidence. The notebook itself is saved separately. Do not replace the full state archive with a pointer JSON file or a CSV export.

## Restore safely

In a new Colab session, run setup and restore your own successful handoff using the notebook helper. Use the restored local workspace before running the next stage. Do not rerun an earlier day over state already changed by a later day. Keep the unchanged source dataset and recorded content version.

Complete the final README and submit the same cumulative project through the announced private channel.

[Daily saving instructions](../docs/GIT_WORKFLOW.md) · [Troubleshooting](../docs/TROUBLESHOOTING.md) · [Project rubric](../assessment/RUBRIC.md)
