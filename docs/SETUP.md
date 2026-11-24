# Run the course in Google Colab

Google Colab is your execution environment for all five days. Keep the complete course repository together because the notebooks share code and the fixed synthetic data.

## 1. Open the daily notebook

Use the **Open in Colab** link on the daily page. If you already saved your notebook to your fork, open that copy instead. Use CPU execution. Begin with `day01/STUDENT.ipynb`, then follow Days 2–5 in order.

## 2. Follow the notebook's setup cells

The setup downloads the course code and installs the versioned environment. The implementation is in [`scripts/bootstrap_colab.py`](../scripts/bootstrap_colab.py), with the environment record in [`environment/colab-lock.json`](../environment/colab-lock.json). Read the displayed version report before starting Spark.

The course targets Python 3.12 and Java 17; a local Python 3.11 route is also supported for verification. If Colab offers a newer Python runtime that the setup does not support, select the documented compatible runtime in **Runtime → Change runtime type**. Do not bypass the version check or independently upgrade Spark, Delta or dbt. The notebook gives the runtime selection currently supported by the pinned environment.

Initial package, JAR and Kafka downloads need internet access. A fresh runtime may need the setup again. Keep the notebook open while it installs and avoid starting a second Spark session in another cell.

## 3. Work locally and keep a recovery copy

Your active data live inside the Colab runtime's local workspace. At the end of each day, the save step creates `outputs/dayNN_handoff.zip`. Save that archive to your course folder on Drive. At the start of a fresh session, restore it using the notebook's restore step before continuing.

Do not run live Delta-table writes directly against a mounted Drive folder. Use the local workspace, then copy the completed archive after writes have stopped. The archive preserves Delta data and transaction logs, reports, project pointers and the cumulative dbt evidence needed to continue.

## 4. Day 4 starts Kafka inside the runtime

The notebook starts the supplied Kafka distribution as a local Java process, checks readiness, and runs the event experiment. You do not need Docker or a broker on your laptop. Read [Day 4 setup](../day04/SETUP.md) for its restart boundary.

## 5. Save two different things

- Save the executed notebook to GitHub using **File → Save a copy in GitHub**. Verify that cell outputs are retained.
- Run the daily export step. Upload the small files from `outputs/dayNN_github.zip` to the same repository. Keep `outputs/dayNN_handoff.zip` on Drive for resuming data state.

[Daily saving instructions](GIT_WORKFLOW.md) explain the exact sequence. A GitHub notebook save does not automatically save other files created in the Colab runtime.

## If setup stops

Read the first failing message and the runtime report. Follow [troubleshooting](TROUBLESHOOTING.md). If a fresh runtime is needed, restore your own last successful handoff. Keep your original source files and saved GitHub work.

For the environment actually used to produce the published comparison outputs, read [execution evidence](VERIFICATION.md). A compatible configuration and a successful hosted Colab test are separate claims.

## Primary references

[Colab FAQ](https://research.google.com/colaboratory/faq.html) · [Colab runtime versions](https://research.google.com/colaboratory/runtime-version-faq.html) · [Delta/Spark compatibility](https://docs.delta.io/releases/) · [Kafka quick start](https://kafka.apache.org/40/getting-started/quickstart/)
