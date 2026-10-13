#!/usr/bin/env python3
"""Run permitted focused gates concurrently; never execute the runner on host."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    root, packet = args.root.resolve(), args.packet.resolve()
    scratch = packet / "scratch" / "tmp"
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
    tasks = [("scope", ["python3", "-B", "scripts/ci_scope.py", "--selftest"]), ("events-check", ["python3", "-B", "scripts/ci_events.py", "--check"]), ("events-selftest", ["python3", "-B", "scripts/ci_events.py", "--selftest"])]

    def run(task):
        name, command = task
        start = time.monotonic()
        with (packet / f"{name}.log").open("w") as log:
            result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=550, check=False)
        receipt = {"command": command, "head": "7c862ad980dfe829ef4d85ff8f4fb4fab451984f", "returncode": result.returncode, "elapsed_seconds": round(time.monotonic() - start, 3)}
        (packet / f"{name}.json").write_text(json.dumps(receipt, indent=2) + "\n")
        (packet / f"{name}.rc").write_text(str(result.returncode) + "\n")
        print(json.dumps(receipt), flush=True)
        return result.returncode

    with ThreadPoolExecutor(max_workers=3) as pool:
        codes = list(pool.map(run, tasks))
    raise SystemExit(any(codes))


if __name__ == "__main__":
    main()
