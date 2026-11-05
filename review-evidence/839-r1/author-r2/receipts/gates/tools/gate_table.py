#!/usr/bin/env python3
"""Print the lane gates' table from the rc files and logs present: gate, command, rc, the log's verdict line.

usage: gate_table.py <lane-logs dir>
The command is the log's first line (written by lane_gates.sh); the verdict is the log's last line
that reads as a tally or verdict, so the table says only what a log shows.
"""
import re, sys
from pathlib import Path

d = Path(sys.argv[1])
VERDICT = re.compile(r"(PASS|FAIL|caught|checks|passed|failed|scenarios|ok\b|OK\b|rc=|error)", re.I)
print("| Gate | Command | rc | Verdict line in the log |\n|---|---|---:|---|")
for rc in sorted(d.glob("*.rc")):
    gid = rc.stem
    log = d / f"{gid}.log"
    lines = log.read_text(errors="replace").splitlines() if log.exists() else []
    cmd = lines[0].split(": ", 1)[1] if lines and ": " in lines[0] else ""
    verdict = next((l.strip() for l in reversed(lines[1:]) if VERDICT.search(l) and len(l.strip()) < 200), "")
    print(f"| {gid} | `{cmd.replace('|', '/')}` | {rc.read_text().strip()} | {verdict.replace('|', '/')} |")
