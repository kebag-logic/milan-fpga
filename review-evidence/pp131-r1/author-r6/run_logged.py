#!/usr/bin/env python3
"""Run one command to completion in a directory and record it.

The command runs with the pinned Verilator wrapper first on PATH (the manager's
bank environment). Its output goes to <out>/<name>.log; one JSON line with the
exit status, seconds, log size and log SHA-256 is appended to <out>/results.jsonl.
Usage: run_logged.py <out> <name> <cwd> <command> [args ...]
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PINNED = "$VALIDATION_STORAGE/pp131-manager-84572585/pinned-tool-bin"
VROOT = ("$WORKSPACE_HOME/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator")


def main():
    out, name, cwd, cmd = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), sys.argv[4:]
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH=PINNED + ":" + os.environ["PATH"], VERILATOR_ROOT=VROOT)
    log = out / f"{name}.log"
    start = time.monotonic()
    with log.open("wb") as stream:
        rc = subprocess.run(cmd, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT,
                            env=env, check=False).returncode
    data = log.read_bytes()
    row = {"name": name, "cwd": str(cwd), "command": cmd, "rc": rc,
           "seconds": round(time.monotonic() - start, 1), "log": log.name,
           "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    with (out / "results.jsonl").open("a") as rec:
        rec.write(json.dumps(row) + "\n")
    print(json.dumps(row), flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
