#!/usr/bin/env python3
"""gate_launcher.py <head> <base> <root> <group> ...: for each group in order, wait (polling cpu_ranges.py show every
20 s, at most 6 h in all) until an 8-CPU range is free and MemAvailable is above 20 GB, then start that group's
workflow replay (wf_all.sh) as its own unit, milan-883-a768-gates-<group>, on that range, MemoryMax 10G. Records each
start in <root>/launch.tsv. Reserves nothing while it waits: a range is booked by the unit that runs on it."""
import ast
import re
import subprocess
import sys
import time
from pathlib import Path

M = "<mgmt>/2026-09-23"
S = Path("<scratch>")
head, base, root, groups = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4:]


def free_eights() -> list[str]:
    text = subprocess.run(["python3", f"{M}/cpu_ranges.py", "show"], capture_output=True, text=True).stdout
    line = [l for l in text.splitlines() if l.startswith("busy")][-1]
    lists = dict((k, ast.literal_eval(v)) for k, v in re.findall(r"(free16|free12|half8) (\[[^\]]*\])", line))
    eights = list(lists.get("half8", []))
    for r in lists.get("free16", []):
        a, b = (int(x) for x in r.split("-"))
        eights += [f"{a}-{a + 7}", f"{a + 8}-{b}"]
    return eights


def mem_gb() -> float:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) / 1048576
    return 0.0


root.mkdir(parents=True, exist_ok=True)
deadline = time.time() + 6 * 3600
for group in groups:
    while time.time() < deadline:
        free = free_eights()
        if free and mem_gb() > 20:
            cpus = free[0]
            log = root / f"unit-{group}.log"
            subprocess.run(["systemd-run", "--user", "--quiet", "--collect", f"--unit=milan-883-a768-gates-{group}",
                            "-p", "MemoryMax=10G", "-p", f"CPUAffinity={cpus}", "bash", "-c",
                            f"bash {S}/scripts/wf_all.sh {head} {base} {root} {group} > {log} 2>&1; "
                            f"echo $? > {log}.rc"], check=True)
            with open(root / "launch.tsv", "a") as t:
                t.write(f"{group}\t{cpus}\t{time.strftime('%FT%T%z')}\n")
            time.sleep(30)          # let cpu_ranges see the new unit's affinity before the next pick
            break
        time.sleep(20)
    else:
        with open(root / "launch.tsv", "a") as t:
            t.write(f"{group}\tTIMEOUT\t{time.strftime('%FT%T%z')}\n")
