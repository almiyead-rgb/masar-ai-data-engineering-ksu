# Kafka for the Masar lab

## Your Colab route

The [Day 4 student notebook](../../day04/STUDENT.ipynb) starts a real
**Apache Kafka 4.0.2** broker inside your Colab VM. It downloads the official
archive, checks its SHA-512 checksum and starts a native KRaft process. Docker
is not part of the student setup.

The broker listens on loopback. The exercise creates a two-partition topic,
publishes the fixed synthetic events, and uses a Spark checkpoint to resume
consumption within the same VM. Keep the broker and its storage running until
that restart experiment finishes. The notebook then stops its owned broker
before saving your daily handoff.

The same helper can be called from a prepared local course environment:

```bash
python scripts/start_kafka.py start
python scripts/start_kafka.py stop
```

These commands run from the repository root. See the
[environment guide](../../environment/README.md) for package and Java requirements.
After a Colab VM is deleted, restore Day 3 and rerun Day 4 with a new topic and
checkpoint. Day 5 uses saved Delta results and does not require the old broker.

## Optional original Docker recipe

[compose.yaml](compose.yaml) is retained for a facilitator who already uses
Docker. It exposes Kafka at `127.0.0.1:9092` and keeps broker data in a named
volume. From the repository root:

```bash
docker compose -f infrastructure/kafka/compose.yaml up -d
```

Use one broker at a time. The native helper and this container use the same
loopback port. Keep the named volume while testing checkpoint resume; deleting
it invalidates the broker state associated with the checkpoint. This recipe is
an optional technical alternative, and its presence does not establish that a
container build was verified for the current course revision.

This one-machine teaching configuration is for the supplied synthetic records.
It is not a production Kafka deployment. The
[Apache Kafka 4.0 quick start](https://kafka.apache.org/40/getting-started/quickstart/)
provides the upstream broker documentation.
