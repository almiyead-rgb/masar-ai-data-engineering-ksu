# Lab 02 · Separate cost assumptions from measurements

[Course home](../../../README.md) · [Day 1](../../README.md) · [Execution record](../../../STATUS.md)

## A · Explain the economic model

Use [the cost notebook](../../STUDENT.ipynb). The defaults produce 1,460 teaching units for always-on operation and 185 for scheduled operation. These are arithmetic results of stated assumptions, not currency or provider quotations. The model includes a break-even case at 23.25 work hours per day and a counterexample at 23.75 hours. Keep storage, runtime, startup and orchestration assumptions visible.

## B · Define a comparable engine question

Ask: how long does a simple aggregate take on the same logical 72 rows read from CSV and from the initial Delta snapshot? Do not compare the 72-row CSV to the current 144-row Bronze table after replay. The experiment uses Delta version 0 and checks all original column values before comparing timings.

## C · Reuse the successful Bronze workspace

Open [the scan notebook](../../STUDENT.ipynb) after Lab 01. It reads the recorded successful workspace, validates its identity and report hash, and leaves earlier source files and tables untouched. It does not manufacture a replacement Bronze table inside the benchmark.

```python
from masar.workspace import completed_bronze_workspace
WORK = completed_bronze_workspace(ROOT)
print(WORK.relative_to(ROOT))
```

## D · Measure a Spark action, not a lazy definition

The shared experiment constructs a query, aggregates row count and fare totals, then calls `collect()`. It checks the result against independent Decimal arithmetic. The timer covers query creation, planning, execution and collection; it excludes session startup, ingestion and package installation. [Inspect the code](../../../src/masar/benchmark.py).

```python
from masar.benchmark import benchmark
result = benchmark(spark, SOURCE, WORK, repetitions=4)
print(result["measurements"])
```

## E · Repeat in balanced order

One warm-up per variant precedes four measured repetitions per variant, alternating CSV-first and Delta-first rounds. Save each duration, the median, minimum and maximum. There is no explicit DataFrame cache, but operating-system, JVM and metadata caches are not controlled. This is a repeated-read observation, not a cold-cache experiment.

## F · Explain the plan and the limits

Actual `explain(mode="formatted")` output is saved for both variants. Identify what was read and aggregated; do not call the displayed plan a measured duration. A slower Delta result does not fail the lab. The small fixture and single local machine cannot establish production scalability or universal performance rankings. See [Spark explain](https://spark.apache.org/docs/3.5.8/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html).

## Retain the evidence and write a bounded conclusion

Keep `reports/benchmark.json`, both plan files and the executed notebook. Use [BENCHMARKS.md](../../../templates/BENCHMARKS.md) and [student/day01/LAB02_NOTES.md](../../../templates/LAB_NOTES.md). State the population, timing scope, cache limits and observed variability. Do not insert example durations or treat hypothetical cost units as an actual bill.
