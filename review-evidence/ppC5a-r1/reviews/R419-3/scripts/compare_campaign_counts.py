#!/usr/bin/env python3
"""Compare each arm's failing-check count in a campaign log with its README cell.

Usage: compare_campaign_counts.py README.md SECTION_HEADING LOG [LOG...]
The README table's arm cell may name several arms (`a`, `-suffix`); the count
cell starts with an integer N or reads "the same N". A log line is
'<arm>: rc=R failures=F named=K KILLED|UNPROVEN'.
"""
import re, sys

readme, heading, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
measured = {}
for log in logs:
    for ln in open(log, errors="replace"):
        m = re.match(r"^([a-z0-9-]+): rc=(\d+) failures=(\d+) named=(\d+) (KILLED|UNPROVEN)", ln)
        if m:
            measured[m.group(1)] = (int(m.group(3)), int(m.group(4)), m.group(5))
text = open(readme).read()
sec = text.split(heading, 1)[1].split("\n### ", 1)[0]
expected = {}
for row in sec.splitlines():
    if not row.startswith("| `"):
        continue
    cells = [c.strip() for c in row.strip("|").split("|")]
    names = re.findall(r"`([^`]+)`", cells[0])
    cnt = re.match(r"(?:the same )?(\d+)", cells[-1])
    if not names or not cnt:
        continue
    n = int(cnt.group(1))
    first = names[0]
    for nm in names:
        if nm.startswith("-"):
            cands = [a for a in measured if a.endswith(nm) and a[:8] == first[:8]]
            nm = cands[0] if len(cands) == 1 else first + nm
        expected[nm] = n
ok = bad = 0
for arm in sorted(set(expected) | set(measured)):
    e = expected.get(arm)
    m = measured.get(arm)
    status = "OK" if (m and e == m[0] and m[2] == "KILLED" and m[1] >= 1) else "MISMATCH"
    ok += status == "OK"
    bad += status != "OK"
    print(f"{status:8} {arm:40} readme={e} measured={m}")
print(f"{ok} equal, {bad} not equal or missing")
sys.exit(1 if bad else 0)
