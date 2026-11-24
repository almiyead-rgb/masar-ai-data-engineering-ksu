# Learning outcomes and evidence

Each outcome connects to a concept, a practical task and something you can inspect in your project.

| Outcome | Days | Evidence |
|---|---|---|
| **LO1** — Compare warehouses, data lakes and Lakehouse architectures for a stated use case. | 1 | An architecture decision for Masar. |
| **LO2** — Explain compute–storage separation and its effects on cost, elasticity and scale. | 1 | A cost comparison with explicit assumptions. |
| **LO3** — Design an ELT pipeline for a modern cloud data environment. | 2 | Bronze-to-Silver transformations, dbt models and actual test results. |
| **LO4** — Implement Delta Lake tables with ACID transactions and schema enforcement. | 3 | Accepted and rejected writes, revision-aware MERGE and version evidence. |
| **LO5** — Develop streaming and event-driven ingestion patterns. | 4 | Kafka delivery, a Spark checkpoint restart and distinct-event evidence. |
| **LO6** — Apply data-quality, observability and governance controls across a pipeline. | 3, 4, 5 | Quality rejection, quarantine, revalidation, monitoring and governance decisions. |
| **LO7** — Connect Lakehouse products to AI, reporting and analytics consumers. | 5 | A reconciled BI query and time-aware AI feature inputs. |
| **LO8** — Build a working Mini-Lakehouse with Delta Lake and PySpark. | 1, 2, 3, 4, 5 | One cumulative project with restorable state and reproducible outputs. |

## Lab map

| Lab | Day | Contribution | Main evidence |
|---|---:|---|---|
| 01 | 1 | Source inspection and Bronze | Provenance, 144 receipts / 72 trip IDs, student/day01/LAB01_NOTES.md |
| 02 | 1 | Cost assumptions and local scan | Cost interpretation, matched-population timing observations, student/day01/LAB02_NOTES.md |
| 03 | 2 | Staging, Silver and dbt | Types, relationships, five Silver scenarios, four dbt phases, student/day02/LAB03_NOTES.md |
| 04 | 3 | Delta reliability | Correction, rejected write, history and sandbox recovery, student/day03/LAB04_NOTES.md |
| 05 | 4 | Streaming | Kafka receipts, offsets, checkpoint restart and distinct events, student/day04/LAB05_NOTES.md |
| 06 | 4 | Quality and governance | Rejection, seven quarantined rows, revalidated 75, monitoring/ownership, student/day04/LAB06_NOTES.md |
| 07 | 5 | Integrated release | Eight product contracts, controlled failure and recovery, student/day05/LAB07_NOTES.md |
| 08 | 5 | AI/BI consumption and submission | Reconciled query, time-aware features, exports and final README, student/day05/LAB08_NOTES.md |

The five daily assessed answers belong in `student/day01/REFLECTION.md` through `student/day05/REFLECTION.md`. The other lab note files retain the practical evidence for their stages. [Assessment](../assessment/RUBRIC.md) assigns points to demonstrated work; the presence of this map does not itself prove execution.
