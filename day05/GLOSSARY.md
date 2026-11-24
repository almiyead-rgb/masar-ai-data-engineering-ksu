# Day 5 glossary · 26 terms

[Course home](../README.md) · [Execution record](../STATUS.md) · [Day 5](README.md)

## How to use the glossary

Read the term, explanation and example; pronunciation is approximate support, not a phonetic transcription.

## Data product

A table or dataset defined for a consumer.

**Example:** zone_hourly_demand

## Grain

What one row represents.

**Example:** one driver per local day

## Fact table

Observations and measurable values at a fixed grain.

**Example:** bi.fact_trips

## Dimension

Descriptions used to filter and group facts.

**Example:** bi.dim_zone

## Star schema

Fact table related to descriptive dimensions.

**Example:** trip fact + date/driver/zone

## Natural key

Business identifier reused as a key.

**Example:** SYN_D001

## Foreign key

Reference to another table’s key.

**Example:** fact.zone_key

## Cardinality

How many rows relate across tables.

**Example:** many trips to one driver

## Fan-out

A join multiplies one source row.

**Example:** one fare repeated per GPS event

## Reconciliation

Checking that comparable totals agree.

**Example:** 75 trips in Silver and fact

## Weighted average

Average derived from totals and counts.

**Example:** total seconds / total trips

## Snapshot

A fixed table state.

**Example:** versionAsOf

## Feature

An allowed input available at decision time.

**Example:** completed_trips_24h

## Label

Observed target outcome used for learning or evaluation.

**Example:** future trip count when observed

## Prediction cutoff

Time at which a prediction must be formed.

**Example:** 06:05 Riyadh time

## Forecast horizon

Future interval being predicted.

**Example:** 07:00–08:00

## Event time

When the event actually happened.

**Example:** trip end time

## Availability time

When information became usable.

**Example:** scenario delivery timestamp

## Point-in-time correctness

Using only information available at the intended decision.

**Example:** available_at ≤ cutoff

## Leakage

Information that should not be available enters model inputs.

**Example:** future target included in X

## Allowlist

Explicit set of permitted fields.

**Example:** FEATURE_INPUTS

## Null

Explicit missing or unknown value.

**Example:** unobserved target is NULL

## DAG

Directed acyclic graph of dependencies.

**Example:** quality before Gold

## Release manifest

Record identifying all tables in a validated release.

**Example:** release.json

## Failure injection

A deliberate controlled fault used to test recovery.

**Example:** fail after first table

## Logical content hash

Hash of canonical rows, excluding volatile run identity.

**Example:** equal data, different run IDs
