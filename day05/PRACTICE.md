# Day 5: activity and reflection

## Five-minute classroom activity

**Prompt:** At a decision cutoff, which input is valid: completed trips already available in the past 24 hours, or the actual trip count in the next hour?

Work alone for one minute, compare with a partner for two minutes, and explain one choice during the discussion.

<details>
<summary>Activity answer</summary>

Use the completed trips whose source data was available by the cutoff. The actual future-hour count is a future label, not an input available at prediction time.

</details>

## End-of-lab question: one project point

**bi.fact_trips has 75 rows, but ai.zone_hourly_features has three. Does that mean 72 trips were lost?**

Write your first answer in the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields; the reflection cell saves it to `student/day05/REFLECTION.md`. Add one count, value, report field or short code result from your own run as evidence. Then read the model answer and add a correction if needed. Keep both the original attempt and the correction. Explain your own result; do not present a copied model answer as your first attempt.

<details>
<summary>Model answer</summary>

No. The products have different grain and time windows. The fact table has one row per trip; features have one row per city, cutoff and prediction horizon, using only eligible historical data.

</details>

Slides 9–10 contain the activity and answer. Slides 19–20 contain this question and answer. Your explanation and evidence are assessed as part of the 100-point project; the quick activity has no separate mark.

## Optional discussion prompts

The existing prompts below deepen the same labs. They do not create another submission or an additional pass condition.

- Why aggregate GPS events before joining to fares?
- Why is an unknown future target different from an observed zero?
- What does the local release pointer protect, and what does it not coordinate?
