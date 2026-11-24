[Course home](../README.md) · [Start here](../docs/START_HERE.md) · [Execution record](../STATUS.md)

## Day 1 glossary

Pronunciation is an approximate reading aid, not a phonetic standard. Technical references: S2–S8.

**Data architecture**

How data storage, processing and consumers fit together.

*Example:* Masar sources → trusted outputs

**Data warehouse**

A system organized for managed analytical tables and queries.

*Example:* Daily reporting tables

**Data lake**

Storage that can retain varied source data.

*Example:* CSV and JSON inputs

**Lakehouse**

Table-management capabilities over lake storage.

*Example:* Delta tables for Masar

**Compute**

Resources that execute processing.

*Example:* Spark processing

**Storage**

Where data remain when retained.

*Example:* Persistent table files

**Schema**

Named fields and their data types.

*Example:* fare_sar: decimal

**Grain**

The exact meaning of one row.

*Example:* One row per trip

**Primary key**

The identifier intended to distinguish a row at its grain.

*Example:* trip_id

**Ingestion**

Receiving source data into a pipeline.

*Example:* Read incoming trips

**Lineage**

Recorded origin and movement of data.

*Example:* Source file + ingestion time

**Append**

Add records while retaining previous records.

*Example:* A controlled 72-row replay

**Overwrite**

Replace data within an explicitly defined scope.

*Example:* Rebuild an isolated result

**Bronze**

The project’s incoming-record layer.

*Example:* Raw trips + source metadata

**Silver**

The project’s typed and checked reusable layer.

*Example:* Clean trips linked to drivers

**Gold**

Outputs designed for a specific consumer question.

*Example:* Trips per city per day

**Idempotency**

Repeating an operation leaves its intended state unchanged.

*Example:* A keyed Silver replay

**ACID**

Atomicity, consistency, isolation and durability for transactions.

*Example:* Test a rejected invalid write

**Elasticity**

Adjusting compute capacity to workload demand.

*Example:* Schedule and stop compute

**Break-even**

Where two modeled total costs are equal.

*Example:* 23.25 work hours/day in this example
