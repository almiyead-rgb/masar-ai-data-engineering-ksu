"""Offline safety tests with synthetic files, not Delta/Kafka engine evidence."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar import colab
from masar.kafka_local import parse_sha512
from masar.workspace import new_workspace, write_json, record_bronze_success, DATASET_MANIFEST_SHA256


class ChecksumTests(unittest.TestCase):
    def test_real_apache_eight_character_group_format(self):
        text = """kafka_2.13-4.0.2.tgz: B854B5EE 761F04F8 BD27F185 76590CD5 4F4890D5 DC103818
 F3DB23C1 A5B04DE2 7F8465D4 042F7CDF 463DBFA6 F149DAFC
 A92B60F5 6B5E2136 861CF8D7 66F1A56B"""
        self.assertEqual(parse_sha512(text),
            "b854b5ee761f04f8bd27f18576590cd54f4890d5dc103818f3db23c1a5b04de2"
            "7f8465d4042f7cdf463dbfa6f149dafca92b60f56b5e2136861cf8d766f1a56b")

    def test_complete_and_sixteen_character_group_formats(self):
        full = "ab" * 64
        self.assertEqual(parse_sha512(full + "  kafka.tgz"), full)
        self.assertEqual(parse_sha512(" ".join(full[i:i+16] for i in range(0, 128, 16))), full)

    def test_ambiguous_or_truncated_checksum_rejected(self):
        for value in ["bad checksum", "abcdef12", "ab" * 64 + "\n" + "cd" * 64]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_sha512(value)


class HandoffSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "course"
        self.root.mkdir()
        (self.root / "course.json").write_text("{}")
        self.work = new_workspace(self.root, "synthetic_test")
        # These are deliberately fake tiny unit-test fixtures. Native engine
        # tests separately validate real Delta data and stage report contents.
        write_json(self.work / "reports/bronze.json", {"scope": "DAY01_BRONZE_ENGINE", "engine_executed": True,
            "counts": {"trips": 144, "drivers": 6, "gps_events": 216}, "checks": {"fixture_only": True},
            "dataset_manifest_sha256": DATASET_MANIFEST_SHA256})
        log = self.work / "mini_lakehouse/bronze/trips/_delta_log/00000000000000000000.json"
        log.parent.mkdir(parents=True)
        log.write_text('{"unit_test_fixture": true}')
        record_bronze_success(self.root, self.work)
        self.dbt = new_workspace(self.root, "dbt_validation")
        write_json(self.dbt / "reports/dbt_attempt.json", {"scope": "SYNTHETIC_TEST_ONLY", "status": "PASSED_DBT_NATIVE"})
        self.patch = patch.object(colab, "_require_stopped_spark")
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def destination(self):
        target = Path(self.temp.name) / "restored"
        target.mkdir()
        return target

    def test_round_trip_keeps_separate_dbt_and_delta_files(self):
        exported = colab.create_handoff(self.root, 2)
        manifest = colab.inspect_handoff(exported["archive"], expected_day=2)
        self.assertIn((self.dbt / "reports/dbt_attempt.json").relative_to(self.root).as_posix(), manifest["files"])
        target = self.destination()
        result = colab.restore_handoff(target, exported["archive"], expected_day=2)
        self.assertEqual(result["status"], "RESTORED_WITHOUT_OVERWRITE")
        again = colab.restore_handoff(target, exported["archive"], expected_day=2)
        self.assertEqual(again["files_created"], 0)

    def test_runtime_and_kafka_files_do_not_conflict_with_new_session(self):
        (self.root / "outputs/runtime_preflight.json").write_text("old")
        broker = self.root / "outputs/_kafka_runtime/broker-data"
        broker.mkdir(parents=True)
        (broker / "log").write_text("not a portable checkpoint")
        exported = colab.create_handoff(self.root, 2)
        manifest = colab.inspect_handoff(exported["archive"])
        self.assertNotIn("outputs/runtime_preflight.json", manifest["files"])
        self.assertFalse(any("_kafka_runtime" in name for name in manifest["files"]))

    def test_wrong_day_is_rejected_before_restoring(self):
        exported = colab.create_handoff(self.root, 2)
        with self.assertRaises(ValueError):
            colab.restore_handoff(self.destination(), exported["archive"], expected_day=3)

    def test_conflict_does_not_overwrite_student_work(self):
        answer = self.root / "student/day02/REFLECTION.md"
        answer.parent.mkdir(parents=True)
        answer.write_text("first answer")
        exported = colab.create_handoff(self.root, 2)
        target = self.destination()
        existing = target / "student/day02/REFLECTION.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("my later edit")
        with self.assertRaises(FileExistsError):
            colab.restore_handoff(target, exported["archive"], expected_day=2)
        self.assertEqual(existing.read_text(), "my later edit")
        self.assertFalse((target / "outputs").exists())

    def test_tampered_archive_is_rejected_without_extraction(self):
        exported = colab.create_handoff(self.root, 2)
        corrupt = Path(self.temp.name) / "corrupt.zip"
        with zipfile.ZipFile(exported["archive"]) as before, zipfile.ZipFile(corrupt, "w") as after:
            for item in before.infolist():
                payload = before.read(item.filename)
                if item.filename.endswith("dbt_attempt.json"):
                    payload = b"corrupted"
                after.writestr(item.filename, payload)
        target = self.destination()
        with self.assertRaises(ValueError):
            colab.restore_handoff(target, corrupt, expected_day=2)
        self.assertEqual(list(target.iterdir()), [])

    def test_path_traversal_with_matching_hash_is_rejected(self):
        payload = b"never extract"
        name = "outputs/../../escaped"
        malicious = Path(self.temp.name) / "unsafe.zip"
        manifest = {"format": "MASAR_HANDOFF_V1", "day": 2,
            "dataset_manifest_sha256": DATASET_MANIFEST_SHA256,
            "files": {name: {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}}}
        with zipfile.ZipFile(malicious, "w") as archive:
            archive.writestr(name, payload)
            archive.writestr(colab.MANIFEST, json.dumps(manifest))
        with self.assertRaises(ValueError):
            colab.restore_handoff(self.destination(), malicious, expected_day=2)
        self.assertFalse((Path(self.temp.name) / "escaped").exists())

    def test_drive_canonical_filename_tracks_latest_successful_save(self):
        drive = Path(self.temp.name) / "drive"
        answer = self.root / "student/day02/REFLECTION.md"
        answer.parent.mkdir(parents=True)
        answer.write_text("first answer")
        colab.save_day(self.root, 2, drive_folder=drive)
        answer.write_text("first answer and correction")
        colab.save_day(self.root, 2, drive_folder=drive)
        with zipfile.ZipFile(drive / "day02_handoff.zip") as archive:
            self.assertEqual(archive.read("student/day02/REFLECTION.md").decode(), "first answer and correction")
        self.assertTrue(list(drive.glob("day02_handoff_*.zip")))

    def test_initialized_notes_are_preserved_and_use_the_real_templates(self):
        shutil.copytree(ROOT / "templates", self.root / "templates")
        template = self.root / "templates/LAB_NOTES.md"
        template.write_text(template.read_text() + "\n[Fixture root link](../README.md)\n")
        result = colab.initialize_student_notes(self.root, 1)
        self.assertEqual(set(result["created"]), {
            "student/day01/LAB01_NOTES.md", "student/day01/LAB02_NOTES.md",
            "student/DECISIONS.md", "student/BENCHMARKS.md", "student/PROJECT_README.md"})
        note = self.root / "student/day01/LAB01_NOTES.md"
        text = note.read_text()
        self.assertIn("**Status: PENDING.**", text)
        self.assertIn("## Evidence and interpretation", text)
        self.assertIn("../../README.md", text)
        self.assertIn("`REFLECTION.md`", text)
        self.assertFalse((self.root / "student/GOVERNANCE.md").exists())
        note.write_text("My own lab observations and evidence")
        again = colab.initialize_student_notes(self.root, 1)
        self.assertEqual(again["created"], [])
        self.assertIn("student/day01/LAB01_NOTES.md", again["preserved"])
        self.assertEqual(note.read_text(), "My own lab observations and evidence")

    def test_daily_notes_survive_github_bundle_and_cumulative_restore(self):
        shutil.copytree(ROOT / "templates", self.root / "templates")
        required = set()
        for day in range(1, 6):
            result = colab.initialize_student_notes(self.root, day)
            required.update(result["created"])
            path = colab.record_reflection(self.root, day, "Test question", "", "")
            required.add(path.relative_to(self.root).as_posix())
        self.assertEqual(len([p for p in required if p.endswith("_NOTES.md")]), 8)
        self.assertIn("student/GOVERNANCE.md", required)
        note = self.root / "student/day03/LAB04_NOTES.md"
        note.write_text("My recorded correction experiment")
        github = colab.create_github_bundle(self.root, 5)
        with zipfile.ZipFile(github["archive"]) as archive:
            self.assertTrue(required <= set(archive.namelist()))
            self.assertEqual(archive.read("student/day03/LAB04_NOTES.md").decode(), note.read_text())
        handoff = colab.create_handoff(self.root, 5)
        restored = self.destination()
        colab.restore_handoff(restored, handoff["archive"], expected_day=5)
        for relative in required:
            self.assertEqual((restored / relative).read_bytes(), (self.root / relative).read_bytes())

    def test_note_initializer_rejects_symlinked_student_folder(self):
        shutil.copytree(ROOT / "templates", self.root / "templates")
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / "student").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            colab.initialize_student_notes(self.root, 1)
        self.assertEqual(list(outside.iterdir()), [])


class ReflectionTests(unittest.TestCase):
    def test_empty_attempt_can_be_filled_once_without_losing_answer(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = colab.record_reflection(root, 1, "Why?", "", "")
            colab.record_reflection(root, 1, "Why?", "My reasoning", "144 receipts")
            self.assertIn("My reasoning", path.read_text())
            self.assertIn("144 receipts", path.read_text())
            with self.assertRaises(FileExistsError):
                colab.record_reflection(root, 1, "Why?", "Replace my first answer", "")


if __name__ == "__main__":
    unittest.main()
