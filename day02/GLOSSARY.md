# Day 2 · Glossary and pronunciation

[Course home](../README.md) · [Execution record](../STATUS.md)

## How to use this page

Pronunciation is an approximate Arabic aid, not a phonetic standard. Relate each term to the same Masar pipeline.

## ETL

Extract, transform, then load.

## ELT

Extract, load, then transform in the target environment.

## Grain

What exactly one row represents.

## Business key

Stable identity of a business record; trip_id here.

## Staging

A first, source-oriented transformation layer.

## Conformed data

Data with agreed names, types and meanings.

## Schema

Field names and data types.

## Decimal

Fixed-precision decimal number used here for fare.

## UTC

Common time reference; business date may still be local.

## Time zone

Rules for relating local time to a time reference.

## Join

Combine related rows using a key.

## Left-anti join

Return left rows that have no right-side match.

## Cardinality

The number and multiplicity of relationships.

## Deduplication

Remove repeated business records under a documented rule.

## Deterministic

The same inputs and rule produce the same content.

## Idempotency

Repeating an operation preserves its intended result.

## Incremental load

Process additions or changes rather than replacing everything.

## MERGE

Match source and target keys to apply specified actions.

## Late arrival

Data arrives after its expected processing window.

## Backfill

Reprocess a defined historical interval.

## Lineage

Trace a result to its inputs and transformations.

## Freshness

How recently relevant data arrived under a defined clock.

## dbt source

Reference to a declared existing source relation.

## dbt ref

Reference that connects one model to another.
