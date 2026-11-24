export const REPO = 'https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu';
export const gitFile = (path) => `${REPO}/blob/main/${path}`;
export const gitFolder = (path) => `${REPO}/tree/main/${path}`;
export const notebook = (day) => `day${String(day).padStart(2, '0')}/STUDENT.ipynb`;
export const colab = (day) => `https://colab.research.google.com/github/almiyead-rgb/masar-ai-data-engineering-ksu/blob/main/${notebook(day)}`;
export const dayId = (day) => `day${String(day).padStart(2, '0')}`;

export const STAGES = ['Bronze', 'Silver', 'Delta', 'Streaming & quality', 'Gold & delivery'];
export const DAILY = [
  {
    number: 1, eyebrow: 'Architecture / raw data', summary: 'Keep an honest record of what arrived.',
    business: 'A delivery is not always a new trip. Preserve the raw inputs before you make decisions about business records.',
    before: 'Complete the setup checklist. Start with the unchanged MASAR_SMALL_V1 synthetic dataset.',
    mission: 'Inspect the source files, create Bronze Delta tables, and explain why receiving the trips file twice doubles receipts but not unique trips.',
    steps: ['Verify the dataset manifest and inspect the trip, driver, and location files.', 'Run the Bronze ingestion cells and inspect the source and batch metadata.', 'Run the intentional redelivery scenario. Compare all receipts with distinct trip IDs.', 'Compare the cost scenarios and equal-result scan checks. Record your assumptions.'],
    task: 'Write down the business key you would use for trips. Explain why preserving repeated deliveries in Bronze can be useful.',
    code: 'bronze_trips.select("trip_id").distinct().count()',
    codeNote: 'Read the corresponding table into bronze_trips in the notebook. A distinct business key answers a different question from the total receipt count.',
    checks: [{label:'Trip receipts after redelivery', value:144}, {label:'Distinct trip IDs', value:72}],
    evidence: ['Executed Day 1 notebook', 'Bronze checks and cost observations', 'student/day01/LAB01_NOTES.md and student/day01/LAB02_NOTES.md', 'student/DECISIONS.md, student/BENCHMARKS.md, and student/day01/REFLECTION.md'],
    artifact: 'Bronze tables and a documented architecture decision',
  },
  {
    number: 2, eyebrow: 'ELT / trusted records', summary: 'Turn repeated inputs into one reliable trip table.',
    business: 'Late trips should complete a report. Replaying the same delivery should not inflate it.',
    before: 'Restore your own Day 1 handoff. The workspace must include its Delta data and metadata, not just a pointer file.',
    mission: 'Standardize the raw data, build Silver, include the late trips, and run the dbt models and their tests.',
    steps: ['Inspect the types, timestamps, city labels, and driver relationships.', 'Build Silver using trip_id and the documented precedence rules.', 'Process the three late trips, then replay the same delivery and compare results.', 'Run the dbt section in the same notebook and keep its models, tests, and reports.'],
    task: 'Identify the trip key and complete the notebook check that proves replay does not increase the unique trip count.',
    code: 'silver_trips.select("trip_id").distinct().count()',
    codeNote: 'The reference scenario finishes with 75 unique trips. Inspect the notebook’s fare reconciliation as well as its row counts.',
    checks: [{label:'Unique Silver trips', value:75}, {label:'Total fares (SAR)', value:1875.60}],
    evidence: ['Executed Day 2 notebook', 'Silver scenario report', 'dbt SQL and test results', 'student/day02/LAB03_NOTES.md and student/day02/REFLECTION.md'],
    artifact: 'Typed Silver data, dbt transformations, and replay evidence',
  },
  {
    number: 3, eyebrow: 'Transactions / change control', summary: 'Correct a value without losing the history.',
    business: 'A correction must update the approved value once, even when the same correction is delivered again.',
    before: 'Restore Day 2 with 75 unique trips and SAR 1,875.60 in fares. Keep the separate dbt evidence.',
    mission: 'Apply a revision-aware fare correction. Test rejection, replay, historical reads, and safe recovery.',
    steps: ['Read the source revision rules and apply the approved correction.', 'Repeat the correction, then inspect the result of older or conflicting input.', 'Observe an intentionally rejected write and verify that the trusted table remains intact.', 'Read an earlier table version and perform maintenance on the isolated training copies.'],
    task: 'Explain why source_revision and a Delta table version are different. Identify the condition that allows a newer correction.',
    code: 'corrected_trips.filter("trip_id = \'SYN_T0001\'").select("fare_sar").show()',
    codeNote: 'SYN_T0001 changes from SAR 18.00 to SAR 23.00. Replaying the approved correction must leave it at SAR 23.00.',
    checks: [{label:'Unique trips', value:75}, {label:'Total fares (SAR)', value:1880.60}, {label:'Corrected fare (SAR)', value:23}],
    evidence: ['Executed Day 3 notebook', 'Correction and rejection evidence', 'Version and recovery observations', 'student/day03/LAB04_NOTES.md and student/day03/REFLECTION.md'],
    artifact: 'Corrected Delta data and an auditable change history',
  },
  {
    number: 4, eyebrow: 'Events / trust', summary: 'Receive events. Stop unsafe data.',
    business: 'Transport messages can repeat. Bad records must be visible and explainable before downstream users rely on them.',
    before: 'Restore Day 3 with 75 trips and SAR 1,880.60. Start the local Kafka broker from the notebook setup.',
    mission: 'Read Kafka events into Delta, test a restart, and use Great Expectations to quarantine and revalidate data.',
    steps: ['Run the Kafka producer and Spark streaming cells. Inspect acknowledgements and offsets.', 'Restart the query with the same checkpoint while the broker and topic remain available.', 'Compare message receipts with distinct event IDs.', 'Run the 82-row quality scenario, inspect the seven rejected rows, then revalidate the clean 75-row candidate.'],
    task: 'Choose a quality rule and explain a rejected record. State which monitoring signal would help you notice the problem.',
    code: 'approved_trips.count()  # Inspect the validation report before approving data.',
    codeNote: 'A failed mixed candidate is an expected test. Approval requires a new validation of the cleaned candidate.',
    checks: [{label:'Message receipts', value:219}, {label:'Distinct events', value:217}, {label:'Quarantined rows', value:7}, {label:'Revalidated trip rows', value:75}],
    evidence: ['Executed Day 4 notebook', 'Streaming and restart report', 'GX validation and quarantine reasons', 'student/day04/LAB05_NOTES.md, student/day04/LAB06_NOTES.md, and student/day04/REFLECTION.md', 'student/GOVERNANCE.md'],
    artifact: 'Distinct events and a quality-approved trip table',
  },
  {
    number: 5, eyebrow: 'Data products / delivery', summary: 'Make the data useful, then submit the evidence.',
    business: 'Reporting and AI consumers need consistent, well-defined inputs with a clear account of when the information was available.',
    before: 'Restore the approved Day 4 trips and 217-event Delta table. Day 5 reads the saved data without requiring the old Kafka broker.',
    mission: 'Build eight serving products, reconcile a BI query, inspect historical AI features, and deliver the same cumulative project.',
    steps: ['Read the grain and key of each data product before building it.', 'Create the serving release and verify that a failed candidate does not replace the last usable release.', 'Run the BI consumer and reconcile the totals. Inspect feature availability at the fixed cutoff.', 'Export the products, complete student/PROJECT_README.md, link it from your root README, and submit your repository and final commit.'],
    task: 'Explain one difference in row counts between a fact table and a feature table. Keep unobserved future labels separate from historical inputs.',
    code: 'fact_trips.selectExpr("count(*) AS trips", "sum(fare_sar) AS total_fares").show()',
    codeNote: 'Aggregate or count location events before joining them to trips, so the join does not multiply fares.',
    checks: [{label:'Serving products', value:8}, {label:'BI trips', value:75}, {label:'Total fares (SAR)', value:1880.60}, {label:'AI feature rows', value:3}],
    evidence: ['All five executed notebooks', 'Eight serving exports and their definitions', 'student/day05/LAB07_NOTES.md, student/day05/LAB08_NOTES.md, and student/day05/REFLECTION.md', 'student/PROJECT_README.md linked from your root README', 'Repository URL, branch, and commit SHA'],
    artifact: 'A complete Mini-Lakehouse with AI and BI consumers',
  }
];
export const PRODUCTS = [
 ['gold.zone_hourly_demand','Observed city and trip-start hour',75],
 ['gold.driver_daily','Driver and local trip-start date',18],
 ['bi.dim_zone','City proxy',3],
 ['bi.dim_driver','Synthetic driver',6],
 ['bi.dim_date','Observed local date',3],
 ['bi.fact_trips','Unique trip',75],
 ['ai.zone_hourly_features','City, cutoff, and prediction hour',3],
 ['ai.zone_hourly_labels','City and prediction hour; future label status',3]
];
export const GLOSSARY = [
 ['ACID','Atomicity, consistency, isolation, and durability. Properties that help transactions behave reliably.'],
 ['Bronze','The raw receipt layer. Keep the source data and the metadata needed to explain how it arrived.'],
 ['Silver','A typed and conformed layer with one accepted business record per documented key.'],
 ['Gold','Data products designed for specific reporting, analytics, or AI consumers.'],
 ['Lakehouse','An architecture that combines open data storage with table management and analytical processing.'],
 ['ELT','Extract, load, then transform. Transformations happen after the source data has been loaded.'],
 ['Business key','The identifier used to decide whether two records describe the same business object.'],
 ['Idempotency','Repeating the same logical input leaves the intended business result unchanged.'],
 ['Delta Lake','A table format with a transaction log that supports reliable reads, writes, and table history.'],
 ['Schema enforcement','Checking that incoming data matches the table’s accepted structure and types.'],
 ['MERGE','A table operation that matches source and target records and applies specified updates or inserts.'],
 ['Source revision','A version assigned by the source to a business record. It is not the Delta table version.'],
 ['Checkpoint','Progress and state used by a streaming query to resume with compatible inputs and settings.'],
 ['Kafka offset','A message’s position in a Kafka partition. It is not the business identity of the event.'],
 ['Event time','When the event happened, as recorded by the source.'],
 ['Arrival time','When a system received a record or delivery.'],
 ['Quarantine','A separate location for rejected records and the reasons they failed a quality rule.'],
 ['Quality gate','A check that must pass before a candidate dataset is approved for downstream use.'],
 ['Observability','Evidence about data and pipeline health, such as freshness, volume, quality, and failures.'],
 ['Lineage','A record of which sources and transformations produced a dataset or result.'],
 ['Grain','What one row represents, such as one trip or one driver on one day.'],
 ['Feature leakage','Using information in a model input that was not available at the intended decision time.'],
 ['NULL','An absent or unknown value. Its meaning must be explained by the data contract; it is not automatically zero.'],
 ['Data contract','The agreed meaning, keys, fields, types, units, and quality expectations of a data product.'],
 ['Commit','A saved version of your repository files with an identifier and a message.'],
 ['Handoff archive','A saved project snapshot used to continue your work in a new runtime session.']
];
export const HELP = [
 {q:'Which environment should I use?',a:'Use Google Colab for all five daily notebooks. Follow the environment selection and setup steps in the notebook before running the lab. Use a CPU runtime; the course does not require a GPU.'},
 {q:'I saved the notebook. Why are my Delta tables missing?',a:'A notebook file does not contain every file created by its runtime. Restore your own dayNN_handoff.zip from Drive. It must include the Delta data and logs, not just the notebook or a pointer JSON.'},
 {q:'My output differs from the example. What should I compare first?',a:'Check the day, dataset version, input handoff, and the scenario you just ran. Compare stable row counts and totals. Runtime duration, session paths, and run identifiers can differ naturally.'},
 {q:'The quality check says FAILED. Is the lab broken?',a:'The 82-row mixed candidate in Day 4 is designed to fail. Inspect the reasons for the seven invalid rows, quarantine them, and validate the cleaned 75-row candidate before approving it.'},
 {q:'Can I reuse a Kafka checkpoint after my Colab VM was deleted?',a:'Do not attach the old checkpoint to a newly created broker and assume it is the same source. Restore the Day 3 state and follow the Day 4 reset instructions. The same-checkpoint restart demonstration happens inside one session with the original broker and topic.'},
 {q:'Can I use the published output as my submission?',a:'Use the reference to understand and compare results. Submit your own executed notebook, code decisions, observations, and reflection. A screenshot or a copied PASS message alone does not prove that your project ran.'},
 {q:'Can I work with a classmate?',a:'You may discuss the labs and help each other troubleshoot. Keep an individual repository, your own run evidence, and your own explanations for assessment.'},
 {q:'Where do I send my final repository?',a:'Use the private submission channel provided by your instructor. Include the repository URL, branch, and final commit SHA. Do not post your student ID, attendance record, or assessment grade in a public repository.'}
];
