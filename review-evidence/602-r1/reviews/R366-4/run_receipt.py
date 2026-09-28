#!/usr/bin/env python3
"""Run one command in the foreground and record a JSON receipt plus its log.

Usage: run_receipt.py NAME TIMEOUT_S CWD -- CMD [ARGS...]
Environment variables of the form RECEIPT_ENV_<K>=<V> are passed as <K>=<V>.
The receipt records the repository HEAD of the clone named by $REVIEW_CLONE
(default: CWD), the command, rc, elapsed seconds, and the log size and SHA-256.
Logs larger than 2 MB are kept in scratch/ and only their hash is published.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PACKET = Path(__file__).resolve().parent
RECEIPTS = PACKET / "receipts"
SCRATCH_LOGS = PACKET / "scratch" / "biglogs"
LIMIT = 2 * 1024 * 1024


def main() -> int:
    name, timeout_s, cwd = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    sep = sys.argv.index("--")
    cmd = sys.argv[sep + 1:]
    env = dict(os.environ)
    extra = {k[len("RECEIPT_ENV_"):]: v for k, v in os.environ.items()
             if k.startswith("RECEIPT_ENV_")}
    env.update(extra)
    clone = os.environ.get("REVIEW_CLONE", cwd)
    head = subprocess.run(["git", "-C", clone, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    RECEIPTS.mkdir(exist_ok=True)
    start = time.monotonic()
    try:
        out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                             timeout=timeout_s)
        rc = out.returncode
        data = out.stdout + (b"\n--- stderr ---\n" + out.stderr if out.stderr else b"")
    except subprocess.TimeoutExpired as exc:
        rc = "timeout"
        data = (exc.stdout or b"") + b"\n--- TIMEOUT ---\n" + (exc.stderr or b"")
    elapsed = round(time.monotonic() - start, 2)
    digest = hashlib.sha256(data).hexdigest()
    if len(data) > LIMIT:
        SCRATCH_LOGS.mkdir(parents=True, exist_ok=True)
        log_path = SCRATCH_LOGS / f"{name}.log"
        published_log = None
    else:
        log_path = RECEIPTS / f"{name}.log"
        published_log = f"receipts/{name}.log"
    log_path.write_bytes(data)
    receipt = {"name": name, "head": head, "cwd": cwd, "cmd": cmd,
               "env_overrides": extra, "timeout_s": timeout_s, "rc": rc,
               "elapsed_s": elapsed, "log_bytes": len(data), "log_sha256": digest,
               "log": published_log}
    (RECEIPTS / f"{name}.json").write_text(json.dumps(receipt, indent=1) + "\n")
    tail = data.decode(errors="replace").splitlines()[-25:]
    print("\n".join(tail))
    print(json.dumps({k: receipt[k] for k in ("name", "rc", "elapsed_s", "log_bytes")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
