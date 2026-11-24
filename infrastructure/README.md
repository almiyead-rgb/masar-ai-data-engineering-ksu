# Optional local infrastructure

Your required learning environment is [Google Colab CPU](../environment/README.md).
The five student notebooks prepare Java and the pinned Python packages, run
Spark locally, and start native Kafka only for Day 4.

The files in this directory preserve the original local technical alternatives:

| Folder | Purpose |
|---|---|
| [kafka](kafka/README.md) | Optional Docker broker recipe for a prepared local machine |
| [runtime](runtime/README.md) | Optional container workbench and separate verification volume |

Use the [runtime specification](../runtime-target.json) and
[execution record](../docs/VERIFICATION.md) to distinguish a supported version
from a configuration that was actually tested. A Docker recipe is not evidence
of a successful container build.
