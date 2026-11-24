"""Daily learner notes, checked handoffs and small GitHub evidence bundles.

These helpers preserve actual engine files. They do not turn saved reference
outputs into execution evidence and never automatically publish to GitHub.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile
from urllib.parse import urlsplit, urlunsplit
from masar.workspace import DATASET_MANIFEST_SHA256, completed_bronze_workspace, write_json

MANIFEST = "masar_handoff_manifest.json"
_SKIP = {"_kafka_runtime", ".ipynb_checkpoints", "__pycache__", ".git", "node_modules"}


def _day(day: int) -> str:
    if type(day) is not int or not 1 <= day <= 5:
        raise ValueError("Day must be an integer from 1 to 5")
    return f"day{day:02d}"


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record_metrics(root: Path, day: int, metrics: dict) -> Path:
    """Save observed metrics passed by a lab, never load reference answers here."""
    label = _day(day)
    if not isinstance(metrics, dict) or not metrics:
        raise ValueError("Observed metrics must be a non-empty dictionary")
    path = Path(root) / "outputs" / f"{label}_metrics.json"
    write_json(path, {"schema_version": "1.0", "day": day, "dataset": "MASAR_SMALL_V1", "metrics": metrics})
    return path


def initialize_student_notes(root: Path, day: int) -> dict:
    """Copy the real note templates once, after restoring the previous day.

    Existing learner files are never replaced. These are pending prompts, not
    generated answers or proof that a lab has been completed.
    """
    label = _day(day)
    root = Path(root).resolve()
    labs = {1: (1, 2), 2: (3,), 3: (4,), 4: (5, 6), 5: (7, 8)}
    requests = [("LAB_NOTES.md", f"student/{label}/LAB{lab:02}_NOTES.md", lab)
                for lab in labs[day]]
    requests += [(name, "student/" + name, None)
                 for name in ("DECISIONS.md", "BENCHMARKS.md", "PROJECT_README.md")]
    if day >= 4:
        requests.append(("GOVERNANCE.md", "student/GOVERNANCE.md", None))
    prepared = []
    for template_name, relative, lab in requests:
        source = root / "templates" / template_name
        destination = root / relative
        for component in [destination, *destination.parents]:
            if component == root:
                break
            if component.is_symlink():
                raise ValueError("Student notes cannot use a symlink: " + relative)
        if destination.exists():
            if not destination.is_file():
                raise ValueError("A note destination is not a file: " + relative)
            prepared.append((relative, destination, None))
            continue
        if source.is_symlink() or not source.is_file():
            raise FileNotFoundError("Required learner template is missing: " + str(source))
        text = source.read_text(encoding="utf-8")
        if lab is not None:
            text = text.replace("# Lab evidence notes", f"# Day {day} — Lab {lab:02} evidence notes", 1)
        first_line, separator, remainder = text.partition("\n")
        text = (first_line + "\n\n**Status: PENDING.** Complete the prompts with your own observations "
                "and evidence paths. This file is not a completed learner answer.\n" + separator + remainder)

        def relocate(match):
            url = urlsplit(match.group(1))
            if url.scheme or url.netloc or not url.path:
                return match.group(0)
            target = (source.parent / url.path).resolve()
            if not target.is_relative_to(root):
                raise ValueError("Template link leaves the course: " + url.path)
            relative_link = Path(os.path.relpath(target, destination.parent)).as_posix()
            return "](" + urlunsplit(("", "", relative_link, url.query, url.fragment)) + ")"

        text = re.sub(r"\]\(([^)]+)\)", relocate, text)
        if lab is not None:
            text += ("\n## Daily question\n\nKeep your daily question answer in "
                     "`REFLECTION.md` in this same folder. Use this lab note for the evidence "
                     "and interpretation requested above.\n")
        prepared.append((relative, destination, text))
    created, preserved = [], []
    for relative, destination, text in prepared:
        if text is None:
            preserved.append(relative)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with destination.open("x", encoding="utf-8") as handle:
                handle.write(text)
        except FileExistsError:
            # A concurrent save wins; never replace an existing learner file.
            preserved.append(relative)
        else:
            created.append(relative)
    return {"day": day, "created": created, "preserved": preserved,
            "reflection": f"student/{label}/REFLECTION.md",
            "instructions": "Open your note files in Colab's Files panel, replace PENDING prompts "
                "with your own evidence, and save. Keep the daily answer in REFLECTION.md. "
                "Run the final save cell after editing; both bundles include the full student folder."}


def record_reflection(root: Path, day: int, question: str, answer: str, evidence: str) -> Path:
    """Preserve a first answer; let the learner explicitly edit it afterwards."""
    label = _day(day)
    path = Path(root) / "student" / label / "REFLECTION.md"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        pending = "[Write your answer before opening the model answer.]"
        if pending in existing and answer.strip():
            existing = existing.replace(pending, answer.strip(), 1)
            if evidence.strip():
                existing = existing.replace("[Record an observed value and its report path.]", evidence.strip(), 1)
            path.write_text(existing, encoding="utf-8")
            return path
        if answer.strip() and answer.strip() not in existing:
            raise FileExistsError(f"Your reflection already exists at {path}. Edit that file to add your correction.")
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (f"# Day {day} reflection\n\n## Question\n\n{question}\n\n"
            f"## My first answer\n\n{answer.strip() or '[Write your answer before opening the model answer.]'}\n\n"
            f"## Evidence from my run\n\n{evidence.strip() or '[Record an observed value and its report path.]'}\n\n"
            "## What I corrected after discussion\n\n[Add a correction if needed, keeping your first answer.]\n")
    path.write_text(text, encoding="utf-8")
    return path


def _walk_files(folder: Path):
    if not folder.exists():
        return
    if folder.is_symlink():
        raise ValueError("Do not archive a symlinked project folder")
    for base, dirs, names in os.walk(folder, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in _SKIP)
        for name in dirs:
            if (Path(base) / name).is_symlink():
                raise ValueError("Do not archive symlinked directories")
        for name in sorted(names):
            path = Path(base) / name
            if path.is_symlink():
                raise ValueError("Do not archive symlinked files")
            if (path.suffix in {".zip", ".pyc", ".part", ".tgz"} or name.startswith(".env")
                or name.endswith(".zip.sha256")):
                continue
            if path.is_file():
                yield path


def _require_stopped_spark() -> None:
    try:
        from pyspark.sql import SparkSession
    except ImportError:
        return
    active = SparkSession.getActiveSession()
    if active is not None:
        raise RuntimeError("Stop Spark and its streaming queries before creating a handoff snapshot.")


def _safe_member(name: str) -> PurePosixPath:
    value = PurePosixPath(name)
    if (not name or "\\" in name or value.is_absolute() or ".." in value.parts
        or name != value.as_posix() or value.parts[0] not in {"outputs", "student"}):
        raise ValueError("Unsafe or unsupported handoff member: " + name)
    return value


def create_handoff(root: Path, day: int) -> dict:
    """Freeze cumulative outputs, including the separate dbt workspace.

    Source notebooks must still be saved through Colab's File menu. Kafka's
    broker process/storage is excluded; Day 5 needs the materialized Delta data.
    """
    label = _day(day)
    root = Path(root).resolve()
    _require_stopped_spark()
    work = completed_bronze_workspace(root)
    paths = sorted(p for p in {*_walk_files(root / "outputs"), *_walk_files(root / "student")}
                   if p != root / "outputs/runtime_preflight.json")
    entries = {p.relative_to(root).as_posix(): {"sha256": _sha(p), "bytes": p.stat().st_size} for p in paths}
    if "outputs/day01_bronze_success.json" not in entries or not any("/_delta_log/" in n for n in entries):
        raise ValueError("The handoff is missing actual Delta data or the workspace pointer")
    if day >= 2 and not any(n.endswith("/reports/dbt_attempt.json") for n in entries):
        raise ValueError("The cumulative handoff must retain the Day 2 dbt evidence")
    manifest = {"format": "MASAR_HANDOFF_V1", "day": day,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_manifest_sha256": DATASET_MANIFEST_SHA256,
        "workspace": work.relative_to(root).as_posix(), "files": entries,
        "not_included": ["Colab notebook editor state", "installed packages", "Kafka broker storage"],
        "kafka_recovery": "After a VM reset, rerun Day 4 from the retained Day 3 input with a new topic and checkpoint."}
    destination = root / "outputs" / f"{label}_handoff.zip"
    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".part", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in paths:
                archive.write(path, path.relative_to(root).as_posix())
            archive.writestr(MANIFEST, json.dumps(manifest, sort_keys=True, indent=2) + "\n")
        inspect_handoff(temporary, expected_day=day)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    checksum = _sha(destination)
    destination.with_suffix(".zip.sha256").write_text(checksum + "  " + destination.name + "\n")
    return {"archive": destination, "sha256": checksum, "files": len(entries), "day": day}


def inspect_handoff(archive_path: Path, *, expected_day: int | None = None) -> dict:
    """Validate all hashes and names before any extraction takes place."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or MANIFEST not in names:
            raise ValueError("Duplicate paths or a missing manifest in handoff")
        if sum(x.file_size for x in archive.infolist()) > 2 * 1024 ** 3:
            raise ValueError("Unexpectedly large handoff")
        manifest = json.loads(archive.read(MANIFEST))
        if manifest.get("format") != "MASAR_HANDOFF_V1" or manifest.get("dataset_manifest_sha256") != DATASET_MANIFEST_SHA256:
            raise ValueError("Unrecognized handoff or dataset")
        _day(manifest.get("day"))
        if expected_day is not None and manifest["day"] != expected_day:
            raise ValueError(f"Restore the Day {expected_day} handoff for this notebook")
        entries = manifest.get("files")
        if not isinstance(entries, dict) or set(names) != set(entries) | {MANIFEST}:
            raise ValueError("Handoff contents do not match the manifest")
        for name, facts in entries.items():
            _safe_member(name)
            info = archive.getinfo(name)
            if stat.S_ISLNK(info.external_attr >> 16) or info.is_dir():
                raise ValueError("Links/directories are not permitted in a handoff")
            data = archive.read(name)
            if len(data) != facts["bytes"] or hashlib.sha256(data).hexdigest() != facts["sha256"]:
                raise ValueError("Handoff hash mismatch: " + name)
        return manifest


