# Troubleshooting your lab

Keep the first error, the failing cell and your runtime version report. Fix that failure before continuing. Do not edit a check to turn a failure into a pass.

| What you see | What to check | Safe next action |
|---|---|---|
| Unsupported Python or Java | Runtime report and environment instructions | Select the supported Colab runtime and rerun setup before Spark starts |
| Package/JAR download failure | The first network/download error | Retry the setup after connectivity returns; keep the pinned versions |
| A stale Spark process or conflicting session | Did you start another Spark session or rerun setup after importing Spark? | Restart the runtime, set up again and restore your last successful archive |
| Missing Day 1/2/3/4 pointer | Did you restore the complete handoff archive? | Restore your own previous archive, including the referenced data folders |
| Only a pointer exists | The folder it names may be missing | Restore the complete state; do not create a pointer manually |
| 144 Bronze rows | Did the Day 1 redelivery run? | This is expected; compare 72 distinct trip IDs |
| Silver has more than 75 trips | Business keys, duplicate handling and whether you changed the input | Inspect the scenario report; preserve the fixed data and repair the rule |
| Day 2 fails after Day 3 | You may be replaying an earlier stage over corrected state | Use the Day 2 archive in a separate clean workspace, or continue forward from Day 3 |
| dbt cannot see the source relations | You may be running dbt in a different process/catalog | Use the supplied notebook runner in its documented Spark session |
| Kafka is not ready | Local process log and readiness check | Follow the notebook startup step; do not point Colab to your laptop's localhost |
| Streaming restart fails after runtime deletion | Kafka topic data disappeared with the VM | Restore the end of Day 3 and start a new Day 4 experiment, with a new checkpoint/source namespace |
| The 82-row quality candidate fails | Did you reach the deliberate defect scenario? | Confirm seven quarantined records and a fresh passing 75-row candidate |
| AI future targets are null | Does the fixture observe the target hour? | Keep NULL/UNOBSERVED; do not convert unknown outcomes to zero |
| Your timing differs from the reference | Runtime, warm-up and downloads vary | Compare semantic results; timings are observations, not exact-match checks |
| GitHub shows an old notebook | The save target/path or branch may be wrong | Save to your fork, open the correct branch and inspect its latest commit |
| Notebook saved but data disappeared | A notebook file does not contain the VM filesystem | Restore the full handoff ZIP from Drive |

## Asking for help

Provide the day, cell heading, error text, runtime report and the last successful checkpoint. Remove account tokens and personal paths from screenshots or logs. You can use the repository's lab issue template for a generic technical problem, while keeping attendance, grading and private project links in the instructor's private channel.

## Recovery without losing evidence

Keep your earlier handoff archives. Restore into the course's documented local workspace using the restore helper, which checks the archive. Do not extract an unknown ZIP over your files. Never combine a recreated empty Kafka topic with an old Spark checkpoint and describe it as a successful resume.

[Environment setup](SETUP.md) · [Daily saves](GIT_WORKFLOW.md) · [Expected results](EXPECTED_OUTPUTS.md)
