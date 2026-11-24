"""Manage the loopback-only Kafka broker for the classroom exercise."""
from pathlib import Path
import argparse
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.kafka_local import start_kafka, stop_kafka
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "stop"], default="start", nargs="?")
    args = parser.parse_args()
    print(json.dumps((start_kafka if args.action == "start" else stop_kafka)(ROOT), indent=2))
