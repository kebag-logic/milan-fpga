#!/usr/bin/env python3
"""Build and run one milan_dp leg from the recorded `make -n run` commands.
Usage: leg.py <commands.txt> <mdir> <exe-relative-path> <log>"""
import subprocess, sys, time
from pathlib import Path
cmds_file, mdir, exe, log = sys.argv[1:5]
text = Path(cmds_file).read_text().replace("\\\n", " ")
cmds = [c.strip() for c in text.splitlines() if c.strip()]
if mdir == "obj_dir":
    build = [c for c in cmds if "verilator " in c and "--Mdir" not in c and "sim_main.cpp -o Vmilan_dp_sim" in c]
else:
    build = [c for c in cmds if "verilator " in c and f"--Mdir {mdir} " in c]
assert len(build) == 1, (mdir, len(build))
here = "$LANES/530-crf-talker-licence/tb/verilator/milan_dp"
with open(log, "w") as fh:
    t = time.time()
    fh.write(f"### build: {build[0][:300]}...\n"); fh.flush()
    rc = subprocess.run(["bash", "-c", build[0]], cwd=here, stdout=fh, stderr=subprocess.STDOUT).returncode
    fh.write(f"### build rc={rc} ({time.time()-t:.1f} s)\n"); fh.flush()
    if rc == 0:
        t = time.time()
        rc = subprocess.run([exe], cwd=here, stdout=fh, stderr=subprocess.STDOUT).returncode
        fh.write(f"### run rc={rc} ({time.time()-t:.1f} s)\n")
print(f"{mdir}: rc={rc}")
sys.exit(rc)
