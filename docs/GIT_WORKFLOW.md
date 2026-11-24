# Save your work to GitHub every day

Use one repository in your own GitHub account for all five days. Use its `main` branch unless your instructor explicitly asks for another branch. You do not need to submit a pull request to the course repository.

## First day: create your copy

1. Open [the course repository](https://github.com/almiyead-rgb/masar-ai-data-engineering-ksu).
2. Select **Fork**, choose your account and create the fork.
3. Keep the course files and attribution. Your fork is where you save your notebooks, small code changes and evidence.
4. Open the daily notebook in Colab. At the first save, choose your own repository as the destination.

A fork of the public course is public. Use the supplied synthetic dataset and do not upload credentials, private attendance/grade records, real customer data or personal GPS traces.

## Edit your student files before saving

After restoring the previous day, notebook setup creates the day's note templates under `student/` without overwriting existing work. Complete them in Colab's Files panel before running the save cell. Use your own decisions and observed output; the templates start with PENDING prompts, not completed answers.

| File | What you add |
|---|---|
| `student/dayNN/REFLECTION.md` | Your daily first answer, observed evidence and any correction after discussion; the notebook's `MY_ANSWER` and `MY_EVIDENCE` fields create this file. |
| `student/dayNN/LABxx_NOTES.md` | The numbered lab's run evidence and your interpretation. Day 1 has Labs 01–02, Day 2 Lab 03, Day 3 Lab 04, Day 4 Labs 05–06, Day 5 Labs 07–08. |
| `student/DECISIONS.md` | Your architecture choice, alternatives and cost assumptions. |
| `student/BENCHMARKS.md` | Your measured scan observations and their limits. |
| `student/GOVERNANCE.md` | Your purpose, ownership, lineage, access and retention decisions; introduced on Day 4. |
| `student/PROJECT_README.md` | Your cumulative project explanation, completed by Day 5. |

Fill your notes as each lab section finishes; reserve the last five minutes for packaging and upload. The save helper includes the entire `student/` folder in both daily packages. Edit these runtime files before packaging so the GitHub upload and Drive continuation contain the same work. Do not replace your first reflection with a copied model answer; retain your attempt and explain any correction.

## End of each day: the five-minute save

### A. Save the executed notebook

1. In Colab, choose **File → Save a copy in GitHub**.
2. Select your repository and `main`.
3. Keep the path for the day, such as `day02/STUDENT.ipynb`.
4. Use a meaningful message, for example `Complete Day 2 Silver and dbt lab`.
5. Open the saved notebook on GitHub and check that your small result outputs are present. Do not enable an option that omits cell output if you need that output as evidence.

If the integration is unavailable, download the notebook as `.ipynb` from Colab and use GitHub's **Add file → Upload files** in the correct folder. Never put a GitHub token inside a notebook, a shell command saved as output or a repository file.

### B. Upload your small evidence files

Run the export/save cells in the notebook. Download `outputs/dayNN_github.zip`, extract it on your computer and inspect the contents. Upload the **extracted files**, preserving their directories, to your repository with **Add file → Upload files**. Do not upload only a ZIP and expect GitHub to display the individual notes.

GitHub accepts up to **100 files per browser upload**. If the extracted bundle has more files, upload it in smaller batches while preserving the directory paths. Upload the current day's new files and your changed notes; previously committed unchanged files do not need another upload. Confirm that every intended new or changed file reached the repository. [GitHub upload limits](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

The bundle carries your notes, small reports, relevant SQL and stage evidence. The executed notebook is saved separately by step A. Do not place package caches, downloaded JARs, Kafka logs or the live Delta workspace in ordinary Git commits.

### C. Keep the state needed for tomorrow

Save `outputs/dayNN_handoff.zip` to your course folder in Drive. This is the full state archive used by the next notebook. It is different from the small GitHub review bundle. Keep earlier daily archives until your project has been assessed.

### D. Check the published result

Open your repository in the browser. Check the notebook, your notes, the evidence files and the latest commit. A completed Colab cell or a local commit does not prove that the file reached GitHub.

## Suggested commit messages

- `Complete Day 1 architecture and Bronze`
- `Complete Day 2 ELT Silver and dbt`
- `Complete Day 3 Delta correction and recovery`
- `Complete Day 4 Kafka and quality gate`
- `Complete Day 5 serving and final project`

## Optional command-line route

If you already use Git locally, add only your intended files, commit them, and push to your own repository. Check `git remote -v` first. Use your normal configured sign-in method; the course does not require a token embedded in code. Do not force-push to solve an authentication error.

## Final submission

Copy the repository URL, branch and final commit SHA. On GitHub, open the final commit to copy its full ID. Submit them through the instructor's announced private channel. An unchanged course fork is not a completed submission.

[Final checklist](../project/SUBMISSION.md) · [GitHub fork guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo) · [GitHub upload guide](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
