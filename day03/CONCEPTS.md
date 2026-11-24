# Day 3 · Understand safe data changes

[Day 3](README.md) · [Student notebook](STUDENT.ipynb) · [Glossary](GLOSSARY.md) · [References D1–D9](SOURCES.md)

## Start with the business change

Your Day 2 table has one row per trip: 75 trips and SAR 1,875.60 in fares. Today, `SYN_T0001` changes from SAR 18.00 to SAR 23.00. The correct result is still 75 trips, now totaling SAR 1,880.60. Use the [saved notebook outputs](STUDENT.ipynb) and your own execution to connect the following concepts to these values.

## 1. A Delta table is more than Parquet files

Parquet holds columnar data. The Delta transaction log identifies the committed table state and its metadata. After an update, old files may still exist. Read the table with the Delta reader; collecting every Parquet file can include obsolete data. Do not edit `_delta_log` manually. [D1]

## 2. Give ACID a practical meaning

**Atomicity:** a table write commits as a unit.

**Consistency:** defined constraints must hold.

**Isolation:** concurrent access follows snapshot and conflict rules.

**Durability:** committed state persists under the storage system’s guarantees.

In 04a, a single append with a valid row and a negative-fare row is rejected without partially changing the constrained copy. This tests that operation, not every ACID property under load. Separate table writes do not become one multi-table transaction. [D2, D3]

## 3. Separate source revision from table version

`source_revision` orders corrections to a particular trip. A Delta table version identifies a committed state of the whole table. Source revision 2 is not necessarily table version 2. Read the actual version from history. The scenario assigns revision 2 to the correction; the original CSV has no revision column.

## 4. Decide which revision wins

Use an explicit application policy: a valid missing key is inserted; a higher revision updates an existing key; identical revision and content leave values unchanged; an older revision is ignored; equal revisions with different content stop processing. Receiving the old SAR 18.00 value later must not erase the approved SAR 23.00 correction. These rules are defined in [this lab’s change policy](CHANGE_POLICY.md), not inferred automatically by Delta.

## 5. MERGE is not append

Match on `trip_id` and update only when `s.source_revision > t.source_revision`. Validate source and target uniqueness first: several source rows matching one target can make the update ambiguous. The supplied correction matches an existing trip, so the count remains 75. Trace `revision_merge_delta` in [the shared code](../src/masar/delta_lab.py); the notebook already calls it. [D4]

## 6. Compare business contents when replaying

Idempotency means that repeating the operation preserves its intended logical result. Compare sorted business rows or their canonical content hash. Correct runs may use different filenames, timestamps and transaction versions. A new history entry alone does not mean an extra trip was created.

## 7. Schema and business quality are different

A decimal fare can still be negative, and a string driver ID can still be unknown. Schema enforcement handles columns and types; constraints and explicit checks handle other rules. A declared business key is not automatically a uniqueness constraint in this setup. The lab uses `fare_sar IS NOT NULL AND fare_sar >= 0` so null is not mistaken for a valid non-negative fare. [D3, D9]

## 8. An expected failure needs specific evidence

A negative test succeeds only when the intended constraint or schema rejection occurs and the committed table’s rows, schema and version remain unchanged. A missing library or a disconnected Spark process is a different failure. Files staged during a failed write are not evidence of committed rows.

## 9. History and time travel are reads

`history()` shows recorded operations; `versionAsOf` reads a retained table version. Neither replaces the current table. In 04a, the captured pre-correction version shows SAR 18.00 while current Silver shows SAR 23.00. A prior version requires its necessary log and data files to remain available. [D1, D5]

## 10. Approve a schema change explicitly

The fixture adds `surcharge_sar` to an experimental copy. First, the write fails without schema permission. Then `mergeSchema=true` allows that one write. Older rows have null in the added field. Do not enable session-wide evolution merely to suppress mismatches. The surcharge does not automatically become part of `fare_sar`. [D1]

## 11. Preserve one row per trip in the schema demo

`SYN_T0002` already exists. Appending its extended record to all 75 rows would create a duplicate. The helper starts a new copy with the other 74 trips, then adds the extended row once: 75 unique trips, 74 null surcharges and one SAR 2.00 surcharge. Trusted Silver is unchanged.

## 12. RESTORE is a new write

The recovery copy starts at 75 rows, drops to 74 after a targeted DELETE, and returns to 75 after RESTORE. Unlike time travel, RESTORE commits the previous state as a new current version. History remains, and the version advances. This local recovery exercise is not a production backup strategy. [D5, D6]

## 13. Compaction changes file layout

OPTIMIZE can combine small files without changing business rows. Read active-file counts from table details, not from a count of every Parquet file on disk. Compare before/after business contents and the actual metrics. On this small dataset, neither a speed gain nor a lower file count is guaranteed. [D7]

## 14. Preview cleanup without deleting history’s data

The lab uses `VACUUM ... RETAIN 168 HOURS DRY RUN` on a sandbox only. It lists candidates without deleting them; zero candidates is valid. Keep the safety check enabled. Actual cleanup may remove data files needed for old versions. The 168-hour setting is an exercise rule, not a retention policy for every organization. [D5, D8]

## 15. Record what the experiment demonstrates

Keep the source filename and hash, revision rules, before/after business values, table versions and operation history. The lab uses one writer and a local table workflow. It does not test concurrent-writer load, crash recovery or distributed cloud durability. Successful lab checks should not be described as those unperformed experiments.

## 16. Continue with trusted outputs only

Day 4 uses corrected Silver and the original event feeds. A sandbox-only surcharge or deletion must not become a reporting fact or AI feature. Save your executed notebook, lab notes and handoff using [the completion checklist](COMPLETION.md). Read [the walkthrough](labs/lab04/WALKTHROUGH.md) to locate each operation and its evidence.
