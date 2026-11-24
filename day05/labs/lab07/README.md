# Lab 07 · Build Gold and recover a usable release

[Day 5](../../README.md) · **[Daily notebook](../../STUDENT.ipynb)** · [Walkthrough](WALKTHROUGH.md)

## Your contribution to the project

Use Day 4's approved trips and distinct events to build the eight contracted Delta products. Keep the last good release selected when a new candidate deliberately fails, then rebuild and compare the business contents.

This is Lab 07 of your existing project. Run the setup cell and the **07** cell in the daily notebook; its helper performs the good/fail/rebuild sequence. Do not create another notebook or manually repeat each internal operation.

## Inputs and evidence

Inputs: the successful workspace, Day 4 stream/quality reports, 75 approved trips totaling SAR 1,880.60, and 217 distinct events. Read the recorded Delta paths, not the contaminated candidate or raw event receipts.

Evidence: the two successful release manifests, the deliberately failed candidate's report, the latest-release pointer and `reports/day05_recovery.json`. Four recovery checks must pass. The data release is local; nothing is deployed to an external service by this lab.

## Read and continue

[Concepts](../../CONCEPTS.md) · [Table contracts](../../DATA_PRODUCTS.md) · [Steps and actual reports](WALKTHROUGH.md) · [Integration boundaries](../../INTEGRATION.md).

Record the product grains, selected input versions and recovery evidence in `student/day05/LAB07_NOTES.md`. Use [the daily practice](../../PRACTICE.md), then continue to [Lab 08](../lab08/README.md). The [calculation reference](../../REFERENCE.ipynb) is optional and does not replace Delta execution.
