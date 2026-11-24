# Day 5 · Primary references and local evidence

[Day 5](README.md) · [Concepts](CONCEPTS.md) · [AI/BI guide](AI_BI_GUIDE.md)

## Use the supplied versions

The [execution record](../docs/VERIFICATION.md) identifies the tested Python environment alongside the pinned Java 17, Spark 3.5.8 and Delta 3.3.3 components. Use the supplied requirements. Online Delta and conceptual documentation may describe newer features; they do not override the pinned exercise code.

The references below support concepts. The local notebook and reports supply evidence for this project's actual results. A vendor example is not evidence that your lab ran.

## D5-1 · [Delta batch reads and writes](https://docs.delta.io/delta-batch/)

Path-based tables, selected-version reads and the retained files needed to read an older snapshot.

## D5-2 · [Delta concurrency control](https://docs.delta.io/concurrency-control/)

Snapshot consistency and transaction conflict handling. The local multi-table release-selection rule is separately implemented in [serving.py](../src/masar/serving.py); the lab does not claim one global transaction.

## D5-3 · [Microsoft star-schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)

Facts, dimensions, grain and one-to-many relationships. Power BI is a conceptual example, not a required service or a tested connector in this course.

## D5-4 · [Spark 3.5.8 built-in functions](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html)

Aggregation and timestamp functions used by the course. The actual reporting query is [bi_zone_summary.sql](sql/bi_zone_summary.sql); the notebook registers its fact view before execution.

## D5-5 · [Feast point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

Retrieving feature values for a specified historical time. The exercise additionally checks source-revision availability from its fixed scenario schedule. Feast is not installed or called by these labs.

## D5-6 · [Python 3.12 CSV module](https://docs.python.org/3.12/library/csv.html)

Dictionary-based CSV writing and reading, including the empty-field representation of `None`. Lab 08 uses this module for bounded exports after native Delta validation; it is not a replacement for the Delta tables.

## Trace this project's numerical results

[STUDENT.ipynb](STUDENT.ipynb) retains actual native outputs; [the daily record](verification.json) documents the executed checks. [serving.py](../src/masar/serving.py) builds and reads the real Delta products. [serving_reference.py](../src/masar/serving_reference.py) independently calculates expected rows from the fixed sources.

[REFERENCE.ipynb](REFERENCE.ipynb) is an optional arithmetic aid, not native-engine evidence. The 75 trips, SAR 1,880.60 and 217 events come from [the supplied synthetic data](../data/DICTIONARY.md), not external operational statistics. Follow [the completion checklist](COMPLETION.md).
