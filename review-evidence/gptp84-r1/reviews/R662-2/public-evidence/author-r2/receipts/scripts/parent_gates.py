#!/usr/bin/env python3
"""Run the manager's full parent consumer gate list in one parent tree.

usage: parent_gates.py <template.json> <parent-tree> <logdir> [first last]

Takes the command list of the manager template, drops its `env` prefix and
reruns each command in <parent-tree> with the same PATH shape (the pinned
Verilator first) and VERILATOR_ROOT. Writes <logdir>/NN.log per command and
<logdir>/rc.txt with one "NN rc=R secs=S cmd" line each. Commands run in
the foreground, one after another.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

PINNED_BIN = "<pinned-tools>"


def main() -> int:
    template = json.loads(Path(sys.argv[1]).read_text())
    tree = Path(sys.argv[2])
    logdir = Path(sys.argv[3])
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    last = int(sys.argv[5]) if len(sys.argv) > 5 else len(template["commands"])
    logdir.mkdir(parents=True, exist_ok=True)
    worst = 0
    for i, cmd in enumerate(template["commands"], start=1):
        if not first <= i <= last:
            continue
        env = dict(os.environ)
        argv = list(cmd)
        if argv[0] == "env":
            argv = argv[1:]
            while "=" in argv[0]:
                key, value = argv.pop(0).split("=", 1)
                env[key] = value
        env["PATH"] = PINNED_BIN + ":" + env["PATH"].split(":", 1)[1]
        env["TMPDIR"] = "<scratch>/tmpdir"
        start = time.time()
        with open(logdir / f"{i:02d}.log", "w", encoding="utf-8") as log:
            rc = subprocess.run(argv, cwd=tree, env=env, stdout=log,
                                stderr=subprocess.STDOUT).returncode
        secs = int(time.time() - start)
        line = f"{i:02d} rc={rc} secs={secs} {' '.join(argv)}"
        with open(logdir / "rc.txt", "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line, flush=True)
        worst = worst or rc
    return 1 if worst else 0


if __name__ == "__main__":
    sys.exit(main())
