# Day 4: Kafka inside Colab

## Before you start

Restore the successful Day 3 state. It must contain 75 corrected trips with SAR 1,880.60 in fares. Use the same course setup and fixed data as the earlier days.

The notebook starts the pinned Kafka distribution as a local Java process inside your Colab runtime. Spark and Kafka run in that same runtime. You do not need Docker, a broker on your laptop, a paid event service or a public endpoint.

## Startup sequence

1. Run the notebook setup and inspect the Python/Java/package report.
2. Run its Kafka preparation cell. It downloads the pinned distribution when needed, prepares the local broker and waits for a readiness check.
3. Read the broker readiness result before running the streaming experiment.
4. Run Lab 05, inspect all four phases, then run Lab 06 and its quality results.
5. Complete the small student tasks and save the notebook, evidence bundle and handoff.

The local broker endpoint is `127.0.0.1:9092` inside the Colab runtime. It does not refer to your laptop. Keep the course broker local; the lab does not require opening a router port or creating a tunnel.

## What the restart experiment proves

The supplied streaming experiment stops and restarts a compatible query using the same checkpoint, destination and source topic within the session. With no new messages, the restart leaves 216 receipts and 216 distinct events. The next phases deliver duplicate messages and one late new event.

If the entire runtime is deleted, its broker/topic state is lost. Restore the end of Day 3 and begin a new Day 4 experiment with a fresh source/checkpoint namespace. Do not connect an old checkpoint to a recreated empty topic and call that a successful resume.

Re-running the full streaming cell begins another experiment. It is different from the controlled stop/restart inside that cell. Use the printed workspace and report paths to keep attempts separate.

## Common startup problems

| Problem | Next action |
|---|---|
| Download failed | Read the network error and retry preparation when connectivity returns |
| Java is unsupported | Rerun the documented environment setup before starting Kafka or Spark |
| Readiness check times out | Inspect the broker log printed by setup; retain the first error |
| Port already in use | Use the provided broker lifecycle helper to inspect/stop the stale course process, then rerun preparation |
| Old checkpoint with a new broker | Restore Day 3 and start a clean Day 4 experiment |

The handoff saves the approved Delta outputs and reports required by Day 5. It does not preserve a running broker process. Day 5 consumes saved tables and does not require the old Kafka service.

[Colab setup](../docs/SETUP.md) · [Kafka official quick start](https://kafka.apache.org/40/getting-started/quickstart/) · [Spark Kafka integration](https://spark.apache.org/docs/3.5.8/structured-streaming-kafka-integration.html) · [Execution record](../docs/VERIFICATION.md)
