#!/usr/bin/env python3
"""Run one gate in the foreground; record its own rc, duration and output.

usage: run_gate.py <name> <cwd> <command...>
Appends {name, cwd, command, rc, seconds, head} to gates.jsonl beside this
script and writes the combined output to gates/<name>.log. Exits with the
gate's rc so a caller sees the verdict unchanged.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PIN = "$VALIDATION_TOOLS/verilator-v5.050/bin"


def main() -> int:
    name, cwd, command = sys.argv[1], sys.argv[2], sys.argv[3:]
    logs = HERE / "gates"
    logs.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["PATH"] = PIN + ":" + env.get("PATH", "/usr/bin:/bin")
    head = subprocess.run(["git", "-C", cwd, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    start = time.monotonic()
    with (logs / (name + ".log")).open("w") as out:
        rc = subprocess.run(command, cwd=cwd, env=env, stdout=out,
                            stderr=subprocess.STDOUT).returncode
    record = {"name": name, "cwd": cwd, "command": command, "rc": rc,
              "seconds": round(time.monotonic() - start, 2), "head": head}
    with (HERE / "gates.jsonl").open("a") as j:
        j.write(json.dumps(record) + "\n")
    print(json.dumps(record))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
