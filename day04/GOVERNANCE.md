# Day 4 · Document your data decisions

[Day 4](README.md) · [Existing governance template](../templates/GOVERNANCE.md) · [Submission guide](../project/SUBMISSION.md)

## Keep one governance note for the project

Use your existing `student/GOVERNANCE.md` to explain the decisions below. Reference the actual reports and paths rather than creating a separate governance project or duplicating lab notes. Purpose: learn ingestion, quality, traceability and controlled downstream use with the supplied synthetic dataset.

Do not add real customer trips, phone numbers, identity numbers or GPS traces. A `synthetic=true` label does not transform real data into synthetic data.

## Trace source to output

**Events:** source filename and SHA-256; producer acknowledgments; topic, partition and offset; raw Delta path and checkpoint; unique event snapshot.

**Trips:** corrected Day 3 Silver; isolated candidate; quality policy and GX results; quarantine or separately revalidated snapshot; selected Day 5 input.

Use `reports/day04_stream_latest.json` and `reports/day04_quality_latest.json` under your `WORK` folder. Copy your own run's identifiers into the note, not the example run ID shown in a saved notebook.

## Assign responsibilities in the design

The data owner approves purpose and permitted access; the operator investigates failed runs; the data steward explains quality rules and defects; the consumer selects approved snapshots. You may document all four roles as one learner. No additional staff or team is required for the exercise.

Example decision: keep the failed 82-row candidate for diagnosis, and permit downstream use only of the newly validated 75-trip snapshot. State who would review a rule change in a real implementation.

## Separate implemented controls from proposals

**Implemented in this lab:** loopback-only host port, fixed synthetic inputs, separate run paths, validation checks, quarantine and preserved reports.

**Design proposals, not implemented here:** user authentication, TLS, multi-user permissions and row-level access policies. A folder name or successful GX report does not enforce them. Keep the unauthenticated broker local and do not place credentials in the repository.

## Explain retention and transfer

Keep learning evidence through submission and the organizer's required review. The broker's 168-hour setting is an exercise configuration, not an organizational or statutory retention period. Kafka log retention and Delta version retention are different mechanisms.

Do not delete volumes or checkpoints to hide failure. The daily ZIP transfers Delta tables, reports, GX files and Spark checkpoints, but not the broker's data volume. Keep prior archives for separate evidence, including Day 2 dbt documentation. See [handoff boundaries](COMPLETION.md).

## Privacy references and submission

Before applying this design to real data, consult the organization's privacy, access and retention rules and the [official SDAIA references S10–S12](SOURCES.md). This synthetic exercise does not implement or certify legal compliance.

In the final project README and submission message, name the programme and [SDAIA Academy](https://github.com/SDAIAAcademy), include the Academy link and `#SDAIAAcademy`, following [the submission guide](../project/SUBMISSION.md). Preserve source attribution. Keep generated raw data, quarantine, broker storage, credentials and local GX folders out of ordinary Git commits.
