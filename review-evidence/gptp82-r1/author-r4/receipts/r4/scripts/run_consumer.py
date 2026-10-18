#!/usr/bin/env python3
"""Run the manager's parent consumer command list in a given parent checkout.

Usage: run_consumer.py TEMPLATE PARENT OUTDIR [INDEX ...]

TEMPLATE is parent-consumer.json. PATH's first entry and VERILATOR_ROOT are
replaced by the pinned Verilator 5.050 wrapper directory and its root; the
rest of each command is the template's, word for word. Each command writes
OUTDIR/NN.log (stdout and stderr) and OUTDIR/results.json records every rc.
INDEX selects 1-based commands; default all.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

PINNED_DIR = "<tools>/pinned-verilator-5.050"
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator")
TMPDIR = "<scratch>/tmpdir"


def rewrite(word: str) -> str:
    if word.startswith("PATH="):
        rest = word[len("PATH="):].split(":", 1)[1]
        return f"PATH={PINNED_DIR}:{rest}"
    if word.startswith("VERILATOR_ROOT="):
        return f"VERILATOR_ROOT={VROOT}"
    return word


def main() -> int:
    template, parent, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pick = {int(x) for x in sys.argv[4:]}
    commands = json.loads(template.read_text())["commands"]
    out.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=parent, check=True,
                          capture_output=True, text=True).stdout.strip()
    sub = subprocess.run(["git", "-C", "gptp-processor", "rev-parse", "HEAD"], cwd=parent,
                         check=True, capture_output=True, text=True).stdout.strip()
    results = []
    worst = 0
    for i, command in enumerate(commands, 1):
        if pick and i not in pick:
            continue
        cmd = [rewrite(w) for w in command]
        cmd.insert(1, f"TMPDIR={TMPDIR}")
        log = out / f"{i:02d}.log"
        start = time.monotonic()
        with log.open("w") as fh:
            rc = subprocess.run(cmd, cwd=parent, stdout=fh, stderr=subprocess.STDOUT).returncode
        secs = round(time.monotonic() - start, 3)
        print(f"{i:02d} rc={rc} {secs}s {' '.join(command[4:])}", flush=True)
        results.append({"index": i, "command": cmd, "exit_code": rc, "seconds": secs,
                        "log": log.name})
        worst = worst or rc
    (out / "results.json").write_text(json.dumps(
        {"parent_head": head, "gptp_processor": sub, "results": results}, indent=1) + "\n")
    return worst


if __name__ == "__main__":
    sys.exit(main())
