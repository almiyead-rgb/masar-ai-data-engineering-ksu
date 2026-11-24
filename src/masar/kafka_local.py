"""Small native Kafka KRaft process for the interactive Day 4 classroom lab.

The broker binds to loopback only. Its storage is deliberately not a cross-VM
checkpoint. A fresh VM starts a new lab topic and query from the Day 3 state.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import subprocess
import tarfile
import time
import urllib.request

VERSION = "4.0.2"
DISTRIBUTION = f"kafka_2.13-{VERSION}"
ARCHIVE_URL = f"https://archive.apache.org/dist/kafka/{VERSION}/{DISTRIBUTION}.tgz"


def parse_sha512(text: str) -> str:
    """Accept Apache's complete hash or whitespace-separated 8/16-hex groups."""
    matches = re.findall(r"\b[0-9a-fA-F]{128}\b", text)
    if len(matches) == 1:
        return matches[0].lower()
    if matches:
        raise ValueError("Multiple Kafka SHA512 checksums")
    compact = "".join(re.findall(r"\b(?:[0-9a-fA-F]{16}|[0-9a-fA-F]{8})\b", text))
    if len(compact) != 128:
        raise ValueError("Could not parse the official Kafka SHA512 checksum")
    return compact.lower()


def _listening() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 9092), timeout=1):
            return True
    except OSError:
        return False


def _healthy() -> bool:
    from kafka.admin import KafkaAdminClient
    client = None
    try:
        client = KafkaAdminClient(bootstrap_servers="127.0.0.1:9092",
            client_id="masar-health", request_timeout_ms=5000, api_version_auto_timeout_ms=3000)
        client.list_topics()
        return True
    except Exception:
        return False
    finally:
        if client is not None:
            client.close()


def _download_distribution(cache: Path) -> Path:
    override = os.environ.get("MASAR_KAFKA_HOME")
    if override:
        home = Path(override).resolve()
        if not (home / "bin/kafka-server-start.sh").is_file():
            raise ValueError("MASAR_KAFKA_HOME does not contain a Kafka distribution")
        return home
    home = cache / DISTRIBUTION
    if (home / "bin/kafka-server-start.sh").is_file():
        return home
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / f"{DISTRIBUTION}.tgz"
    temporary = archive.with_suffix(".part")
    checksum_url = ARCHIVE_URL + ".sha512"
    with urllib.request.urlopen(checksum_url, timeout=60) as response:
        checksum_text = response.read().decode("ascii")
    expected = parse_sha512(checksum_text)
    if not archive.is_file() or hashlib.sha512(archive.read_bytes()).hexdigest() != expected:
        with urllib.request.urlopen(ARCHIVE_URL, timeout=90) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        if hashlib.sha512(temporary.read_bytes()).hexdigest() != expected:
            temporary.unlink(missing_ok=True)
            raise ValueError("Kafka download checksum mismatch")
        temporary.replace(archive)
    with tarfile.open(archive, "r:gz") as bundle:
        for member in bundle.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != DISTRIBUTION:
                raise ValueError("Unexpected path in Kafka distribution")
            if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                raise ValueError("Unexpected link or special entry in Kafka distribution")
        bundle.extractall(cache, filter="data")
    return home


def start_kafka(root: Path) -> dict:
    """Start or reuse a real local broker and wait for an API health check."""
    root = Path(root).resolve()
    runtime = root / "outputs/_kafka_runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    state = runtime / "process.json"
    if _listening():
        if not _healthy():
            raise RuntimeError("Port 9092 is occupied but Kafka is not healthy. Inspect the service before continuing.")
        return {"status": "REUSED_HEALTHY_LOCAL_BROKER", "bootstrap_servers": "127.0.0.1:9092",
                "owned": False, "broker_version_target": VERSION}
    home = _download_distribution(runtime / "distribution")
    config = runtime / "server.properties"
    log_dir = runtime / "broker-data"
    config.write_text("\n".join([
        "process.roles=broker,controller", "node.id=1",
        "controller.quorum.voters=1@127.0.0.1:9093", "controller.listener.names=CONTROLLER",
        "listeners=PLAINTEXT://127.0.0.1:9092,CONTROLLER://127.0.0.1:9093",
        "advertised.listeners=PLAINTEXT://127.0.0.1:9092",
        "listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT",
        "inter.broker.listener.name=PLAINTEXT", "num.partitions=2",
        "offsets.topic.replication.factor=1", "transaction.state.log.replication.factor=1",
        "transaction.state.log.min.isr=1", "group.initial.rebalance.delay.ms=0",
        "auto.create.topics.enable=false", "num.network.threads=2", "num.io.threads=2",
        "log.retention.hours=24", f"log.dirs={log_dir}", "" ]), encoding="utf-8")
    environment = os.environ.copy()
    environment["KAFKA_HEAP_OPTS"] = "-Xms128m -Xmx384m"
    environment["LOG_DIR"] = str(runtime / "logs")
    if not (log_dir / "meta.properties").is_file():
        cluster = subprocess.check_output([str(home / "bin/kafka-storage.sh"), "random-uuid"],
                                          env=environment, text=True, timeout=30).strip()
        subprocess.run([str(home / "bin/kafka-storage.sh"), "format", "-t", cluster, "-c", str(config)],
                       env=environment, check=True, capture_output=True, text=True, timeout=60)
    log_path = runtime / "broker.log"
    with log_path.open("a", encoding="utf-8") as log:
        process = subprocess.Popen([str(home / "bin/kafka-server-start.sh"), str(config)],
            env=environment, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    value = {"pid": process.pid, "config": str(config), "log": str(log_path),
             "bootstrap_servers": "127.0.0.1:9092", "broker_version_target": VERSION, "owned": True}
    state.write_text(json.dumps(value, indent=2) + "\n")
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Kafka stopped during startup. Read " + str(log_path))
        if _listening() and _healthy():
            return {**value, "status": "STARTED_HEALTHY_LOCAL_BROKER"}
        time.sleep(1)
    stop_kafka(root)
    raise TimeoutError("Kafka did not become healthy. Read " + str(log_path))


def stop_kafka(root: Path) -> dict:
    """Stop only a process whose saved PID still names this exact config."""
    state = Path(root).resolve() / "outputs/_kafka_runtime/process.json"
    if not state.is_file():
        return {"status": "NO_OWNED_BROKER"}
    value = json.loads(state.read_text())
    pid = value["pid"]
    try:
        command = (Path("/proc") / str(pid) / "cmdline").read_bytes().replace(b"\0", b" ").decode()
    except FileNotFoundError:
        return {"status": "ALREADY_STOPPED"}
    if value["config"] not in command or "kafka" not in command.lower():
        raise RuntimeError("Saved PID no longer identifies this Kafka process; no process was stopped")
    os.killpg(pid, signal.SIGTERM)
    return {"status": "STOP_REQUESTED", "pid": pid}
