# Day 2 · Primary references

[Day 2](README.md) · [dbt guide](DBT_GUIDE.md)

Use these references to explain the transformations. Use [the execution record](../docs/VERIFICATION.md) for the tested versions, and [the data contract](DATA_CONTRACT.md) for Masar field rules. The figures in the [notebook](STUDENT.ipynb) come from the supplied synthetic dataset, not an external operational system.

## D2-1 · [Spark 3.5.8 built-in functions](https://spark.apache.org/docs/3.5.8/sql-ref-functions-builtin.html)

Type conversion, timestamps and window functions.

## D2-2 · [Spark ANSI behavior and TRY_CAST](https://spark.apache.org/docs/3.5.8/sql-ref-ansi-compliance.html)

Casting failures and explicit validation of null results.

## D2-3 · [Delta MERGE](https://docs.delta.io/delta-update/)

Source deduplication and matching rows before a merge.

## D2-4 · [dbt ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

Model dependencies and relation resolution.

## D2-5 · [dbt source](https://docs.getdbt.com/reference/dbt-jinja-functions/source)

Referencing declared existing sources, not ingesting files.

## D2-6 · [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)

Incremental filters, keys and the distinction from full refresh.

## D2-7 · [dbt source freshness](https://docs.getdbt.com/reference/resource-properties/freshness)

Arrival-clock configuration and warning/error thresholds.

## D2-8 · [dbt build](https://docs.getdbt.com/reference/commands/build)

Building and testing in dependency order; freshness is a separate command.

dbt documentation may show newer version syntax. The course uses dbt Core 1.9.8 and dbt-spark 1.9.1 with the supplied project files; do not upgrade packages or copy newer configuration blocks into the exercise without retesting.
