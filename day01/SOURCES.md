# Day 1 sources

[Day 1](README.md) · [Course home](../README.md)

These sources support the explanations, not a claim of successful engine execution. Hypothetical cost units are teaching assumptions, not provider prices.

## [S1] Course definition

[Course definition](../TRAINING_CONTENT.md) — The supplied learning outcomes and agreed cumulative lab scope.

## [S2] Medallion architecture

[Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) — Bronze, Silver and Gold responsibilities.

## [S3] Snowflake architecture

[Snowflake architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) — A warehouse example with storage/compute separation.

## [S4] Delta quick start

[Delta quick start](https://docs.delta.io/quick-start/) — Session configuration, writes, reads and previous versions.

## [S5] Delta constraints

[Delta constraints](https://docs.delta.io/delta-constraints/) — Constraints and write rejection.

## [S6] Spark execution concepts

[Spark execution concepts](https://spark.apache.org/docs/3.5.8/rdd-programming-guide.html) — Transformations, actions and persistence.

## [S7] Delta/Spark compatibility

[Delta/Spark compatibility](https://docs.delta.io/releases/) — Use a compatible version family; compatibility is not runtime proof.

## [S8] Spark SQL and DataFrames

[Spark SQL and DataFrames](https://spark.apache.org/docs/3.5.8/sql-programming-guide.html) — Structured data and SQL queries.

## [S9] Fixed synthetic data

[Fixed synthetic data](../data/masar-small-v1/manifest.json) — The approved manifest and file hashes. No real people or journeys.

## [S10] Spark installation requirements

[Spark installation requirements](https://spark.apache.org/docs/3.5.8/api/python/getting_started/install.html) — Use the version-specific Python and Java requirements.

## [S11] Apache Parquet

[Apache Parquet](https://parquet.apache.org/docs/overview/) — Background on columnar storage.

## [S12] Google Colab limits

[Google Colab limits](https://research.google.com/colaboratory/faq.html) — Resource and runtime persistence context; not a promise of availability.

## [S13] Course cost arithmetic

[Course cost arithmetic](STUDENT.ipynb) — Run the cost section and retain your observed values. The execution record states which release was actually tested.

## Implementation details

[CSV schemas and reader options](https://spark.apache.org/docs/3.5.8/sql-data-sources-csv.html) · [Query plans](https://spark.apache.org/docs/3.5.8/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.explain.html). Use [current execution status](../docs/VERIFICATION.md) for what has actually run.
