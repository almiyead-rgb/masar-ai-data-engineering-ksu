[Course home](../README.md) · [Start here](../docs/START_HERE.md) · [Execution record](../STATUS.md)

## Day 1: from files to an architecture decision

SDA-DSC-214 · Modern Data Engineering for AI Systems. Instructor: Meaad Al-Marri. This cohort meets on five evenings,17:00–21:00, with 150 minutes of explanation,60 minutes of lab and two 15-minute prayer breaks per day. The explanation is staged for mixed prior experience. The eight cumulative labs form one final project; there is no additional final project. Excellence tasks are entirely optional. [S1]

## Your Day 1 learning path

This guide covers the source inspection, Delta Bronze writes and Spark scan measurement in Labs 01 and 02. Use the combined notebook for the full sequence. [Execution evidence and environment limits](../STATUS.md) are recorded separately from the conceptual explanation.

## C01 · Start with the consumer question

Masar is a fictional trip-data project, not a ride-booking app. Ask two questions: how many trips were completed per city and day, and what trustworthy columns could later support a model? Before selecting a tool, state the input, desired output, freshness need and owner. For a daily report, constant streaming may add complexity without meeting an additional need. For an event alert, a next-day batch may be too late. These are design scenarios, not measured service requirements.

## C02 · One row must have one stated meaning

In the fixed fixture, trips.csv has 72 rows, drivers.csv has six rows and gps.ndjson has 216 events. A trip key is trip_id; a driver key is driver_id; an event key is event_id. Each trip has three base GPS events. Counting rows after joining trips to all their events would count event-level rows, not distinct trips. Keep the grain explicit before aggregation. Run the source-inspection notebook to inspect the source rather than trusting these counts as an engine result. [S9]

## C03 · Warehouse, lake and lakehouse: compare capabilities

Use three lenses: a warehouse emphasizes governed analytical tables; a lake emphasizes retaining varied source data; a lakehouse adds table-management capabilities over lake storage. Real products overlap, so these are not rigid mutually exclusive boxes. For Masar, we select a small lakehouse to teach ingestion, table transactions and reuse for reporting and AI. We are not claiming that all warehouses are old, lack AI support or couple storage to compute. Snowflake explicitly separates storage and compute. [S3, S4]

## C04 · Bronze, Silver and Gold are responsibilities

For this project, Bronze preserves incoming records and ingestion metadata. Silver holds typed, linked and checked trip records. Gold serves a defined question, such as daily trips by city. These names describe a design pattern, not automatic quality guarantees. A folder named gold does not prove its values are correct. Write a contract for each boundary: intended grain, required columns, owner, checks and acceptable freshness. [S2]

## C05 · Read does not mean clean; append does not mean unique

The base fixture intentionally has no duplicate keys. Later scenario files contain delayed records, a correction, quality cases and a schema change. Do not mix them into the initial load. In the Bronze replay, appending the same 72 trips twice is expected to produce 144 stored rows. Compare this expected result with the actual report from your daily notebook. Silver must then apply an explicit key/version rule; blindly dropping conflicting versions can lose a valid correction. [S1, S9]

## C06 · Spark computes; Delta manages table state

Spark is the processing engine used here. Delta adds table transactions and schema controls to the storage layer. The lab checks actual writes, reads and transaction-log evidence; a CSV profile or a plain Parquet file is not a replacement. ACID is a transaction property, not a claim that every business value is correct. A negative fare needs a business rule or constraint. Later labs will test an invalid write and verify that valid table state is preserved. [S4, S5, S8]

## C07 · Distinguish physical separation from local folders

Conceptually, independent compute can stop while durable storage remains. Our local teaching folder layout illustrates responsibilities; it does not demonstrate independent cloud scaling or reliable storage after a notebook runtime is deleted. Record where data live, what survives engine shutdown, and what must be exported before a temporary runtime ends. For the operating-cost exercise, hold storage constant and vary billed compute hours. [S3]

## C08 · Cost claims need units, assumptions and counterexamples

The cost section of the daily notebook and the workbook use hypothetical teaching units, not SAR or USD. A planning volume of 100 GiB is assumed independently of the small fixture. Both schedules use four cores and the same storage. Start with two work hours and 0.25 startup hours per day; then increase the workload. Additional scheduled charges are explicit. Read the difference with its sign. This budget is not an actual provider comparison, performance measurement or procurement recommendation.

## C09 · What counts as evidence?

A saved output must identify the code, input release and scope. Here, source_inspection.json demonstrates source-file checks; cost_model_result.json demonstrates arithmetic. Neither proves a Delta commit or Kafka delivery. Later engine evidence must include actual tables, transaction logs and fresh-run comparison. A query plan alone does not prove a speedup: real measurements must execute work, control caching/warm-up, reconcile results and report limitations. [S1, S6]

## Day 1 workflow and learner evidence

Read C01–C06, then complete Lab 01 and its notes. Read C07–C09, complete Lab 02, and compare the observed scan measurements. Record your architecture decision: the need, chosen design, alternatives and limitations. Save these results as the first stage of your cumulative project. [S1]

References: see SOURCES.md. The fixture, assumptions and executed outputs are bundled. Follow the links to the daily notebook and sources.

The initial trip keys are unique, but 10 rows contain city labels with surrounding spaces and lower-case letters. Profiling identifies this without altering the raw source.
