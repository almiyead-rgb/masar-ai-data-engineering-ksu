# Fixed synthetic Masar data

[Course home](../README.md) · [Start here](../docs/START_HERE.md) ·
[Data dictionary](DICTIONARY.md)

**MASAR_SMALL_V1** is the fixed teaching dataset for your cumulative project.
It describes fictional trips, drivers and location events. No record represents
a real person or journey. The scenario dates and deliveries are fixed, so your
business results remain comparable when you run the course on a different date.

## Start with the base feeds

| Source | Base rows | Use |
|---|---:|---|
| [trips.csv](masar-small-v1/trips.csv) | 72 | Trip IDs, fares, times and city labels |
| [drivers.csv](masar-small-v1/drivers.csv) | 6 | Driver reference data |
| [gps.ndjson](masar-small-v1/gps.ndjson) | 216 | Location events linked to trips |

Day 1 deliberately delivers the trip source twice. You should therefore observe
144 Bronze trip receipts and 72 distinct trip IDs. The driver and GPS base feeds
are not redelivered in that exercise.

## Apply each scenario on its assigned day

Keep the late trips, correction, schema change, quality cases and event replays
separate until the notebook requests them. The
[scenario schedule](masar-small-v1/scenario_schedule.json) defines their fixed
times. Loading every scenario on Day 1 would change the meaning of your result.

- Day 2 adds three late trips and checks that replay does not create new business trips.
- Day 3 applies an approved fare correction once and tests rejected writes.
- Day 4 introduces event replays, one late event and seven deliberately invalid quality rows.
- Day 5 consumes the approved tables built by the preceding days.

## Verify before processing

The [manifest](masar-small-v1/manifest.json) records the size, row count and
SHA-256 hash for each source file. Its approved SHA-256 is
`20a7e45bed2980b9394c10e8532da3b9f40f614366bb2df26a88610253e768e3`.
The runtime checks both the manifest and the individual files. Preserve the raw
city-label variants until the documented Silver cleaning step.

A source integrity check establishes that you are using the intended input.
Your notebook's native engine reports establish what the pipeline did with it.
Compare those reports with the [expected daily results](../docs/EXPECTED_OUTPUTS.md).
