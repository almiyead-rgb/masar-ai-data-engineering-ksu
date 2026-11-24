# Day 4 · Primary references

[Day 4](README.md) · [Concepts](CONCEPTS.md) · [Setup](SETUP.md)

## Use the documented course versions

The course pins Java 17, Spark 3.5.8, Delta 3.3.3, Kafka 4.0.2, kafka-python 2.2.15 and GX 1.7.0. Read the runtime record for the Python version actually exercised. Read [Day 4 evidence](verification.json) and [the course execution record](../docs/VERIFICATION.md). Live documentation may show newer releases; do not upgrade the exercise or copy newer API syntax without retesting.

Counts, fares, quality rules and freshness examples come from the unchanged [Masar synthetic dataset](../data/DICTIONARY.md) and the supplied implementation. The optional reference explains arithmetic; the [student notebook](STUDENT.ipynb) contains the native execution outputs.

## S1 · [Spark 3.5.8 Kafka integration](https://spark.apache.org/docs/3.5.8/structured-streaming-kafka-integration.html)

Message fields, starting offsets, checkpoint behavior and connector coordinates.

## S2 · [Structured Streaming guide](https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html)

AvailableNow, query identities, progress, recovery and the separate concept of watermarks.

## S3 · [Delta streaming reads and writes](https://docs.delta.io/delta-streaming/)

Delta as a streaming sink and checkpoint-related writing behavior.

## S4 · [Apache Kafka 4.0 quick start](https://kafka.apache.org/40/getting-started/quickstart/)

Use the supplied notebook setup for the local Java-process broker in Colab. The official guide documents native startup from downloaded files.

## S5 · [kafka-python 2.2.15 producer API](https://kafka-python.readthedocs.io/en/2.2.15/apidoc/KafkaProducer.html)

Sending, acknowledgments, retries and idempotence in the pinned producer client.

## S6 · [GX dataframe connections](https://docs.greatexpectations.io/docs/core/connect_to_data/dataframes/)

Data source, asset and batch definitions for an in-memory snapshot. The course uses Pandas for the bounded quality snapshot.

## S7 · [GX Checkpoints and actions](https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions/)

Validation definitions and actions; not Spark streaming progress.

## S8 · [GX Data Docs](https://docs.greatexpectations.io/docs/core/configure_project_settings/configure_data_docs/)

Local documentation and retained validation results.

## S9 · [GX 1.7.0 source](https://github.com/great-expectations/great_expectations/tree/1.7.0)

Pinned implementation reference when current online documentation differs from this exercise.

## S10 · [SDAIA · Personal Data Protection Law](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL)

Official reference for a real-data context; the synthetic lab is not a compliance certification.

## S11 · [SDAIA · Implementing Regulation](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL 2)

Read alongside the applicable organizational policies for real deployments.

## S12 · [SDAIA · Data destruction and de-identification guidance](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PersonalDataDestruction)

Reference for discussing retention and data handling beyond the synthetic exercise.

## S13 · [Kafka 4.0 producer settings](https://kafka.apache.org/40/configuration/producer-configs/)

Acknowledgments and idempotence semantics. Client-specific option names are documented in S5.

## S14 · Colab runtime persistence

[Colab FAQ](https://research.google.com/colaboratory/faq.html). Preserve the same broker/topic and compatible Spark checkpoint for the within-session resume exercise. After runtime deletion, restore Day 3 and start a new Day 4 experiment.
