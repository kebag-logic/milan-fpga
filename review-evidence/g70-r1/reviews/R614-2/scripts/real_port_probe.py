#!/usr/bin/env python3
"""Rename only the engine's top clock in a disposable exact-head export.

Usage: real_port_probe.py REPO PACKET [LOCK]
Runs the shipping run.sh (both tops) under one exclusive synthesis lock.
Requires Vivado settings via VIVADO_SETTINGS or the run.sh default.
"""
from datetime import datetime, timezone
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
lock = sys.argv[3] if len(sys.argv) > 3 else "$VIVADO_LOCK"
work = packet / "scratch" / "real_port_probe"
out = packet / "receipts" / "real_port_probe"
work.mkdir(parents=True, exist_ok=False)
out.mkdir(parents=True, exist_ok=True)
head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
assert head == "169073fe9751b873d140b46d4363e02ad4f56b88", head
archive = subprocess.check_output(["git", "-C", str(repo), "archive", head])
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(work, filter="data")
top = work / "hdl/top/KL_gptp_engine.sv"
text = top.read_text()
mutated, count = re.subn(r"(?<!\.)\bclk_i\b", "review_clock_i", text)
assert count >= 10, count
top.write_text(mutated)
(out / "mutation.txt").write_text(f"head={head}\nrename engine signal clk_i to review_clock_i, preserving .clk_i submodule formal ports\nreplacements={count}\n")
env = dict(os.environ, TMPDIR=str(packet / "scratch" / "tmp"), PYTHONDONTWRITEBYTECODE="1")
(out / "start.txt").write_text(datetime.now(timezone.utc).isoformat() + "\n")
with (out / "run.log").open("w") as log:
    proc = subprocess.run(["flock", "-x", "-w", "540", lock, "sh", "syn/ooc/run.sh"], cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=540)
(out / "end.txt").write_text(datetime.now(timezone.utc).isoformat() + "\n")
(out / "rc.txt").write_text(str(proc.returncode) + "\n")
for name in ("ucpu_ooc.log", "engine_ooc.log", "ucpu_timing.rpt", "engine_timing.rpt"):
    shutil.copy2(work / "syn/ooc/work" / name, out / name)
text = (out / "run.log").read_text()
words = ["ooc clock order: PASS (ooc_clock.xdc", "ooc clock order: FAIL", "CRITICAL WARNING: [Vivado 12-4739]", "session ends with 2 critical warnings", "Clock Summary is []", "not bound to clk_i", "checking no_clock reports ['4412']"]
ok = proc.returncode == 1 and all(word in text for word in words)
print(f"real engine clock rename: {'PASS' if ok else 'FAIL'} run.sh rc={proc.returncode}")
for line in text.splitlines():
    if "ooc clock order" in line or "engine_timing.rpt:" in line or "session ends" in line:
        print(line)
sys.exit(not ok)
