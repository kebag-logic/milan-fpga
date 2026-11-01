#!/usr/bin/env python3
"""Split gate 1h's cost: the recipe lookup against the front-end read, on a clean clone.

usage: gate1h_cost.py <clone> <front-end-dir>; prints per-step wall times; writes nothing in the clone.
"""
import os, subprocess, sys, time, resource, shutil, tempfile
from pathlib import Path
root = Path(sys.argv[1]).resolve(); os.environ["PATH"] = sys.argv[2] + os.pathsep + os.environ["PATH"]
sys.path.insert(0, str(root / "syn/ooc"))
import dp_srcs
print("front end:", subprocess.run(["sv2v", "--version"], capture_output=True, text=True).stdout.strip())
print("load:", open("/proc/loadavg").read().strip())
ts = []
for _ in range(5):
    t = time.monotonic(); rec, bad, rc = dp_srcs.ask_authority("milan_datapath"); ts.append(time.monotonic() - t)
print("ask_authority s:", [round(x, 3) for x in ts], "sources", len(rec["src"]), "defines", rec["define"], "incdirs", len(rec["incdir"]))
rtl = (root / "hdl/milan/milan_datapath.sv").read_text()
def read(srcs):
    t = time.monotonic()
    r = subprocess.run(["sv2v", "--pass-through", *(f"-D{d}" for d in rec["define"]), "-I", str(root / "hdl/milan"),
                        *(a for i in rec["incdir"] for a in ("-I", i)), *srcs], capture_output=True, text=True, timeout=300)
    return time.monotonic() - t, r.returncode, len(r.stdout)
for name, srcs in (("whole list", rec["src"]), ("datapath alone", [str(root / "hdl/milan/milan_datapath.sv")])):
    xs = [read(srcs) for _ in range(4)]
    print(name, "s:", [round(x[0], 3) for x in xs], "rc", {x[1] for x in xs}, "stdout bytes", xs[0][2])
print("child maxrss KB:", resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
print("load:", open("/proc/loadavg").read().strip())
idx = [i for i, s in enumerate(rec["src"]) if Path(s).resolve() == (root / "hdl/milan/milan_datapath.sv").resolve()]
print("datapath position (0-based):", idx, "of", len(rec["src"]))
