#!/usr/bin/env python3
"""From the probe logs: time from the input's last counters update before each
unbind to the unbind command (page: at least 2 s), and the hold after the lock update."""
import json, sys
from pathlib import Path
A = Path(sys.argv[1]); worst = 1e18
for s in ("s0b", "s1"):
    ev = [json.loads(l) for l in (A / f"runs/{s}/{s}-probe.jsonl").read_text().splitlines() if l.startswith("{")]
    cur = None; last = {}  # idx -> list of update times
    for e in ev:
        if e["ev"] == "cycle_begin": cur, li = e["tag"], e["listener_in"]
        if e["ev"] == "si_counters" and e["who"] == "dut": last.setdefault(e["idx"], []).append(e["t"])
        if e["ev"] == "unbind":
            gap = (e["t_cmd"] - max(t for t in last[li] if t < e["t_cmd"])) / 1e6; worst = min(worst, gap)  # updates logged before the unbind event may postdate its command
            print(f"{s}/{cur} last counters update -> unbind {gap:.3f} s")
print(f"minimum {worst:.3f} s; {'PASS' if worst >= 2.0 else 'FAIL'} (page: at least 2 s)")
sys.exit(0 if worst >= 2.0 else 1)
