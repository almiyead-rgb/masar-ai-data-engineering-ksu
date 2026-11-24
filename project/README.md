# Masar: your cumulative Mini-Lakehouse project

## Business problem

A fictional transport company receives trip files, driver records and location events. Repeated deliveries can inflate its reports. Late trips can leave a reporting day incomplete. Corrections can change an approved fare. Defective values can reach an analyst, and data that arrived later can accidentally enter an earlier AI decision.

You build a traceable data pipeline that makes those situations visible and handles them explicitly. The business outputs are consistent trip counts and fares, understandable city/driver summaries, and historical feature inputs with a clear decision-time boundary.

## Technical solution

- **Bronze:** preserve original deliveries and provenance.
- **Silver:** create typed, linked business records using explicit keys and revision rules.
- **Delta Lake:** enforce table contracts, apply approved corrections and retain version evidence.
- **dbt:** express transformations and dependencies, run tests and retain generated documentation.
- **Kafka and Spark:** receive actual event messages and demonstrate a compatible query restart.
- **Great Expectations:** validate candidates, block unsafe promotion, quarantine defects and revalidate.
- **Gold and consumers:** produce eight defined data products, reconcile a BI query and inspect suitable historical AI inputs.

The supplied dataset is synthetic and deliberately small. You are building an instructional Mini-Lakehouse, not a deployed transport service or evidence of production-scale capacity. Read [the data dictionary](../data/DICTIONARY.md) before interpreting a field.

## What grows each day

| Day | New stage | What continues |
|---|---|---|
| 1 | Architecture, source checks, Bronze and cost evidence | Original receipt history |
| 2 | Staging, Silver, late-arrival handling and dbt | One trusted record per trip plus transformation evidence |
| 3 | Corrections, constraints, history and safe recovery | Corrected Silver |
| 4 | Streaming, quality, observability and governance | Approved trips and distinct events |
| 5 | Gold, AI/BI, release recovery and export | The complete project and its cumulative evidence |

Labs 03 and 04 each have two teaching parts; they remain single numbered labs. Labs 01–08 together are your final project. You do not start a separate assignment on Day 5.

## Your deliverables

Keep your executed daily notebooks, small student-authored code/SQL tasks, eight lab note files, architecture decisions, cost/scan observations, governance decisions, stage reports and final exports. Complete `student/PROJECT_README.md` from the [README template](../templates/PROJECT_README.md) to explain your implementation and results. Link it from your repository's root `README.md`. The notebook creates the templates safely and the daily save includes the `student/` folder.

[Learning-to-evidence map](../docs/ALIGNMENT.md) · [100-point rubric](../assessment/RUBRIC.md) · [Final submission](SUBMISSION.md)
