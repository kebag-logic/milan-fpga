#!/usr/bin/env python3
"""Run named gates in order; record rc, seconds, log size and sha256.

Usage: run_gates.py <lane> <gates.json> <log dir> <summary.tsv>
gates.json: [{"name": .., "argv": [..], "cwd": "<lane-relative>"?, "env": {..}?,
              "timeout": s?}]
Each gate's stdout and stderr go to <log dir>/<name>.log, never through a pipe,
so the recorded rc is the command's own. `$LANE` in argv and env is the lane.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    """Run every gate; exit 1 when any rc is non-zero."""
    lane, spec, logdir, summary = (Path(arg) for arg in sys.argv[1:5])
    logdir.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()
    bad = 0
    rows = []
    for gate in json.loads(spec.read_text()):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        env.update({k: v.replace("$LANE", str(lane)) for k, v in gate.get("env", {}).items()})
        argv = [a.replace("$LANE", str(lane)) for a in gate["argv"]]
        log = logdir / f"{gate['name']}.log"
        start = time.monotonic()
        with log.open("w") as out:
            try:
                rc = subprocess.run(argv, cwd=lane / gate.get("cwd", "."), env=env, stdout=out,
                                    stderr=subprocess.STDOUT, timeout=gate.get("timeout", 7200)).returncode
            except subprocess.TimeoutExpired:
                rc = "timeout"
        seconds = time.monotonic() - start
        data = log.read_bytes()
        rows.append((gate["name"], " ".join(argv).replace(str(lane), "$LANE"), str(rc), f"{seconds:.1f}",
                     str(len(data)), hashlib.sha256(data).hexdigest()))
        bad += rc != 0
        print(f"{gate['name']}: rc={rc} {seconds:.1f}s", flush=True)
    now = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"], capture_output=True, text=True,
                         check=True).stdout.strip()
    with summary.open("a") as out:
        out.write(f"# head {head} (after the run: {now})\n")
        out.write("name\tcommand\trc\tseconds\tlog_bytes\tlog_sha256\n")
        for row in rows:
            out.write("\t".join(row) + "\n")
    print(f"head {head}; after {now}; non-zero: {bad}")
    return int(bad != 0 or head != now)


if __name__ == "__main__":
    sys.exit(main())
