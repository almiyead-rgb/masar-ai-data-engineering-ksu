# Masar
## Modern Data Engineering for AI Systems

**SDA-DSC-214 · King Saud University students · Instructor: Meaad Al-Marri**

Build one Mini-Lakehouse across five evenings. You will keep raw data, produce trusted trip records, apply corrections, ingest events, reject defective data and serve AI/BI consumers. Run every lab in **Google Colab** and save your work to **your own GitHub repository each day**.

[Open the learning portal](https://almiyead-rgb.github.io/masar-ai-data-engineering-ksu/) · [Start here](docs/START_HERE.md) · [Project brief](project/README.md) · [Compare results](docs/EXPECTED_OUTPUTS.md) · [Submit your project](project/SUBMISSION.md)

## Your five-day route

| Day | What you add to your project | Labs | Slides | Colab |
|---|---|---|---:|---|
| [1](day01/README.md) | Architecture, source evidence and Bronze | 01 + 02 | [20](slides/day01.md) | [Open Day 1](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day01/STUDENT.ipynb) |
| [2](day02/README.md) | ELT, trusted Silver and dbt | 03 | [20](slides/day02.md) | [Open Day 2](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day02/STUDENT.ipynb) |
| [3](day03/README.md) | Delta corrections, constraints and history | 04 | [20](slides/day03.md) | [Open Day 3](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day03/STUDENT.ipynb) |
| [4](day04/README.md) | Kafka, quality, observability and governance | 05 + 06 | [20](slides/day04.md) | [Open Day 4](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day04/STUDENT.ipynb) |
| [5](day05/README.md) | Gold, AI/BI, recovery and final delivery | 07 + 08 | [20](slides/day05.md) | [Open Day 5](https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/day05/STUDENT.ipynb) |

Each evening runs **17:00–21:00, Asia/Riyadh**: 150 minutes of explanation and demonstrations, one 60-minute lab, and two 15-minute prayer breaks. The instructor adjusts both prayer-break positions for the actual course dates. This gives 20 scheduled hours and 17.5 learning hours. Activities, questions and answers are included in the 20 slides for each day.

## What you will build

Masar uses a small, fixed, synthetic dataset for a fictional transport company. Repeated deliveries, late records and approved corrections make its reports disagree unless the pipeline handles them explicitly. Your project uses **PySpark, Delta Lake, dbt, Kafka and Great Expectations** to produce traceable tables and reusable analytics inputs.

The final products reconcile **75 trips, SAR 1,880.60 and 217 distinct location events**. You also create three historical AI-feature rows; unobserved future labels remain `NULL`. These are expected values for this training fixture, not operational statistics or a trained-model result. [Read the output contracts](day05/DATA_PRODUCTS.md).

## How you work every day

1. Read the day's concepts and watch the demonstration.
2. Open the daily notebook in Colab and restore your previous state when needed.
3. Complete the small code/decision tasks, run the real components and inspect their outputs.
4. Write your answer before revealing the model answer; add an observed result as evidence.
5. Save the executed notebook, your notes and small reports to GitHub. Keep the full handoff archive on Drive for the next session.

A notebook save does not back up all files in the Colab runtime. Follow the [daily GitHub and Drive workflow](docs/GIT_WORKFLOW.md).

## Assessment and certificates

Your cumulative project is marked **out of 100**. **Attend all five days and earn at least 70 points to pass.** If you attend all five days but do not submit a project, or score below 70, you receive an **attendance certificate only**. A project awaiting assessment remains pending. Fewer than five attended days does not meet the completion requirement; the organizer confirms any attendance-certificate eligibility for that case.

[Project rubric](assessment/RUBRIC.md) · [Certificate policy](assessment/CERTIFICATES.md) · [Learning outcomes and evidence](docs/ALIGNMENT.md)

## Compare evidence accurately

[Expected outputs](docs/EXPECTED_OUTPUTS.md) describe the fixed scenario. [Execution evidence](docs/VERIFICATION.md) states which environment actually ran the code. Compare your own saved results with both. Different timings, session paths and run IDs are normal; counts, business values and rejection decisions must satisfy their contracts.

## Course credit

Developed for **Modern Data Engineering for AI Systems (SDA-DSC-214)**, with course materials by **Meaad Al-Marri**, based on [the original Masar repository](https://github.com/almiyead-rgb/masar-modern-data-engineering). Preserve this attribution in your project. Include [SDAIA Academy](https://github.com/SDAIAAcademy) and `#SDAIAAcademy` in your final README and submission message.

[Data dictionary](data/DICTIONARY.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) · [Primary sources](docs/SOURCES.md)
