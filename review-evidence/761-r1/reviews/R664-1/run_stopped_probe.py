#!/usr/bin/env python3
"""Run after run_focused.py; use its disposable source tree and bounded compiler."""
import os
from pathlib import Path
import subprocess

p = Path(__file__).resolve().parent
scratch = p / "scratch"
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), VERILATOR=str(scratch / "bounded-simulator"))
with (p / "stopped-silence-build.log").open("w") as log:
    result = subprocess.run(["make", "-j16", "unit-build", f"CPP={p / 'probe_stopped_silence.cpp'}",
                             f"UNIT_MDIR={scratch / 'stopped-silence-build'}"],
                            cwd=scratch / "tb/verilator/crf_rx", env=env,
                            stdout=log, stderr=subprocess.STDOUT)
(p / "stopped-silence-build.rc").write_text(str(result.returncode) + "\n")
if result.returncode:
    raise SystemExit(result.returncode)
with (p / "stopped-silence.log").open("w") as log:
    result = subprocess.run([str(scratch / "stopped-silence-build/Vcrf_rx_sim")],
                            stdout=log, stderr=subprocess.STDOUT)
(p / "stopped-silence.rc").write_text(str(result.returncode) + "\n")
print("stopped-silence", result.returncode)
raise SystemExit(result.returncode)
