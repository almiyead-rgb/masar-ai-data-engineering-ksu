# Project rubric: 100 points

Your project is the work you build during Labs 01–08. You receive points for the part you complete, supported by your own code, observed outputs and explanation. Attendance is a separate completion condition.

| Criterion | Points | How points are allocated |
|---|---:|---|
| Business problem, architecture and cost | 10 | Explain the problem (2), compare architectures (3), explain compute/storage and cost (3), show the architecture (2). |
| Bronze, ELT, Silver and dbt | 20 | Raw/source evidence (5), types and relationships (5), duplicates and late arrivals (5), actual dbt models and tests (5). |
| Delta reliability and corrections | 15 | Real Delta transactions (3), rejected write evidence (4), revision-aware correction/replay (4), history and recovery (4). |
| Event ingestion | 10 | Actual Kafka producer/consumer evidence (4), checkpoint restart (3), interpretation of delivery, event identity and lateness (3). |
| Quality, observability and governance | 15 | GX quality gate (5), quarantine and revalidation (4), operational observations (3), ownership/lineage/access/retention decisions (3). |
| Gold, AI and BI consumers | 15 | Product contracts and grain (4), BI reconciliation (4), time-aware AI inputs (5), unknown versus zero (2). |
| Integration, reproducibility and documentation | 10 | Dependency order (4), state save/restore (2), failed-candidate recovery (2), README and final version (2). |
| Five daily evidence-based answers | 5 | One point per day for your explanation connected to an observed result. |
| **Total** | **100** | |

## How evidence is assessed

- **Full points for a sub-item:** the required behavior works, your output provides relevant evidence, and your explanation correctly connects it to the project.
- **Partial points:** award the completed portion when evidence or interpretation is incomplete. Record what was achieved and what is missing.
- **No points for an unperformed sub-item:** a copied expected number, a fabricated output or an unchanged placeholder does not show execution.
- A green `PASS` label alone does not prove the required component ran. Check the report scope, notebook outputs and relevant files.
- Matching outputs across students are normal because the fixture is fixed. Review each student's small code task and explanation, not just whether values differ.
- The daily questions are learning reflections. Write your initial answer before viewing the model answer, then keep your correction if needed. One point is available per day for a clear evidence-based explanation.
- Quick classroom activities are formative and do not add marks outside the 100-point project.
- Optional extensions, repository stars, a public social-media post or paid services are not additional pass requirements.

The criteria have no hidden minimum score per section. Apply the total project score and the [announced attendance/certificate policy](CERTIFICATES.md). Record final marks in the organizer's private assessment system, not in the public site.

## Reviewer record

For each criterion record: awarded points, evidence location, one strength and one correction if needed. Check that the total is between 0 and 100. State whether the project has been assessed or remains pending. An automated packaging check can help identify missing files, but it does not award a grade or verify attendance.