def restore_handoff(root: Path, archive_path: Path, *, expected_day: int) -> dict:
    """Restore only into empty destinations or files with exactly the same bytes."""
    root = Path(root).resolve()
    manifest = inspect_handoff(archive_path, expected_day=expected_day)
    planned = []
    for name, facts in manifest["files"].items():
        target = root.joinpath(*_safe_member(name).parts)
        for parent in [target, *target.parents]:
            if parent == root:
                break
            if parent.is_symlink():
                raise ValueError("Restore destination contains a symlink")
        if target.exists():
            if not target.is_file() or _sha(target) != facts["sha256"]:
                raise FileExistsError("Your existing work differs; no files were overwritten: " + name)
        else:
            planned.append((name, target))
    with zipfile.ZipFile(archive_path) as archive:
        for name, target in planned:
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as source, target.open("xb") as output:
                shutil.copyfileobj(source, output)
    work = completed_bronze_workspace(root)
    return {"status": "RESTORED_WITHOUT_OVERWRITE", "day": expected_day,
            "files_created": len(planned), "workspace": work.relative_to(root).as_posix()}


def create_github_bundle(root: Path, day: int) -> dict:
    """Export readable evidence; exclude Delta binary files, secrets and caches."""
    label = _day(day)
    root = Path(root).resolve()
    folder = root / "student/results" / label
    folder.mkdir(parents=True, exist_ok=True)
    copied = []
    for path in _walk_files(root / "outputs"):
        if "_delta_log" in path.parts or path.stat().st_size > 2 * 1024 ** 2:
            continue
        if path.suffix not in {".json", ".csv"}:
            continue
        # dbt emits repeated large manifest schemas. The command report + actual
        # result records carry the inspectable evidence needed for this exercise.
        if path.name in {"manifest.json", "catalog.json", "partial_parse.msgpack"}:
            continue
        target = folder / path.relative_to(root / "outputs")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(target.relative_to(root).as_posix())
    write_json(folder / "export.json", {"day": day, "scope": "SMALL_ACTUAL_RUN_ARTIFACTS",
        "files": copied, "notebook_action": "Also use File > Save a copy in GitHub to save your executed notebook."})
    destination = root / "outputs" / f"{label}_github.zip"
    paths = list(_walk_files(root / "student"))
    # Retain the student's SQL/model definitions with the evidence, preserving
    # normal repository paths so the upload is easy to inspect.
    paths += [p for p in (root / "day02/dbt").rglob("*")
              if p.is_file() and p.suffix in {".sql", ".yml"} and not any(s in p.parts for s in {"target", "logs"})]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(paths)):
            archive.write(path, path.relative_to(root).as_posix())
    return {"archive": destination, "files": len(set(paths)), "bytes": destination.stat().st_size}


def save_day(root: Path, day: int, *, drive_folder: Path | None = None) -> dict:
    """Create the GitHub evidence package and the cumulative continuation backup."""
    github = create_github_bundle(root, day)
    handoff = create_handoff(root, day)
    result = {"day": day, "github_bundle": str(github["archive"]),
              "handoff": str(handoff["archive"]), "handoff_sha256": handoff["sha256"],
              "git_commit_created": False, "notebook_editor_saved": False}
    if drive_folder is not None:
        drive_folder = Path(drive_folder)
        drive_folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        for original in [github["archive"], handoff["archive"], handoff["archive"].with_suffix(".zip.sha256")]:
            target = drive_folder / original.name
            # Preserve the prior snapshot, then keep the canonical filename
            # pointing to the latest successful save for automatic restoration.
            if target.exists() and _sha(target) != _sha(original):
                backup = target.with_name(target.stem + "_" + stamp + target.suffix)
                shutil.copy2(target, backup)
            shutil.copy2(original, target)
        result["drive_folder"] = str(drive_folder)
    return result
