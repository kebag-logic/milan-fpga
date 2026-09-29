#!/usr/bin/env python3
"""Scratch: run ONE gate command in a tree, log it, append a JSON result line.

usage: gate.py <tree> <results.jsonl> <logdir> <label> -- <command...>
The pinned Verilator 5.050 is put first on PATH. The log is kept in <logdir>
(scratch); the result line records rc, seconds, log bytes and log SHA-256.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

VBIN = "$VALIDATION_TOOLS/verilator-v5.050/bin"


def main() -> int:
    sep = sys.argv.index("--")
    tree, results, logdir, label = sys.argv[1:sep]
    cmd = sys.argv[sep + 1:]
    env = dict(os.environ)
    env["PATH"] = VBIN + os.pathsep + env.get("PATH", "")
    Path(logdir).mkdir(parents=True, exist_ok=True)
    log = Path(logdir) / f"{label}.log"
    start = time.monotonic()
    with log.open("wb") as stream:
        rc = subprocess.run(cmd, cwd=tree, env=env, stdout=stream,
                            stderr=subprocess.STDOUT, check=False).returncode
    data = log.read_bytes()
    rec = {"label": label, "tree": tree, "cmd": " ".join(cmd), "rc": rc,
           "seconds": round(time.monotonic() - start, 1), "log_bytes": len(data),
           "log_sha256": hashlib.sha256(data).hexdigest()}
    with open(results, "a") as out:
        out.write(json.dumps(rec) + "\n")
    print(json.dumps(rec))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
