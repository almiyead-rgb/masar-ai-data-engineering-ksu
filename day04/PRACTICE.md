# Day 4: activity and reflection

## Five-minute classroom activity

**Prompt:** Two Kafka messages have different offsets but the same event_id and identical payloads. How many deliveries and business events do they represent?

Work alone for one minute, compare with a partner for two minutes, and explain one choice during the discussion.

<details>
<summary>Activity answer</summary>

They represent two deliveries and one distinct business event. Transport offsets identify records in a partition; event_id identifies the business event.

</details>

## End-of-lab question: one project point

**A candidate contains 82 rows and fails because seven are invalid. How can you safely use the other 75?**

Write your first answer in the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields; the reflection cell saves it to `student/day04/REFLECTION.md`. Add one count, value, report field or short code result from your own run as evidence. Then read the model answer and add a correction if needed. Keep both the original attempt and the correction. Explain your own result; do not present a copied model answer as your first attempt.

<details>
<summary>Model answer</summary>

Block the failed candidate, quarantine the seven rows with reasons, create a clean 75-row candidate, and run the quality gate again before approving it.

</details>

Slides 9–10 contain the activity and answer. Slides 19–20 contain this question and answer. Your explanation and evidence are assessed as part of the 100-point project; the quick activity has no separate mark.

## Optional discussion prompts

The existing prompts below deepen the same labs. They do not create another submission or an additional pass condition.

- What does the Kafka offset identify?
- How does Spark streaming progress differ from a GX Checkpoint?
- Why is an old event not automatically invalid?
