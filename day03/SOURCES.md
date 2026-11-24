# Day 3 · Primary references

[Day 3](README.md) · [Concepts](CONCEPTS.md) · [Lab 04 walkthrough](labs/lab04/WALKTHROUGH.md)

## Use the references with the supplied environment

The course pins Spark 3.5.8 and Delta 3.3.3 with Java 17. The runtime record states the Python version actually exercised. Some documentation links show newer releases. Use the supplied requirements and the code in [delta_lab.py](../src/masar/delta_lab.py); do not copy a newer feature into the exercise without retesting. See [the tested environment](../docs/VERIFICATION.md).

## D1 · [Batch reads, writes and schema](https://docs.delta.io/delta-batch/)

Delta snapshots, retained-version reads, schema enforcement and explicit schema evolution.

## D2 · [Concurrency control](https://docs.delta.io/concurrency-control/)

Snapshot consistency, transaction conflicts and the boundaries of concurrent table operations.

## D3 · [CHECK and NOT NULL constraints](https://docs.delta.io/delta-constraints/)

Value constraints and rejection of writes that violate them.

## D4 · [MERGE, updates and deletes](https://docs.delta.io/delta-update/)

Matching source rows to targets, conditional updates and ambiguous duplicate source rows.

## D5 · [History, RESTORE and VACUUM](https://docs.delta.io/delta-utility/)

Operation history, recovery commits, dry-run candidates and retention safeguards. The lab uses dry run only; it does not delete expired data files.

## D6 · [Delta Python API](https://docs.delta.io/api/latest/python/spark/)

Read the signatures of `history`, `merge`, `restoreToVersion` and `optimize`. The latest-reference page can differ from the pinned course release.

## D7 · [Open-source OPTIMIZE](https://docs.delta.io/optimizations-oss/)

Compaction and its effect on file layout without changing table results.

## D8 · [Table retention properties](https://docs.delta.io/table-properties/)

The distinction between log retention and retention of obsolete data files.

## D9 · [Spark 3.5.8 null semantics](https://spark.apache.org/docs/3.5.8/sql-ref-null-semantics.html)

Null comparisons and the need for explicit missing-value checks.

## Trace the course results

Trip counts and fare totals come from the unchanged [synthetic dataset](../data/DICTIONARY.md) and are checked in [the executed notebook](STUDENT.ipynb). Revision precedence, permitted mutations and sandbox boundaries are explicit [lab rules](CHANGE_POLICY.md). The optional [calculation reference](REFERENCE.ipynb) helps reconcile arithmetic; [the execution record](verification.json) documents actual Spark and Delta checks.
