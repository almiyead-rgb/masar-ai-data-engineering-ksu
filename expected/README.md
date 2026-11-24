# Compare your actual results

Run your daily notebook in **Google Colab**. At the end of the lab, open
`outputs/dayNN_metrics.json` and compare it with the matching reference below.
Use **Compare results** in the course portal to compare the JSON locally in your
browser. Your file is not uploaded. The comparison is a learning check; your
instructor assesses the complete project using the 100-point rubric.

| Day | Expected business result | Reference contract | Actual executed notebook |
|---|---|---|---|
| 1 | 144 trip receipts, 72 unique trips, 6 drivers, 216 GPS events | [Day 1 JSON](day01.json) | [Day 1 notebook](../day01/STUDENT.ipynb) |
| 2 | 150 receipts, 75 Silver trips, SAR 1,875.60; dbt counts 72 → 72 → 75 → 75 | [Day 2 JSON](day02.json) | [Day 2 notebook](../day02/STUDENT.ipynb) |
| 3 | 75 trips, corrected fare SAR 23.00, total SAR 1,880.60 | [Day 3 JSON](day03.json) | [Day 3 notebook](../day03/STUDENT.ipynb) |
| 4 | 219 deliveries, 217 events; 82 candidates → 7 quarantined + 75 revalidated | [Day 4 JSON](day04.json) | [Day 4 notebook](../day04/STUDENT.ipynb) |
| 5 | Eight data products, 75 trips, SAR 1,880.60, 217 events, three unobserved labels | [Day 5 JSON](day05.json) | [Day 5 notebook](../day05/STUDENT.ipynb) |

## What must match

The dataset identifier, day number, integer counts and decimal money strings
must match. Money is stored as a two-decimal string so `"1880.60"` remains an
exact currency value. A floating-point value is not the same JSON contract.
The notebook computes observed metrics from actual engine reads and reports;
it never copies these reference JSON files into your results.

Generated run IDs, local paths, timestamps, measured timings and individual
physical file names vary. Explain differences in **business metrics** instead
of trying to reproduce another computer's timing or generated identifiers.

## Inspect the real run

Read the [execution record](../docs/VERIFICATION.md) for the actual validation
host, two-run status, output notebooks and report links. Expected JSON alone
is a specification. Executed notebook outputs and native reports provide the
run evidence. Preserve your own executed notebook and evidence every day.

[Detailed expected outputs](../docs/EXPECTED_OUTPUTS.md) · [Project rubric](../assessment/RUBRIC.md) · [Daily saving guide](../docs/GIT_WORKFLOW.md)
