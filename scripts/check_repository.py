"""Check the five-evening learning contract and optional native release evidence.

The default command is a development check. Only ``--release`` validates two
complete independent executions; publication flags cannot replace those files.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.native_contracts import STAGES, validate_stage_result
from masar.release_evidence import _safe_path, implementation_digest
from masar.workspace import DATASET_MANIFEST_SHA256, completed_bronze_workspace, digest_file

NOTEBOOKS = [f'day{day:02}/STUDENT.ipynb' for day in range(1, 6)]
LAB_DAYS = {'01': 1, '02': 1, '03': 2, '04': 3, '05': 4, '06': 4, '07': 5, '08': 5}
DAY_STAGES = {
    1: ['lab01_bronze', 'lab02_scan'],
    2: ['lab03a_staging', 'lab03b_silver'],
    3: ['lab04a_transactions', 'lab04b_maintenance'],
    4: ['lab05_streaming', 'lab06_quality'],
    5: ['lab07_gold_recovery', 'lab08_serving'],
}


def code_digest(nb):
    return hashlib.sha256(json.dumps(
        [c.source for c in nb.cells if c.cell_type == 'code'], ensure_ascii=False
    ).encode()).hexdigest()


def _object(path):
    result = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(result, dict):
        raise ValueError(f'{Path(path).name} must contain a JSON object')
    return result


def _contract_issues(root, cfg):
    problems = []
    schedule = cfg.get('schedule', {})
    if not isinstance(schedule, dict):
        schedule = {}
    expected_schedule = {
        'days': 5, 'start': '17:00', 'end': '21:00', 'timezone': 'Asia/Riyadh',
        'lecture_minutes': 150, 'lab_minutes': 60, 'total_hours': 20,
        'net_learning_hours': 17.5, 'slides_per_day': 20,
    }
    for name, expected in expected_schedule.items():
        if schedule.get(name) != expected:
            problems.append(f'Course schedule changed: {name} must be {expected}')
    breaks = schedule.get('prayer_breaks')
    if (not isinstance(breaks, list) or len(breaks) != 2
            or any(not isinstance(b, dict) for b in breaks)
            or [(b.get('name'), b.get('minutes')) for b in breaks] != [('Maghrib', 15), ('Isha', 15)]):
        problems.append('Each evening requires two 15-minute prayer breaks: Maghrib and Isha')
    for name, expected in {'language': 'en', 'labs_are_final_project': True,
                           'separate_final_project': False}.items():
        if cfg.get(name) != expected:
            problems.append('Course contract changed: ' + name)
    for name in ('paid_services_required', 'extra_final_project', 'distinction_required'):
        if cfg.get(name, False) is not False:
            problems.append('An additional completion requirement was introduced: ' + name)
    if type(cfg.get('published')) is not bool:
        problems.append('published must be a boolean; false is valid before publication')
    if cfg.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256:
        problems.append('The fixed MASAR_SMALL_V1 dataset manifest changed')
    if cfg.get('learner_notebooks') != NOTEBOOKS:
        problems.append('Daily notebook registry differs from the five-day learning path')
    registry = cfg.get('notebooks')
    if not isinstance(registry, list) or any(not isinstance(n, dict) for n in registry):
        problems.append('The notebook registry must be a list of path/kind objects')
        registry = []
    paths = [n.get('path') for n in registry]
    if any(not isinstance(p, str) for p in paths) or len(paths) != len(set(str(p) for p in paths)):
        problems.append('The notebook registry contains invalid or duplicate paths')
    if [n.get('path') for n in registry if n.get('kind') == 'engine'] != NOTEBOOKS:
        problems.append('Exactly five daily engine notebooks are required')
    for notebook in registry:
        if notebook.get('kind') not in {'engine', 'reference'}:
            problems.append('Unrecognized notebook kind')
        try:
            if not _safe_path(root, notebook.get('path')).is_file():
                raise ValueError('Notebook file is missing')
        except (OSError, TypeError, ValueError) as exc:
            problems.append(f'Notebook registry: {exc}')
    outcomes = cfg.get('learning_outcomes', [])
    if (not isinstance(outcomes, list) or any(not isinstance(o, dict) for o in outcomes)
            or sorted(str(o.get('id')) for o in outcomes) != [f'LO{n}' for n in range(1, 9)]):
        problems.append('The course must retain learning outcomes LO1 through LO8')
    days = cfg.get('days')
    if (not isinstance(days, list) or len(days) != 5 or any(not isinstance(d, dict) for d in days)
            or [d.get('number') for d in days] != list(range(1, 6))):
        problems.append('days must contain the five ordered daily course records')
        days = []
    covered = set()
    slide_total = 0
    for day in days:
        number = day['number']
        prefix = f'day{number:02}'
        for name, expected in {'id': prefix, 'notebook': prefix + '/STUDENT.ipynb',
                               'readme': prefix + '/README.md', 'slides': f'slides/{prefix}.json'}.items():
            if day.get(name) != expected:
                problems.append(f'Day {number}: incorrect {name} path')
        for name in ('question', 'answer'):
            if not isinstance(day.get(name), str) or not day[name].strip():
                problems.append(f'Day {number}: missing daily {name}')
        activity = day.get('activity', {})
        if not isinstance(activity, dict) or not all(isinstance(activity.get(k), str) and activity[k].strip() for k in ('prompt', 'answer')):
            problems.append(f'Day {number}: activity and model answer are required')
        daily_outcomes = day.get('outcomes', [])
        if not isinstance(daily_outcomes, list) or any(o not in [f'LO{n}' for n in range(1, 9)] for o in daily_outcomes):
            problems.append(f'Day {number}: invalid outcome mapping')
        else:
            covered.update(daily_outcomes)
        expected_labs = [key for key, value in LAB_DAYS.items() if value == number]
        daily_labs = day.get('labs', [])
        if (not isinstance(daily_labs, list) or any(not isinstance(lab, dict) for lab in daily_labs)
                or [lab.get('id') for lab in daily_labs] != expected_labs):
            problems.append(f'Day {number}: cumulative lab mapping changed')
        try:
            deck = _object(root / f'slides/{prefix}.json')
            slides = deck.get('slides', [])
            if (deck.get('day') != number or deck.get('language') != 'en'
                    or deck.get('slide_count') != 20 or not isinstance(slides, list)
                    or len(slides) != 20 or any(not isinstance(s, dict) for s in slides)
                    or [s.get('number') for s in slides] != list(range(1, 21))):
                raise ValueError('Exactly 20 numbered English slides are required')
            if any(not s.get('title') or not isinstance(s.get('body'), list) or not s['body'] for s in slides):
                raise ValueError('Every slide requires a title and content')
            kinds = [s.get('kind') for s in slides]
            for kind in ('activity', 'activity-answer', 'lab', 'outputs', 'question', 'answer'):
                if kinds.count(kind) != 1:
                    raise ValueError('One slide is required for ' + kind)
            if kinds.index('activity') > kinds.index('activity-answer') or kinds.index('question') > kinds.index('answer'):
                raise ValueError('A question or activity must appear before its answer')
            slide_total += len(slides)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append(f'Day {number} slide deck: {exc}')
    if covered != {f'LO{n}' for n in range(1, 9)}:
        problems.append('The daily plan must cover all eight course outcomes')
    if slide_total != 100:
        problems.append('The five-day course must contain 100 slides in total')
    labs = cfg.get('labs')
    if (not isinstance(labs, list) or any(not isinstance(lab, dict) for lab in labs)
            or [(lab.get('id'), lab.get('day')) for lab in labs] != list(LAB_DAYS.items())):
        problems.append('The cumulative project must contain the eight correctly mapped labs')
    assessment = cfg.get('assessment')
    if (not isinstance(assessment, list) or not assessment
            or any(not isinstance(a, dict) or type(a.get('points')) is not int or a['points'] <= 0 for a in assessment)
            or sum(a['points'] for a in assessment) != 100):
        problems.append('The project assessment must allocate exactly 100 points')
    policy = cfg.get('certificate_policy', {})
    if not isinstance(policy, dict):
        policy = {}
    for name, expected in {'required_attendance_days': 5, 'project_max_score': 100,
                           'passing_project_score': 70}.items():
        if policy.get(name) != expected:
            problems.append(f'Certificate policy changed: {name} must be {expected}')
    return problems


def release_issues(root: Path, cfg: dict) -> list[str]:
    """Publishing flags never replace two saved, complete course executions."""
    try:
        return _course_execution_issues(Path(root).resolve(), cfg)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, nbformat.ValidationError) as exc:
        return ['Invalid full-course execution evidence: ' + str(exc)]


def _executed_notebook(path):
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    cells = [c for c in notebook.cells if c.cell_type == 'code' and c.source.strip()]
    if not cells or any(type(c.execution_count) is not int or c.execution_count < 1 for c in cells):
        raise ValueError('Missing executed code cells: ' + str(path))
    if any(output.get('output_type') == 'error' for cell in cells for output in cell.outputs):
        raise ValueError('A saved notebook contains an error: ' + str(path))
    return notebook, cells


def _restore_record(record, day, workspace):
    if (not isinstance(record, dict) or record.get('status') != 'RESTORED_WITHOUT_OVERWRITE'
            or record.get('day') != day or record.get('workspace') != workspace
            or type(record.get('files_created')) is not int or record['files_created'] <= 0):
        raise ValueError(f'Day {day} continuation archive was not restored into a fresh workspace')


def _retained_run_reports(root, result):
    """Audit the reports retained after native artifact validation by the runner.

    Full Delta data is validated during execution and archive restoration. This
    published package retains notebooks and small reports, not every Parquet file.
    """
    attempt = result['attempt']
    base = _safe_path(root, f'evidence/student-course/reports/run_{attempt}')
    work = completed_bronze_workspace(base)
    workspace = work.relative_to(base).as_posix()
    if _object(work / '.masar-workspace.json').get('run_id') != result['run_id']:
        raise ValueError('Retained workspace identity differs from its course run')
    for day, stage_names in DAY_STAGES.items():
        item = result['days'][day - 1]
        for name in stage_names:
            report = _object(_safe_path(work, STAGES[name][0]))
            validate_stage_result(name, report)
            if item['checks'][name] != report['checks']:
                raise ValueError('Saved stage checks differ from the course record: ' + name)
        metrics = _object(base / f'outputs/day{day:02}_metrics.json')
        if metrics != item['metrics'] or metrics != _object(root / f'expected/day{day:02}.json'):
            raise ValueError(f'Run {attempt}, Day {day}: observed business metrics differ')
        if day == 1:
            if item.get('restored_previous_day') is not None:
                raise ValueError('Day 1 must begin without a previous-day archive')
        else:
            _restore_record(item.get('restored_previous_day'), day - 1, workspace)
    _restore_record(result.get('final_restore'), 5, workspace)
    bronze = _object(work / STAGES['lab01_bronze'][0])
    scan = _object(work / STAGES['lab02_scan'][0])
    serving = _object(work / STAGES['lab08_serving'][0])
    if (result.get('bronze_counts') != bronze.get('counts')
            or result.get('base_aggregate') != scan.get('expected_and_observed_aggregate')
            or result.get('serving_checks') != serving.get('checks')):
        raise ValueError('Course business summaries differ from the retained engine reports')
    dbt_paths = list((base / 'outputs').rglob('dbt_attempt.json'))
    if len(dbt_paths) != 1:
        raise ValueError('Exactly one retained dbt attempt is required per course run')
    dbt_path = _safe_path(base, dbt_paths[0].relative_to(base).as_posix())
    dbt = _object(dbt_path)
    if (dbt.get('scope') != 'DBT_RUNTIME_ATTEMPT' or dbt.get('status') != 'PASSED_DBT_NATIVE'
            or dbt.get('dbt_executed') is not True or dbt.get('engine_executed') is not True
            or dbt.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
            or dbt.get('implementation_sha256') != result['implementation_sha256']):
        raise ValueError('The retained dbt execution is incomplete or stale')
    phases = dbt.get('phases')
    if (not isinstance(phases, list) or [p.get('phase') for p in phases] != ['base', 'rerun', 'late', 'late_replay']
            or [p.get('rows') for p in phases] != [72, 72, 75, 75]):
        raise ValueError('All four native dbt scenarios are required')
    if result.get('dbt_phases') != [{k: p[k] for k in ('phase', 'rows', 'total_fare_sar', 'business_digest')} for p in phases]:
        raise ValueError('dbt scenario summary differs from its native report')
    dbt_work = dbt_path.parent.parent
    for phase in phases:
        snapshot = _safe_path(dbt_work, phase['snapshot'])
        if digest_file(snapshot) != phase['snapshot_sha256']:
            raise ValueError('Missing or changed dbt business snapshot')
    commands = dbt.get('commands')
    names = [phase + '_' + command for phase in ('base', 'rerun', 'late', 'late_replay')
             for command in ('stage', 'gate', 'freshness', 'build')] + ['documentation']
    if (not isinstance(commands, list) or [c.get('phase') for c in commands] != names
            or result['days'][1].get('dbt_commands') != len(names)):
        raise ValueError('Native dbt model, test, freshness and documentation commands are incomplete')
    invocations = set()
    for command in commands[:-1]:
        invocation = command.get('invocation_id')
        if not isinstance(invocation, str) or not invocation or invocation in invocations:
            raise ValueError('Missing or repeated dbt command invocation')
        invocations.add(invocation)
        target = _safe_path(dbt_work, command['target'])
        artifact_name = 'sources.json' if command['phase'].endswith('_freshness') else 'run_results.json'
        matches = [a for a in command.get('artifacts', []) if a.get('name') == artifact_name]
        if len(matches) != 1 or digest_file(_safe_path(target, artifact_name)) != matches[0].get('sha256'):
            raise ValueError('A native dbt result artifact is missing or changed')
        artifact = _object(target / artifact_name)
        rows = artifact.get('results')
        allowed = {'pass', 'warn'} if artifact_name == 'sources.json' else {'pass', 'success'}
        if (artifact.get('metadata', {}).get('invocation_id') != invocation
                or not isinstance(rows, list) or not rows
                or any(r.get('status') not in allowed for r in rows)):
            raise ValueError('A retained native dbt command did not succeed')


def _course_execution_issues(root, cfg):
    path = root / 'docs/verification.json'
    if not path.is_file():
        return ['No independent full-course notebook execution record']
    report = _object(_safe_path(root, 'docs/verification.json'))
    if (report.get('scope') != 'FIVE_STUDENT_NOTEBOOKS_WITH_NATIVE_ENGINES_AND_DBT'
            or report.get('status') != 'PASSED' or report.get('independent_course_runs') != 2
            or report.get('notebook_executions') != 10
            or report.get('fresh_kernel_per_day') is not True
            or report.get('fresh_workspace_restore_per_day') is not True):
        raise ValueError('Two complete five-day executions with fresh kernels and restored state are required')
    if report.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256:
        raise ValueError('Wrong dataset in execution evidence')
    if report.get('implementation_sha256') != implementation_digest(root):
        raise ValueError('Runtime implementation changed after execution')
    if type(report.get('colab_host_tested')) is not bool or not report.get('host'):
        raise ValueError('The actual execution host must be stated explicitly')
    if report['colab_host_tested'] and report['host'] != 'Google Colab hosted runtime':
        raise ValueError('A hosted Colab claim requires the Colab execution host')
    if _object(_safe_path(root, 'evidence/student-course/summary.json')) != report:
        raise ValueError('Published verification differs from the retained course summary')
    results = report.get('results')
    if (not isinstance(results, list) or len(results) != 2 or any(not isinstance(r, dict) for r in results)
            or [r.get('attempt') for r in results] != [1, 2]):
        raise ValueError('Two distinct ordered course attempts are required')
    identities = [r.get('run_id') for r in results]
    if any(not isinstance(i, str) or not re.fullmatch(r'[0-9a-f]{32}', i) for i in identities) or len(set(identities)) != 2:
        raise ValueError('Course runs must have different native workspace identities')
    for result in results:
        attempt = result['attempt']
        if result.get('status') != 'PASSED' or result.get('implementation_sha256') != report['implementation_sha256']:
            raise ValueError('A course attempt is incomplete or uses different runtime sources')
        if result.get('host') != report['host'] or result.get('colab_host_tested') is not report['colab_host_tested']:
            raise ValueError('Inconsistent execution host claims')
        days = result.get('days')
        if (not isinstance(days, list) or len(days) != 5 or any(not isinstance(d, dict) for d in days)
                or [d.get('day') for d in days] != list(range(1, 6))):
            raise ValueError('Each independent course attempt must complete all five days in order')
        if _object(_safe_path(root, f'evidence/student-course/notebooks/run_{attempt}/summary.json')) != result:
            raise ValueError('A course attempt differs from its retained summary')
        for day, item in enumerate(days, start=1):
            if item.get('status') != 'PASSED' or item.get('stages') != DAY_STAGES[day]:
                raise ValueError(f'Run {attempt}, Day {day}: missing native stages')
            checks = item.get('checks')
            if not isinstance(checks, dict) or set(checks) != set(DAY_STAGES[day]):
                raise ValueError(f'Run {attempt}, Day {day}: missing stage checks')
            for stage in DAY_STAGES[day]:
                values = checks[stage]
                if (not isinstance(values, dict) or not STAGES[stage][2].issubset(values)
                        or not all(value is True for value in values.values())):
                    raise ValueError('Incomplete or unsuccessful native checks: ' + stage)
            relative = f'evidence/student-course/notebooks/run_{attempt}/day{day:02}.ipynb'
            nb_path = _safe_path(root, relative)
            if item.get('notebook') != relative or item.get('notebook_sha256') != digest_file(nb_path):
                raise ValueError('A saved executed notebook is missing or changed: ' + relative)
            notebook, cells = _executed_notebook(nb_path)
            current = nbformat.read(_safe_path(root, NOTEBOOKS[day - 1]), as_version=4)
            if item.get('code_sha256') != code_digest(notebook) or code_digest(notebook) != code_digest(current):
                raise ValueError(f'Day {day}: source changed after execution')
            if item.get('code_cells_executed') != len(cells):
                raise ValueError('Executed code-cell count differs from saved notebook')
            if (item.get('handoff_zip_verified') is not True or type(item.get('handoff_files')) is not int
                    or item['handoff_files'] <= 0):
                raise ValueError(f'Day {day}: continuation archive was not verified')
        _retained_run_reports(root, result)
    for name in ('bronze_counts', 'base_aggregate', 'dbt_phases', 'serving_checks'):
        if results[0].get(name) != results[1].get(name):
            raise ValueError('Independent native business results differ: ' + name)
    for day in range(1, 6):
        notebook, cells = _executed_notebook(_safe_path(root, NOTEBOOKS[day - 1]))
        _, recorded_cells = _executed_notebook(root / f'evidence/student-course/notebooks/run_1/day{day:02}.ipynb')
        record = _object(_safe_path(root, f'day{day:02}/verification.json'))
        if (record.get('day') != day or record.get('status') != 'PASSED'
                or record.get('independent_course_runs') != 2
                or record.get('dataset_manifest_sha256') != DATASET_MANIFEST_SHA256
                or record.get('code_sha256') != code_digest(notebook)
                or record.get('checks') != results[0]['days'][day - 1]
                or record.get('host') != report['host']
                or record.get('colab_host_tested') is not report['colab_host_tested']):
            raise ValueError(f'Day {day}: incomplete or inconsistent daily verification')
        if [(c.execution_count, c.outputs) for c in cells] != [(c.execution_count, c.outputs) for c in recorded_cells]:
            raise ValueError(f'Day {day}: student-facing outputs differ from the retained first run')
    return []


def inspect(root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    problems = []
    spec = importlib.util.spec_from_file_location('student_layout', ROOT / 'scripts/check_student_course.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        layout = module.inspect(root)
        problems.extend(layout['errors'])
    except Exception as exc:
        layout = {}
        problems.append('Learner layout: ' + str(exc))
    try:
        cfg = _object(root / 'course.json')
        problems.extend(_contract_issues(root, cfg))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        problems.append('Course metadata: ' + str(exc))
    for forbidden in ('INSTRUCTOR_PACKAGE.md', 'instructor_only', 'MASAR_STUDENT.ipynb', 'DAY01_STUDENT.ipynb'):
        if (root / forbidden).exists():
            problems.append('Private or duplicate learner entry: ' + forbidden)
    return {
        **{k: v for k, v in layout.items() if k not in ('errors', 'status')},
        'passed': not problems, 'issues': problems, 'warnings': [],
        'validation_mode': 'STRUCTURE_ONLY', 'release_evidence_checked': False,
        'release_verified': False, 'scheduled_hours': 20, 'net_learning_hours': 17.5,
        'engine_notebooks': 5, 'slides': 100,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true', help='Require two complete independent native course executions')
    args = parser.parse_args()
    result = inspect()
    if args.release:
        try:
            cfg = _object(ROOT / 'course.json')
        except (OSError, ValueError):
            cfg = {}
        result['issues'].extend(release_issues(ROOT, cfg))
        result['passed'] = not result['issues']
        result['validation_mode'] = 'TWO_RUN_RELEASE'
        result['release_evidence_checked'] = True
        result['release_verified'] = result['passed']
        result['engine_execution_claim'] = result['passed']
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
