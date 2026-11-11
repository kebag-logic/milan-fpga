#!/usr/bin/env python3
"""sweep_launcher.py <head> <out>: wait (polling cpu_ranges.py show every 20 s, at most 4 h) until four 8-CPU ranges
are free and MemAvailable is above 30 GB, then start the full sweep as 4 native-shards units on them at once. The
shard holding capture_coherence (shard 2) gets the first 4 CPUs of its range. Writes <out>.launch.json (the ranges,
the time, native-shards' answer) or <out>.launch.timeout. Reserves nothing while it waits."""
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path

M = "<mgmt>/2026-09-23"
S = Path("<scratch>")
head, out = sys.argv[1], Path(sys.argv[2])


def ranges() -> list[str]:
    text = subprocess.run(["python3", f"{M}/cpu_ranges.py", "show"], capture_output=True, text=True).stdout
    line = [l for l in text.splitlines() if l.startswith("busy")][-1]
    lists = dict((k, ast.literal_eval(v)) for k, v in re.findall(r"(free16|free12|half8) (\[[^\]]*\])", line))
    eights = []
    for r in lists.get("half8", []):
        eights.append(r)
    for r in lists.get("free16", []):
        a, b = (int(x) for x in r.split("-"))
        eights += [f"{a}-{a + 7}", f"{a + 8}-{b}"]
    return eights


def mem_gb() -> float:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) / 1048576
    return 0.0


spec = S / "sweep-spec.json"
subprocess.run(["python3", str(S / "scripts/sweep_spec.py"), head, str(spec), str(S / "tmp-sweep-unused")], check=True)
(S / "tmp-sweep").mkdir(exist_ok=True)
deadline = time.time() + 4 * 3600
while time.time() < deadline:
    free = ranges()
    if len(free) >= 4 and mem_gb() > 30:
        cpus = free[:4]
        a = int(cpus[2].split("-")[0])
        cpus[2] = f"{a}-{a + 3}"
        r = subprocess.run(["python3", f"{M}/native-shards.py", "883-a768-sweep", str(spec), str(out), "4", *cpus],
                           capture_output=True, text=True)
        Path(f"{out}.launch.json").write_text(json.dumps(
            {"head": head, "cpus": cpus, "time": time.strftime("%FT%T%z"), "rc": r.returncode,
             "stdout": r.stdout, "stderr": r.stderr}, indent=1) + "\n")
        sys.exit(r.returncode)
    time.sleep(20)
Path(f"{out}.launch.timeout").write_text("no four free ranges within 4 h\n")
sys.exit(3)
