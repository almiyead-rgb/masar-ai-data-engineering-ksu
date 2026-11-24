# Day 4: save and continue

## Inspect your result

| Check | Expected value | Meaning |
|---|---|---|
| Received message records | **219** | The experiment includes two replayed messages and one new late event. |
| Distinct events | **217** | The two identical replayed event IDs do not become new business events. |
| Quality candidate | **82 → rejected** | The candidate combines 75 trusted rows with seven deliberately defective rows. |
| Quarantine / revalidated | **7 / 75** | Record rejection reasons, then test a new clean candidate before approval. |

Read the full stage report for expected failures and business-content checks. A matching total alone does not prove every relationship or field is correct.

## Preserve your work

1. Complete `student/day04/LAB05_NOTES.md`, `student/day04/LAB06_NOTES.md`. Keep the daily answer in `student/day04/REFLECTION.md`.
2. Edit the note files printed by the notebook setup in Colab's Files panel, replace their PENDING prompts with your observations, and save the text files. Then run the notebook's save/export step after the day's writers and queries have stopped.
3. Save the executed notebook to your fork, retaining its small outputs.
4. Upload the extracted small evidence files from `outputs/day04_github.zip` to the same repository.
5. Save `outputs/day04_handoff.zip` to Drive. Keep earlier archives until assessment is complete.
6. Open GitHub and verify that today's notebook and evidence are visible.

The full handoff preserves cumulative output state, including Delta files/logs, reports, pointers and the separate Day 2 dbt evidence. The notebook itself is saved separately. Do not replace the full state archive with a pointer JSON file or a CSV export.

## Restore safely

In a new Colab session, run setup and restore your own successful handoff using the notebook helper. Use the restored local workspace before running the next stage. Do not rerun an earlier day over state already changed by a later day. Keep the unchanged source dataset and recorded content version.

For the Kafka experiment, a query restart requires its original compatible checkpoint, destination and source-topic data. A deleted runtime loses the broker. Restore the end of Day 3 and begin a new Day 4 experiment instead of attaching an old checkpoint to a recreated empty topic. Day 5 reads saved approved Delta snapshots and does not need the old broker.

Proceed to Day 5 only after the current stage checks pass.

[Daily saving instructions](../docs/GIT_WORKFLOW.md) · [Troubleshooting](../docs/TROUBLESHOOTING.md) · [Project rubric](../assessment/RUBRIC.md)
