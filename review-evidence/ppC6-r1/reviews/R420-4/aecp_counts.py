#!/usr/bin/env python3
"""Compare the failure counts printed by aecp_mutants.py / aecp_dispatch_mutants.py
per-arm logs in the campaign output directories (FAIL: lines) with the README record rows
("| `ARM` | ... | K: ..."). usage: aecp_counts.py README OUTDIR..."""
import re, sys
rec = {}
for line in open(sys.argv[1]):
    m = re.match(r"^\| `([a-z0-9-]+)` \|.*\| (\d[\d,]*)(?::| |\b)", line)
    if m:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        n = re.match(r"(\d[\d,]*)", cells[-1])
        if n:
            rec.setdefault(m.group(1), int(n.group(1).replace(",", "")))
import pathlib
got = {}
for d in sys.argv[2:]:
    for log in sorted(pathlib.Path(d).glob("*.log")):
        if log.name.startswith("control-"):
            continue
        text = log.read_text(errors="replace")
        fails = sum(1 for l in text.splitlines() if l.startswith("FAIL:"))
        got[log.stem] = (fails, "KILLED" if fails and "checks" in text else "UNPROVEN")
diff = 0
for arm, (n, v) in sorted(got.items()):
    ok = rec.get(arm) == n
    diff += not ok
    print(f"{'OK ' if ok else 'DIFF'} {arm}: {v} failures {n} README {rec.get(arm)}")
print(f"{len(got)} arms, {sum(v == 'KILLED' for _, v in got.values())} KILLED, {diff} count differences")
