#!/usr/bin/env python3
"""Print the current observation, never a suite verdict: progress.py RUN_DIR."""
import json
import sys
from pathlib import Path
r = Path(sys.argv[1])
with (r / "samples.jsonl").open("rb") as stream:
    stream.seek(max(0, stream.seek(0, 2) - 65536))
    sample = json.loads(stream.read().splitlines()[-1])
print(json.dumps(dict(elapsed_s=sample["t"], simulations=[(p["argv"], p["cpu_s"])
    for p in sample["procs"] if p["argv"] and "Vmilan" in p["argv"][0]])))
records = [line for line in (r / "milan_dp.log").read_text(errors="replace").splitlines()
           if line.startswith(("RENDER-PHASE", "[PASS]", "[FAIL]"))]
print("\n".join(records[-2:]))
if (r / "exit.json").exists():
    print((r / "exit.json").read_text())
