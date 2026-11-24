# Optional container workbench

This folder retains the original Docker workbench for facilitators. The student
course uses [Colab CPU](../../environment/README.md); students do not need Docker.

The [Dockerfile](Dockerfile) uses Python 3.11 and Java 17. Python 3.11 remains an
accepted compatibility runtime; the documented Colab target is Python 3.12.
The [compose file](compose.yaml) separates the source repository, persistent
learner workspace, verification workspace and Kafka storage. Its source mount
is read-only, and Jupyter is exposed on loopback with its normal token
protection.

Container build and offline-execution status are recorded explicitly in
[runtime-target.json](../../runtime-target.json). Do not infer verification
from the presence of these files. See the
[actual execution record](../../docs/VERIFICATION.md) for the environment used
to produce the current course evidence.

If you deliberately choose this optional route, review the compose file before
running it. Keep the Kafka and learner volumes through checkpoint experiments.
A fresh container with a preserved learner volume is different from a fresh
broker with lost offsets; the latter cannot resume an old Kafka checkpoint.
