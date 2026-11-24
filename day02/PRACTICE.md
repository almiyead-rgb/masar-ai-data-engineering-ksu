# Day 2: activity and reflection

## Five-minute classroom activity

**Prompt:** Choose the trip business key: driver_id, trip date or trip_id. Explain one collision the wrong key would create.

Work alone for one minute, compare with a partner for two minutes, and explain one choice during the discussion.

<details>
<summary>Activity answer</summary>

Use trip_id. A driver can complete many trips and a date can contain many trips, so neither uniquely identifies a trip.

</details>

## End-of-lab question: one project point

**Silver has 75 trips after three late trips arrive. Will replaying that same late data increase the result to 78?**

Write your first answer in the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields; the reflection cell saves it to `student/day02/REFLECTION.md`. Add one count, value, report field or short code result from your own run as evidence. Then read the model answer and add a correction if needed. Keep both the original attempt and the correction. Explain your own result; do not present a copied model answer as your first attempt.

<details>
<summary>Model answer</summary>

No. Silver stays at 75 because the replay carries the same trip IDs and identical business values. Receipt counts may increase for a new delivery; the business count must not.

</details>

Slides 9–10 contain the activity and answer. Slides 19–20 contain this question and answer. Your explanation and evidence are assessed as part of the 100-point project; the quick activity has no separate mark.

## Optional discussion prompts

The existing prompts below deepen the same labs. They do not create another submission or an additional pass condition.

- How can a duplicate driver key inflate a trip join?
- Which date belongs in a business report and which clock belongs in a freshness check?
- Why can equal totals hide differently assigned city values?
