"""Learner packaging tests; they do not substitute for native notebook execution."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
import nbformat
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repository_checker',ROOT/'scripts/check_repository.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'repo'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns(
            '.git','outputs','evidence','__pycache__','.venv','node_modules','dist',
            '.runtime','.pytest_cache','metastore_db','derby.log','target','logs','dbt_packages'))
    def tearDown(self):
        self.temp.cleanup()
    def mutate_config(self,name,value):
        path=self.root/'course.json';cfg=json.loads(path.read_text());cfg[name]=value
        path.write_text(json.dumps(cfg))
    def mutate_section(self,section,name,value):
        path=self.root/'course.json';cfg=json.loads(path.read_text());cfg[section][name]=value
        path.write_text(json.dumps(cfg))
    def test_clean_layout(self):
        result=checker.inspect(self.root)
        self.assertTrue(result['passed'], result['issues'])
        self.assertEqual(result['scheduled_hours'],20)
        self.assertEqual(result['net_learning_hours'],17.5)
        self.assertEqual(result['slides'],100)
        self.assertEqual(result['engine_notebooks'],5)
        self.assertFalse(result['release_evidence_checked'])
        self.assertFalse(result['release_verified'])
        self.assertFalse(result['engine_execution_claim'])
    def test_wrong_duration_rejected(self):
        self.mutate_section('schedule','total_hours',25)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_wrong_net_duration_rejected(self):
        self.mutate_section('schedule','net_learning_hours',20)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_shorter_lab_rejected(self):
        self.mutate_section('schedule','lab_minutes',45)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_prayer_break_cannot_be_omitted(self):
        self.mutate_section('schedule','prayer_breaks',[{'name':'Maghrib','minutes':15}])
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_days_requires_records_not_integer(self):
        self.mutate_config('days',5)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_certificate_threshold_is_70(self):
        self.mutate_section('certificate_policy','passing_project_score',60)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_all_five_days_of_attendance_are_required(self):
        self.mutate_section('certificate_policy','required_attendance_days',4)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_project_points_must_total_100(self):
        path=self.root/'course.json';cfg=json.loads(path.read_text())
        cfg['assessment'][0]['points']=5;path.write_text(json.dumps(cfg))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_each_day_requires_twenty_slides(self):
        path=self.root/'slides/day03.json';deck=json.loads(path.read_text())
        deck['slides'].pop();path.write_text(json.dumps(deck))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_daily_question_requires_an_answer_slide(self):
        path=self.root/'slides/day03.json';deck=json.loads(path.read_text())
        deck['slides'][-1]['kind']='concept';path.write_text(json.dumps(deck))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_missing_learning_outcome_rejected(self):
        path=self.root/'course.json';cfg=json.loads(path.read_text())
        cfg['learning_outcomes'].pop();path.write_text(json.dumps(cfg))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_extra_project_rejected(self):
        self.mutate_config('extra_final_project',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_required_distinction_rejected(self):
        self.mutate_config('distinction_required',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_paid_service_rejected(self):
        self.mutate_config('paid_services_required',True)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_private_material_rejected(self):
        (self.root/'INSTRUCTOR_PACKAGE.md').write_text('private')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_duplicate_entry_rejected(self):
        (self.root/'MASAR_STUDENT.ipynb').write_text('{}')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_missing_daily_notebook_rejected(self):
        (self.root/'day03/STUDENT.ipynb').unlink()
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_missing_lab_walkthrough_rejected(self):
        (self.root/'day04/labs/lab06/WALKTHROUGH.md').unlink()
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_broken_markdown_link_rejected(self):
        path=self.root/'README.md';path.write_text(path.read_text()+'\n<a href="missing.md">missing</a>')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_broken_notebook_link_rejected(self):
        path=self.root/'day02/STUDENT.ipynb';nb=nbformat.read(path,4)
        nb.cells.append(nbformat.v4.new_markdown_cell('<a href="missing.ipynb">missing</a>'))
        nbformat.write(nb,path)
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_changed_data_rejected(self):
        (self.root/'data/masar-small-v1/trips.csv').write_text('changed')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_payload_and_manifest_rewrite_rejected(self):
        p=self.root/'data/masar-small-v1/trips.csv';p.write_bytes(p.read_bytes()+b'\n')
        m=p.parent/'manifest.json';value=json.loads(m.read_text())
        for rec in value['files']:
            if rec['path']=='trips.csv':
                rec['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();rec['bytes']=p.stat().st_size
        m.write_text(json.dumps(value))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_wrong_notebook_registry_rejected(self):
        self.mutate_config('learner_notebooks',['missing.ipynb'])
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_reference_cannot_replace_engine_notebook(self):
        path=self.root/'course.json';cfg=json.loads(path.read_text())
        cfg['notebooks'][0]['kind']='reference';path.write_text(json.dumps(cfg))
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_dependency_and_build_trees_are_pruned(self):
        for folder in ('site/node_modules/dependency','site/dist','.venv/lib/example'):
            path=self.root/folder;path.mkdir(parents=True,exist_ok=True)
            (path/'README.md').write_text('[deliberately broken](missing.md)')
            (path/'invalid.ipynb').write_text('not a notebook')
        result=checker.inspect(self.root)
        self.assertTrue(result['passed'],result['issues'])
    def test_unpublished_development_layout_is_valid(self):
        self.mutate_config('published',False)
        result=checker.inspect(self.root)
        self.assertTrue(result['passed'],result['issues'])
        self.assertEqual(result['validation_mode'],'STRUCTURE_ONLY')
        self.assertFalse(result['release_verified'])
    def test_publication_does_not_make_development_check_a_release(self):
        self.mutate_config('published',True)
        result=checker.inspect(self.root)
        self.assertTrue(result['passed'],result['issues'])
        self.assertFalse(result['release_verified'])
    def test_invalid_metadata_reports_failure(self):
        (self.root/'course.json').write_text('[]')
        self.assertFalse(checker.inspect(self.root)['passed'])
    def test_publication_flag_cannot_replace_execution(self):
        (self.root/'docs/verification.json').unlink(missing_ok=True)
        cfg=json.loads((self.root/'course.json').read_text())
        self.assertEqual(checker.release_issues(self.root,{**cfg,'published':True}),
                         checker.release_issues(self.root,{**cfg,'published':False}))
        self.assertTrue(checker.release_issues(self.root,cfg))
    def test_incomplete_course_record_rejected(self):
        p=self.root/'docs/verification.json';p.write_text(json.dumps({'status':'PASSED','independent_course_runs':1}))
        self.assertTrue(checker.release_issues(self.root,{}))
    def test_malformed_release_record_does_not_crash(self):
        for value in ('[]','{'):
            (self.root/'docs/verification.json').write_text(value)
            self.assertTrue(checker.release_issues(self.root,{}))
    def test_two_run_flags_without_notebook_files_rejected(self):
        record={'scope':'FIVE_STUDENT_NOTEBOOKS_WITH_NATIVE_ENGINES_AND_DBT',
            'status':'PASSED','independent_course_runs':2,'notebook_executions':10,
            'fresh_kernel_per_day':True,'fresh_workspace_restore_per_day':True,
            'dataset_manifest_sha256':checker.DATASET_MANIFEST_SHA256,
            'implementation_sha256':checker.implementation_digest(self.root),
            'colab_host_tested':False,'host':'Local Linux compatibility runner'}
        (self.root/'docs/verification.json').write_text(json.dumps(record))
        self.assertTrue(checker.release_issues(self.root,{}))
    def test_release_requires_current_runtime_sources(self):
        record={'scope':'FIVE_STUDENT_NOTEBOOKS_WITH_NATIVE_ENGINES_AND_DBT',
            'status':'PASSED','independent_course_runs':2,'notebook_executions':10,
            'fresh_kernel_per_day':True,'fresh_workspace_restore_per_day':True,
            'dataset_manifest_sha256':checker.DATASET_MANIFEST_SHA256,
            'implementation_sha256':'0'*64}
        (self.root/'docs/verification.json').write_text(json.dumps(record))
        issues=checker.release_issues(self.root,{})
        self.assertTrue(any('Runtime implementation changed' in issue for issue in issues))
    def test_code_digest_detects_cell_change(self):
        nb=nbformat.read(self.root/'day01/STUDENT.ipynb',4);before=checker.code_digest(nb)
        next(c for c in nb.cells if c.cell_type=='code').source+='\nprint("changed")'
        self.assertNotEqual(before,checker.code_digest(nb))
    def test_code_digest_excludes_machine_timing_outputs(self):
        nb=nbformat.read(self.root/'day01/STUDENT.ipynb',4);before=checker.code_digest(nb)
        cell=next(c for c in nb.cells if c.cell_type=='code')
        cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text='a different duration')]
        self.assertEqual(before,checker.code_digest(nb))


if __name__=='__main__':
    unittest.main()
