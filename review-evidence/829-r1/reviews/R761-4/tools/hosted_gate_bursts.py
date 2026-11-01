#!/usr/bin/env python3
"""Bound gate 1h on one hosted job from its log's output bursts.

The driver's output reaches the log in buffered bursts, so a gate has no timestamp
of its own. Two runs are comparable where the burst holding the gate opens and
closes on the same lines; the gain between the bursts is then the change in that
stretch of gates.

usage: hosted_gate_bursts.py <job id> [<job id> ...]
"""
import re, subprocess, sys
for job in sys.argv[1:]:
    text = subprocess.run(["gh", "api", "--allow-escape-sequences",
                           f"repos/kebag-logic/milan-fpga/actions/jobs/{job}/logs"],
                          capture_output=True, text=True, check=True, errors="replace").stdout
    lines = [re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", line) for line in text.splitlines()]
    mark = next(i for i, line in enumerate(lines) if "[gate 1h mutation]" in line)
    first = mark
    while lines[first - 1][:19] == lines[mark][:19]:
        first -= 1
    last = mark
    while lines[last + 1][:19] == lines[mark][:19]:
        last += 1
    print(job, "| before", lines[first - 1][:19], "| burst", lines[mark][:19],
          "| opens", lines[first][28:].strip(), "| closes", lines[last][28:].strip(),
          "|", lines[mark][28:].strip())
