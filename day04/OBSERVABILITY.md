# Day 4 · Read the right monitoring signal

[Day 4](README.md) · [Quality lab](labs/lab06/WALKTHROUGH.md) · [Quality policy](QUALITY_POLICY.md)

## Volume and rejection rate

State what one row represents. Final counts are 219 message receipts, 217 distinct events, 82 candidate trip rows, seven quarantined rows and 75 approved trips. They are different populations, not contradictory totals.

The rejected-row rate for the mixed candidate is `7 / 82 × 100 = 8.54%`, rounded to two decimals. Count rejected rows, not failed GX expectations or reason labels. The policy rejects the candidate even when most rows pass.

## Separate scenario freshness from actual run time

The quality report's `scenario_freshness` uses a fixed reference clock: `2026-06-04T03:04:00Z`. Latest source event: `2026-06-03T17:45:00Z`; its age is **33,540 seconds, or 9 hours 19 minutes**, within the example 43,200-second limit.

Scenario delivery: `2026-06-04T03:00:00Z`; age **240 seconds**, within the example 300-second limit. These figures are deterministic teaching calculations, not live network latency or broker lag. Do not replace their historical timestamps with today.

The streaming report's actual `broker_timestamp`, `ingested_at` and `progress` describe a different clock and execution. A negative age indicates future time or clock inconsistency, not extra freshness.

## Schema and distribution

Compare the 12 business columns with the existing Silver contract. Unknown columns, missing fields and wrong types need explicit checks; the absence of an exception alone does not establish quality.

`distribution` compares city shares in the approved trips with the corrected Day 3 trips. Total variation distance is `0.5 × Σ|current share − baseline share|`. It is zero for identical business contents. The example warning threshold is 0.10; exceeding it produces a diagnostic warning, not a statistical significance claim or an automatic promotion blocker in this lab.

## Turn a signal into a useful incident note

Within `student/day04/LAB05_NOTES.md` or `student/day04/LAB06_NOTES.md`, record the run ID, source, last successful phase, observed/expected measure and relevant rule. Identify whether the issue concerns environment, delivery, data or a policy decision. Link to the report rather than copying a long log.

Keep the last trusted output and failed evidence. Fix the identified cause and revalidate a new candidate. These files provide recorded diagnostics; they do not deploy a live dashboard or an alert-notification service.
