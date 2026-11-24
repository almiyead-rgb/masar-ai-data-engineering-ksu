# Execution status

Read the [execution record](docs/VERIFICATION.md) and its
[machine-readable evidence](docs/verification.json) to see which revision,
environment and complete course runs were actually verified.

Your five daily [student notebooks](docs/START_HERE.md) run real PySpark,
Delta Lake, dbt, Kafka and Great Expectations operations. Saved notebook outputs
show a recorded run; run the cells yourself and retain your own observed results.
The [fixed expected results](docs/EXPECTED_OUTPUTS.md) explain the business values to
compare. Timing samples, local paths, run IDs and transaction versions can vary.

## What each check establishes

| Check | What it establishes |
|---|---|
| `python scripts/check_repository.py` | The five-day course structure, learning resources, data integrity, 20 slides per day and links are consistent. It makes no execution claim. |
| `python scripts/check_repository.py --release` | The required two independent complete course executions and their saved notebook evidence pass the release checks. |
| Your daily notebook | Your current environment produced the tables, reports and comparison metrics you submit. |

A `published` flag is a publication setting. It cannot establish that a notebook
was executed. Local native execution also does not establish that a run took
place on Google's hosted Colab service; the evidence records that distinction.

Use the [Colab environment guide](environment/README.md) for setup and the
[daily save instructions](docs/GIT_WORKFLOW.md) for notebook, GitHub and Drive
handoff steps.
