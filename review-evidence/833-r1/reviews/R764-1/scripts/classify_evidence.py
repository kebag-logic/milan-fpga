#!/usr/bin/env python3
"""usage: classify_evidence.py <extracted review-evidence/833-r1/author/receipts>
Reads the published raw receipts only. (1) Re-derives each captured CLEANUP
FAILED message from the raw jsonl/log sources (not the author's summary) and
classifies it: D present -> uninterruptible sleep; a T shell -> stopped shell
holding a zombie; else all Z -> zombie whose only possible parent is the owner
(a listed process's parent is the owner or another listed process).
(2) Counts each before/after run's failure kind in the final load receipts."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1])
msgs = []
for f in sorted(root.rglob("*")):
    if not f.is_file() or f.suffix not in (".jsonl", ".log") or "mutations" in f.parts:
        continue
    text = f.read_text(errors="replace")
    for line in text.splitlines():
        if "owner-survivor:" in line:
            continue  # the survivor control's own deliberate print, not a captured failure
        for raw in re.findall(r"CLEANUP FAILED: owned descendants remain after [0-9.]+ s,[^\"\n]*", line.replace("\\n", "\n")):
            msgs.append((str(f.relative_to(root)), raw.strip()))
seen, rows = set(), []
for src, m in msgs:
    if m in seen:
        continue
    seen.add(m)
    procs = re.findall(r"pid (\d+) \(([^)]*)\) state (\S) wchan (\S+) parent (\d+)", m)
    pids = {p[0] for p in procs}
    states = [p[2] for p in procs]
    if "D" in states:
        kind = "D: uninterruptible sleep after SIGKILL"
    elif "T" in states:
        kind = "T: stopped shell holding a zombie"
    else:
        kind = "Z: zombie awaiting the raising owner"
    parent_outside = sorted({p[4] for p in procs if p[4] not in pids})
    rows.append(dict(source=src, kind=kind, processes=len(procs), parents_outside_listing=parent_outside,
                     message=m[:300]))
for r in rows:
    print(json.dumps(r))
kinds = {}
for r in rows:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
print("TOTAL", len(rows), json.dumps(kinds))
print("--- final load receipts: failure kind per run")
for d in ("final-fullsuite-L48", "final-lifecycle-L48-M6", "final-suite-L48-M6"):
    for tree in ("before", "after"):
        tally = {}
        for rc in sorted((root / d / tree).glob("*.rc")):
            log = rc.with_suffix(".log").read_text(errors="replace")
            code = rc.read_text().strip()
            if code == "0":
                k = "pass"
            elif "CLEANUP FAILED" in log:
                k = "CLEANUP FAILED"
            elif "timed out after 12 seconds" in log:
                k = "fixture 12 s hang bound (Probe.finish)"
            elif "missing boundary" in log:
                k = "fixture 15 s handshake (Probe.ready)"
            else:
                k = "other rc " + code
            tally[k] = tally.get(k, 0) + 1
        print(d, tree, json.dumps(tally))
