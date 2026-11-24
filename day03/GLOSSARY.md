# Day 3 · Glossary

[Course home](../README.md) · [Execution record](../STATUS.md)

## How to read

Each entry includes the English term, both explanations, an example and approximate Arabic pronunciation. Pronunciation is a learning aid, not formal phonetic notation.

### Transaction

A set of table changes committed as one unit.

**Example:** Fare correction write.

### ACID

Atomicity, Consistency, Isolation and Durability.

**Example:** A failed constrained write must not partially commit.

### Atomicity

All changes in the transaction commit, or none become committed.

**Example:** One valid plus one invalid row in a single write.

### Consistency

The transaction preserves the defined constraints.

**Example:** A non-negative fare constraint.

### Isolation

Concurrent operations have defined snapshot and conflict behaviour.

**Example:** A reader sees a consistent snapshot.

### Durability

Committed state persists with supported storage guarantees.

**Example:** A committed table is readable afterward.

### Transaction log

The table’s record of committed changes and metadata.

**Example:** The _delta_log directory.

### Snapshot

A view of table contents at a particular version.

**Example:** Silver before the correction.

### Table version

A number identifying a committed table state.

**Example:** Read from Delta history.

### Source revision

A source/application ordering of entity corrections.

**Example:** Revision 2 supersedes revision 1.

### MERGE

Match source rows to target rows and apply specified actions.

**Example:** Update only a newer revision.

### Upsert

Update a matching row or insert a missing one.

**Example:** Match on trip_id.

### Idempotency

Repeating an operation preserves its intended logical result.

**Example:** Replay the same correction without adding another trip.

### Stale data

An older value arriving after a newer approved revision.

**Example:** The old 18.00 fare arrives again.

### Conflict

Incompatible changes requiring an explicit decision.

**Example:** Same revision with two different fares.

### Schema enforcement

Reject unapproved structural/type differences in a write.

**Example:** An unapproved extra surcharge column.

### Schema evolution

An explicitly allowed change to the table structure.

**Example:** Add surcharge_sar to a sandbox only.

### CHECK constraint

A rule applied to values written into a table.

**Example:** fare_sar IS NOT NULL AND fare_sar >= 0.

### Time travel

Read a retained older table version.

**Example:** versionAsOf before correction.

### RESTORE

Commit a previous table state as a new current state.

**Example:** Restore the recovery copy from 74 to 75 trips.

### Compaction

Rewrite small data files into a more consolidated layout.

**Example:** OPTIMIZE on a copy.

### Retention

How long data/log history is kept under configured rules.

**Example:** 168-hour cleanup threshold in the safe demo.

### Dry run

Preview the operation’s candidates without performing deletion.

**Example:** VACUUM ... DRY RUN.

### Sandbox

An isolated training copy that does not alter trusted outputs.

**Example:** sandbox/day03/recovery_<id>.
