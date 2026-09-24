#!/usr/bin/env python3
"""Run one gate synchronously: output straight to receipts/<label>.log, never
piped; the real exit code, duration, command, cwd, PATH and log hash go to
receipts/<label>.json.

Usage: run_gate.py <label> [--cwd DIR] [--env K=V ...] -- <command...>
Exit code = the gate's exit code."""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "receipts"


def main() -> int:
    args = sys.argv[1:]
    label = args.pop(0)
    cwd = os.getcwd()
    env = os.environ.copy()
    extra = {}
    while args and args[0] != "--":
        flag = args.pop(0)
        if flag == "--cwd":
            cwd = args.pop(0)
        elif flag == "--env":
            key, _, value = args.pop(0).partition("=")
            env[key] = value
            extra[key] = value
        else:
            sys.exit(f"unknown flag {flag}")
    command = args[1:]
    assert command, "no command"
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / f"{label}.log"
    receipt = OUT / f"{label}.json"
    assert not log.exists() and not receipt.exists(), f"{label} already recorded"
    started = time.time()
    with log.open("wb") as stream:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                stderr=subprocess.STDOUT, check=False)
    record = {
        "label": label,
        "command": command,
        "cwd": cwd,
        "env_overrides": extra,
        "path": env.get("PATH", ""),
        "exit_code": result.returncode,
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "elapsed_seconds": round(time.time() - started, 3),
        "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
    }
    receipt.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: record[k] for k in ("label", "exit_code", "elapsed_seconds")}))
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
