# Masar student portal

The English student workspace for **Modern Data Engineering for AI Systems (SDA-DSC-214)**.

## Content and runtime

- `../course.json` supplies the five-day structure, learning outcomes, rubric, and certificate policy.
- `../slides/day01.json` through `day05.json` supply exactly 20 slides per day.
- Markdown guides are bundled from the course folders and can be read within the portal.
- `../expected/day01.json` through `day05.json` define the stable reference metrics used by the browser comparison.
- The website runs no Spark, Kafka, Python, attendance service, or grading backend. Its primary lab links open Google Colab.
- Personal checklists and draft reflections use local browser storage. They are not official records.
- Student metrics files are read locally with `File.text()` and compared in the browser. The portal does not upload those files.

## Develop and build

```bash
cd site
npm ci
npm run dev -- --host 0.0.0.0 --port 4173 --strictPort
```

```bash
npm run test:logic
npm run build
```

Publish **`site/dist/client`** to GitHub Pages. The relative Vite base and hash routes support the project URL:

`https://almiyead-rgb.github.io/masar-ai-data-engineering-ksu/`

The Product Design starter also emits a Sites worker and metadata outside `dist/client`; GitHub Pages only needs `dist/client`.

## Main routes

| Route | Purpose |
| --- | --- |
| `#home` | Project introduction and daily learning path |
| `#start` or `#setup` | Guided account, repository, Colab, and saving setup |
| `#project` | Business problem, architecture, and eight outcomes |
| `#day-1` through `#day-5` | Learn, Apply, Compare, and Save |
| `#slides-1-1` | Day 1, slide 1; supports keyboard navigation and printing |
| `#results` | Local metrics-file and manual result comparison |
| `#assessment` | The 100-point rubric and certificate rules |
| `#submission` | Daily saving and final delivery checklist |
| `#help` | Troubleshooting and searchable glossary |
| `#read/day01/CONCEPTS.md` | Embedded course document |

## Checks before publication

1. Inspect the home, setup, daily lesson, comparison, submission, and slide views in a browser.
2. Test navigation at desktop and mobile widths.
3. Test a matching metrics JSON, a mismatched result, a wrong-day file, malformed JSON, and an oversized file.
4. Verify that every daily notebook and source link points at the new repository.
5. Verify that each slide deck contains 20 slides and that slide 19 is followed by its answer on slide 20.
6. Inspect printed slide pages and review the source notes.
7. Check the browser console and document any remaining limits honestly.

No frontend test proves that a lab ran. Lab execution evidence is maintained separately in the repository verification records.
