# Masar dbt · local session

Run the six models, seven singular SQL tests, key/null tests and arrival-time freshness checks through the daily notebook. Read DBT_GUIDE.md for the dependency graph and interpretation.

[Learner guide](../DBT_GUIDE.md) · [Setup and run](../../docs/VERIFICATION.md) · [Runner](../../scripts/run_dbt.py) · [Credential-free profile](profiles/profiles.yml) · [Project specification](design_status.json)

## Use the runner, not a separate CLI process

The registered source tables exist in the live local Spark catalog. Running a separate `dbt build` process would lose that catalog/session. `scripts/run_dbt.py` prepares a safe copy of the verified Day 1 snapshots and invokes dbt serially in the same process. Generated files live under the new course outputs directory, never in this tracked source project.

## Important constraints

Use the pinned Colab environment and its Java 17, Spark 3.5.8 and Delta 3.3.3 requirements. Run the daily notebook in order. The runner copies your Bronze snapshots into an isolated workspace; it does not connect to production. Read [the execution record](../../docs/VERIFICATION.md) for the tested environment.
