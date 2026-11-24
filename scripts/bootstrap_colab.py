"""Prepare the pinned classroom runtime; never claim that setup proves a lab.

In a fresh Colab session run with --install. On an already provisioned local
test runner omit --install. No credentials or public network listeners needed.
"""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.runtime import java_major


def find_java17() -> Path | None:
    candidates = []
    if os.environ.get("JAVA_HOME"):
        candidates.append(Path(os.environ["JAVA_HOME"]))
    candidates.extend(sorted(Path("/usr/lib/jvm").glob("*17*")))
    for candidate in candidates:
        binary = candidate / "bin/java"
        if binary.is_file():
            run = subprocess.run([str(binary), "-version"], capture_output=True, text=True, timeout=10)
            if run.returncode == 0 and java_major(run.stdout + run.stderr) == 17:
                return candidate.resolve()
    return None


def prepare(install: bool = False) -> dict:
    if sys.version_info[:2] not in {(3, 11), (3, 12)}:
        raise RuntimeError(
            "This course requires Python 3.12 (or 3.11 for compatibility). "
            "In Colab choose Runtime > Change runtime type > Runtime Version: "
            "2026.07 (Python 3.12), reconnect, then run this cell again. "
            "Do not continue on Python 3.13 with the pinned dbt adapter.")
    specification = json.loads((ROOT / "runtime-target.json").read_text())
    missing = []
    for name, version in specification["packages"].items():
        try:
            found = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found = None
        if found != version:
            missing.append(f"{name}: need {version}; found {found}")
    if missing:
        if not install:
            raise RuntimeError("Install requirements-course.txt first: " + "; ".join(missing))
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
                        "-r", str(ROOT / "requirements-course.txt")], check=True)
    java_home = find_java17()
    if java_home is None:
        if not install:
            raise RuntimeError("Java 17 was not found. Set JAVA_HOME to a Java 17 installation.")
        subprocess.run(["apt-get", "update", "-qq"], check=True)
        subprocess.run(["apt-get", "install", "-y", "-qq", "openjdk-17-jre-headless"], check=True)
        java_home = find_java17()
    if java_home is None:
        raise RuntimeError("Java 17 setup did not complete.")
    os.environ["JAVA_HOME"] = str(java_home)
    from masar.runtime import require_environment
    report = require_environment()
    report.update(java_home=str(java_home), colab_runtime_candidate="2026.07",
                  meaning="Dependencies checked only. Run the labs to produce execution evidence.")
    for name, version in specification["packages"].items():
        found = importlib.metadata.version(name)
        if found != version:
            raise RuntimeError(f"Package mismatch after installation: {name}: {found} != {version}")
        report["packages"][name] = {"required": version, "observed": found}
    report["readiness"] = {
        "python_supported": sys.version_info[:2] in {(3, 11), (3, 12)},
        "java_17_selected": report["java_major"] == 17,
        "all_direct_package_pins_match": all(p["required"] == p["observed"] for p in report["packages"].values()),
        "fixed_dataset_available": (ROOT / "data/masar-small-v1/manifest.json").is_file(),
        "next_step": "Execute today's notebook cells. Package readiness does not prove any lab has run."
    }
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs/runtime_preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Install missing pins and Java 17 in Colab")
    args = parser.parse_args()
    print(json.dumps(prepare(args.install), indent=2))
