#!/usr/bin/env python3
"""Run after run_focused.py; retain the restart engine's focused regression."""
import os
from pathlib import Path
import subprocess

p = Path(__file__).resolve().parent
scratch = p / "scratch"
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), VERILATOR=str(scratch / "bounded-simulator"))
with (p / "restart-engine.log").open("w") as log:
    result = subprocess.run(["make", "-j16"], cwd=scratch / "tb/verilator/tkdiag",
                            env=env, stdout=log, stderr=subprocess.STDOUT)
(p / "restart-engine.rc").write_text(str(result.returncode) + "\n")
raise SystemExit(result.returncode)
