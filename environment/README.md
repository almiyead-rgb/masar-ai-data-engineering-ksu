# Your Colab environment

Use **Google Colab with a CPU runtime** for all five days. You do not need a GPU,
a paid LLM API, Docker on your computer, or a cloud database account.

## Prepare once, verify each session

1. Open your daily `dayNN/STUDENT.ipynb` using its Colab link.
2. Choose **Runtime > Change runtime type > CPU**.
3. Select the documented **2026.07 runtime with Python 3.12** when available.
   The first cell refuses unsupported Python versions and explains the change.
4. Run the first setup cell. It checks the pinned packages and prepares Java 17.
5. Review the readiness report. Every required package must match its pin.
6. Mount your own Drive when Colab asks. Keep the continuation archives in
   `MyDrive/Masar_Project`.
7. Continue with the lab cells. Package checks alone do not mean the lab ran.

Colab changes its available runtimes over time. If the named runtime is no
longer available, use an environment explicitly verified in the current course
release. Do not silently upgrade the Spark/dbt stack or use Python 3.13 with
the pinned dbt version.

## What runs inside your notebook?

| Component | Course configuration |
|---|---|
| Python | 3.12; 3.11 retained for compatibility testing |
| Java | 17 |
| PySpark | 3.5.8, local CPU execution |
| Delta Lake | 3.3.3 |
| dbt | Core 1.9.8 and Spark session adapter 1.9.1 |
| Kafka | Official 4.0.2 distribution, local KRaft broker |
| Data quality | Great Expectations 1.7.0 |
| Data | Frozen synthetic `MASAR_SMALL_V1` |

The machine-readable direct pins are in `colab-lock.json` and
`../runtime-target.json`. Read the execution evidence separately to see the
environment in which a particular result was actually produced.

## Daily saving

The final cell creates two files:

- `outputs/dayNN_github.zip`: your reflections, SQL and small observed reports.
- `outputs/dayNN_handoff.zip`: cumulative working data, including Delta logs,
  table files and the separate Day 2 dbt workspace.

The notebook copies these packages to your Drive. A later save preserves the
previous backup under a dated name and updates the ordinary filename to the
latest successful save. Download and unzip the GitHub package, then upload its
folders to the same student repository. Also use **File > Save a copy in GitHub**
to save the notebook you have actually executed, including its outputs.

**A GitHub notebook copy does not include the runtime's Delta files.** Your
handoff archive is what allows the next Colab session to resume the project.

## Recover after a new session

The first cells of Days 2–5 restore the preceding day's handoff from Drive if no
local workspace exists. The restore validates every included file hash before
writing. It refuses to overwrite different existing work. Keep that work and
use a clean project folder if you need to recover from a failed experiment.

For a manually uploaded archive, use the real archive path:

```python
from pathlib import Path
from masar.colab import restore_handoff

restore_handoff(ROOT, Path('/content/day02_handoff.zip'), expected_day=2)
```

Do not run live Delta writes directly on mounted Drive. Work in the local
`/content/masar-project` folder and save the stopped project's archive.

## Day 4: Kafka restart scope

The notebook starts a real broker inside the same Colab VM. It uses loopback
addresses and does not expose a service to the internet. The exercise creates
a new topic, then resumes the query with the same checkpoint across its four
phases. After a VM is deleted, that broker and its offsets are gone. Restore
the retained Day 3 input and rerun Day 4 with a new topic and checkpoint.
Day 5 reads the saved Delta results; it does not need the broker to survive.

## Facilitator execution

For an already provisioned local runner, activate the course Python environment,
select Java 17 with `JAVA_HOME`, and run:

```bash
python scripts/bootstrap_colab.py
python scripts/start_kafka.py start
```

The notebook runner may set `MASAR_NONINTERACTIVE=1` to suppress Drive mounting
and browser downloads. All dependency checks and engine cells still run. This
mode uses the runner's existing course folder so independent attempts remain
separate. It does not turn a local run into hosted-Colab evidence.

## Primary references

- [Colab runtime versions](https://research.google.com/colaboratory/runtime-version-faq.html)
- [Colab storage and runtime lifetime](https://research.google.com/colaboratory/faq.html)
- [Delta and Spark compatibility](https://docs.delta.io/releases/)
- [dbt Python compatibility](https://docs.getdbt.com/faqs/Core/install-python-compatibility)
- [Apache Kafka 4.0 quick start](https://kafka.apache.org/40/getting-started/quickstart/)
