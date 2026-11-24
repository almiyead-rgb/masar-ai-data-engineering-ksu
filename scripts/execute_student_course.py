"""Execute real daily notebooks twice, using fresh kernels and restored state.

Only interactive Drive/download dialogs are suppressed. Actual native engines
still execute. One run is diagnostic; two are required for release evidence.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.colab import inspect_handoff, restore_handoff
from masar.native_contracts import read_stage_report
from masar.release_evidence import implementation_digest
from masar.workspace import completed_bronze_workspace, DATASET_MANIFEST_SHA256

STAGES = {
    1: ['lab01_bronze', 'lab02_scan'],
    2: ['lab03a_staging', 'lab03b_silver'],
    3: ['lab04a_transactions', 'lab04b_maintenance'],
    4: ['lab05_streaming', 'lab06_quality'],
    5: ['lab07_gold_recovery', 'lab08_serving'],
}
EVIDENCE = ROOT / 'evidence/student-course'
IGNORE = shutil.ignore_patterns('.git', '.venv', 'node_modules', 'dist', 'outputs', 'evidence',
    'student', '__pycache__', '.pytest_cache', '.ipynb_checkpoints', 'metastore_db', 'derby.log',
    'target', 'logs', 'dbt_packages', 'site', '.runtime', '.openai')


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def code_hash(nb) -> str:
    code = json.dumps([c.source for c in nb.cells if c.cell_type == 'code'], ensure_ascii=False)
    return hashlib.sha256(code.encode()).hexdigest()


def observed_host() -> dict:
    colab = bool(os.environ.get('COLAB_RELEASE_TAG'))
    github = os.environ.get('GITHUB_ACTIONS') == 'true'
    host = 'Google Colab hosted runtime' if colab else (
        'GitHub Actions runner' if github else 'Local Linux compatibility runner')
    workflow = ('https://github.com/' + os.environ['GITHUB_REPOSITORY'] + '/actions/runs/' +
                os.environ['GITHUB_RUN_ID']) if github else None
    return {'host': host, 'platform': platform.platform(), 'python': platform.python_version(),
            'colab_host_tested': colab, 'workflow_url': workflow}


def retain_reports(source: Path, target: Path) -> None:
    for base, dirs, names in os.walk(source / 'outputs'):
        dirs[:] = [d for d in dirs if d not in {'_delta_log', '_kafka_runtime', '__pycache__'}]
        for name in names:
            path = Path(base) / name
            if (path.suffix not in {'.json', '.log', '.csv', '.txt'} or
                name in {'manifest.json', 'catalog.json', 'partial_parse.msgpack'} or
                path.stat().st_size > 2_000_000):
                continue
            dest = target / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)


def prepare_kernel(parent: Path) -> str:
    """Use this pinned interpreter instead of an unrelated global python3."""
    kernel = parent / 'jupyter/kernels/masar-validation'
    kernel.mkdir(parents=True)
    save(kernel / 'kernel.json', {'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                                'display_name': 'Masar pinned validation', 'language': 'python'})
    os.environ['JUPYTER_PATH'] = str(parent / 'jupyter') + os.pathsep + os.environ.get('JUPYTER_PATH', '')
    os.environ['MASAR_NONINTERACTIVE'] = '1'
    return 'masar-validation'


def run_course(attempt: int, sandbox: Path, kernel: str, host: dict) -> dict:
    target = EVIDENCE / 'notebooks' / f'run_{attempt}'
    reports_target = EVIDENCE / 'reports' / f'run_{attempt}'
    result = {'attempt': attempt, 'status': 'RUNNING', 'days': [],
              'implementation_sha256': implementation_digest(ROOT), **host}
    target.mkdir(parents=True, exist_ok=True)
    previous_archive = None
    source = None
    try:
        for day, stages in STAGES.items():
            started = time.monotonic()
            print(f'EXECUTING run {attempt} / day {day}', flush=True)
            source = sandbox / f'run_{attempt}' / f'day{day:02}'
            shutil.copytree(ROOT, source, ignore=IGNORE)
            restoration = restore_handoff(source, previous_archive, expected_day=day - 1) if previous_archive else None
            nb = nbformat.read(source / f'day{day:02}/STUDENT.ipynb', as_version=4)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.outputs = []
                    cell.execution_count = None
            nb_path = target / f'day{day:02}.ipynb'
            try:
                NotebookClient(nb, timeout=1200, kernel_name=kernel,
                    resources={'metadata': {'path': str(source)}}, allow_errors=False).execute()
            finally:
                nbformat.write(nb, nb_path)
            cells = [c for c in nb.cells if c.cell_type == 'code' and c.source.strip()]
            assert cells and all(c.execution_count is not None for c in cells), 'Unexecuted code cell'
            assert not any(o.output_type == 'error' for c in cells for o in c.outputs), 'Notebook error'
            work = completed_bronze_workspace(source)
            reports = {stage: read_stage_report(work, stage) for stage in stages}
            observed = json.loads((source / f'outputs/day{day:02}_metrics.json').read_text())
            expected = json.loads((ROOT / f'expected/day{day:02}.json').read_text())
            assert observed == expected, f'Day {day} observed metrics differ: {observed!r}'
            day_result = {'day': day, 'status': 'PASSED', 'stages': list(reports),
                'checks': {stage: report['checks'] for stage, report in reports.items()},
                'code_cells_executed': len(cells), 'code_sha256': code_hash(nb),
                'notebook': nb_path.relative_to(ROOT).as_posix(),
                'notebook_sha256': hashlib.sha256(nb_path.read_bytes()).hexdigest(),
                'metrics': observed, 'restored_previous_day': restoration}
            if day == 1:
                result['run_id'] = json.loads((work / '.masar-workspace.json').read_text())['run_id']
                result['bronze_counts'] = reports['lab01_bronze']['counts']
                result['base_aggregate'] = reports['lab02_scan']['expected_and_observed_aggregate']
            if day == 2:
                paths = list((source / 'outputs').rglob('dbt_attempt.json'))
                assert len(paths) == 1, 'Exactly one native daily dbt run is required'
                dbt = json.loads(paths[0].read_text())
                assert dbt['status'] == 'PASSED_DBT_NATIVE' and dbt['dbt_executed'] is True
                assert [p['rows'] for p in dbt['phases']] == [72, 72, 75, 75]
                result['dbt_phases'] = [{k: p[k] for k in ('phase', 'rows', 'total_fare_sar', 'business_digest')} for p in dbt['phases']]
                day_result['dbt_commands'] = len(dbt['commands'])
            if day == 5:
                result['serving_checks'] = reports['lab08_serving']['checks']
            archive = source / f'outputs/day{day:02}_handoff.zip'
            manifest = inspect_handoff(archive, expected_day=day)
            day_result.update(handoff_zip_verified=True, handoff_files=len(manifest['files']),
                              elapsed_seconds=round(time.monotonic() - started, 2))
            previous_archive = sandbox / f'handoffs/run_{attempt}_day{day:02}.zip'
            previous_archive.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archive, previous_archive)
            retain_reports(source, reports_target)
            result['days'].append(day_result)
            save(target / 'summary.json', result)
            # Only this runner's temporary checkout is removed. This proves the
            # next day's relative paths use its restored state, not the old VM.
            shutil.rmtree(source)
            source = None
            print(f"PASSED run {attempt} / day {day}: {day_result['elapsed_seconds']}s", flush=True)
        final_restore = sandbox / f'run_{attempt}/final_restore'
        shutil.copytree(ROOT, final_restore, ignore=IGNORE)
        result['final_restore'] = restore_handoff(final_restore, previous_archive, expected_day=5)
        work = completed_bronze_workspace(final_restore)
        for stages in STAGES.values():
            for stage in stages:
                read_stage_report(work, stage)
        result['status'] = 'PASSED'
    except Exception as exc:
        result.update(status='FAILED', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        save(target / 'summary.json', result)
        if source:
            retain_reports(source, reports_target)
    return result


def publish_record(results: list[dict], host: dict) -> None:
    assert len(results) == 2 and results[0]['run_id'] != results[1]['run_id'], 'Need two distinct full runs'
    digest = implementation_digest(ROOT)
    assert all(r['implementation_sha256'] == digest for r in results), 'Implementation changed during execution'
    for key in ('bronze_counts', 'base_aggregate', 'dbt_phases', 'serving_checks'):
        assert results[0][key] == results[1][key], f'Non-repeatable business result: {key}'
    assert [d['metrics'] for d in results[0]['days']] == [d['metrics'] for d in results[1]['days']]
    verified = datetime.now(timezone.utc).isoformat()
    for day in STAGES:
        nb = nbformat.read(EVIDENCE / f'notebooks/run_1/day{day:02}.ipynb', as_version=4)
        nb.metadata['masar'] = {'day': day, 'execution_status': 'PASSED', 'independent_course_runs': 2,
                                'verified_at_utc': verified, **host}
        nbformat.write(nb, ROOT / f'day{day:02}/STUDENT.ipynb')
        save(ROOT / f'day{day:02}/verification.json', {'day': day, 'status': 'PASSED',
            'independent_course_runs': 2, 'verified_at_utc': verified,
            'dataset_manifest_sha256': DATASET_MANIFEST_SHA256, 'code_sha256': code_hash(nb),
            'checks': results[0]['days'][day - 1], **host})
    summary = {'status': 'PASSED', 'scope': 'FIVE_STUDENT_NOTEBOOKS_WITH_NATIVE_ENGINES_AND_DBT',
        'independent_course_runs': 2, 'notebook_executions': 10, 'verified_at_utc': verified,
        'dataset_manifest_sha256': DATASET_MANIFEST_SHA256, 'fresh_kernel_per_day': True,
        'fresh_workspace_restore_per_day': True, 'production_scale_tested': False,
        'implementation_sha256': digest, 'results': results, **host}
    save(ROOT / 'docs/verification.json', summary)
    save(EVIDENCE / 'summary.json', summary)
    record = f'''# Actual execution record

The five student notebooks completed in order in **two independent course runs**.
Every day used a fresh Python kernel. Days 2–5 restored the prior day's checked
handoff ZIP into a fresh source checkout after the previous directory was removed.
The student notebooks contain the real outputs from the first complete run.

| Verification | Observed result |
|---|---|
| Host | {host['host']} |
| Python | {host['python']} |
| Complete course runs / notebook executions | 2 / 10 |
| Actual engines | PySpark 3.5.8, Delta 3.3.3, dbt-core 1.9.8 / dbt-spark 1.9.1, Kafka 4.0.2, GX 1.7.0 |
| Runtime Java | 17 |
| Google Colab host executed | {host['colab_host_tested']} |
| Production-scale deployment tested | False |
| Record time (UTC) | {verified} |

## Inspect the evidence

- [Machine-readable verification](verification.json)
- [First run notebooks](../evidence/student-course/notebooks/run_1/)
- [Second run notebooks](../evidence/student-course/notebooks/run_2/)
- [First run reports](../evidence/student-course/reports/run_1/)
- [Second run reports](../evidence/student-course/reports/run_2/)
- [Expected business results](../expected/README.md)

Business metrics are reproducible. Elapsed time, generated identifiers, file
names and local paths vary. A matching result file does not establish attendance,
authorship or a project grade. Empty learner reflections remain visibly pending.

Google Colab is the student execution environment. This record states exactly
which host ran validation; it does not substitute a local run for a hosted Colab
trial. The organizer checks the selected runtime before the actual course dates.

## Reproduce

In the pinned Python and Java environment, install `requirements-validation.txt`,
then run `python scripts/execute_student_course.py --runs 2`. The runner clears all
saved notebook outputs before execution and stops on a failed engine cell or
business-result mismatch. [Return to the course](../README.md).
'''
    (ROOT / 'docs/VERIFICATION.md').write_text(record, encoding='utf-8')
    print(json.dumps({'status': 'PASSED', 'notebook_executions': 10, **host}, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    host = observed_host()
    with tempfile.TemporaryDirectory(prefix='masar_validation_') as folder:
        sandbox = Path(folder)
        kernel = prepare_kernel(sandbox)
        results = [run_course(i, sandbox, kernel, host) for i in range(1, args.runs + 1)]
        if args.runs == 2:
            publish_record(results, host)
        else:
            print('One diagnostic run passed. No two-run release claim was written.', flush=True)


if __name__ == '__main__':
    main()
