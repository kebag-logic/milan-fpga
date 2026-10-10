#!/usr/bin/env python3
"""Check that every packet path cited in backticks on the findings page exists.

Usage: cited_paths.py <findings-page.md> <packet-author-dir> <raw-index-dir>
A token counts as a path when it contains '/' or ends in a known extension.
Tokens 'cycle-NNN' expand to every cycle directory; bare file names
(msrp.tsv, acmp.tsv, analysis.json, result.json) are checked per cycle.
Raw names (snapshot-*.jsonl) are looked up in the raw indexes.
"""
import re, sys
from pathlib import Path

page, A, RI = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
text = page.read_text()
tokens = sorted(set(re.findall(r"`([^`\s]+)`", text)))
exts = (".json", ".jsonl", ".tsv", ".txt", ".csv", ".sha256", ".md")
raw = "".join(p.read_text() for p in RI.glob("*.jsonl"))
cycles = sorted(p for p in (A / "item3/cycles").iterdir() if p.is_dir())
bad = 0
for t in tokens:
    if not ("/" in t or t.endswith(exts)) or t.startswith(("http", "../", "hdl/", "tests/")):
        continue
    t2 = t.rstrip("/")
    if t2.startswith("review-evidence/608-b14-r1/"):
        p = A.parent / t2[len("review-evidence/608-b14-r1/"):]
        ok = p.exists()
    elif "cycle-NNN" in t2:
        ok = all((c / Path(t2).name).exists() for c in cycles)
    elif "/" not in t2 and t2 in ("msrp.tsv", "acmp.tsv", "analysis.json", "result.json"):
        ok = all((c / t2).exists() for c in cycles)
    elif t2.startswith("snapshot-"):
        ok = ("/" + t2 + '"') in raw
    elif t2.startswith("round2"):
        ok = (A / t2).exists()
    else:
        ok = (A / t2).exists()
    print("OK  " if ok else "MISSING", t)
    bad += not ok
# ranges named with 'to'
for a, b in re.findall(r"`(soak/console-soak-\d+\.txt)` to `(soak/console-soak-\d+\.txt)`", text):
    lo, hi = int(re.search(r"(\d+)", a).group(1)), int(re.search(r"(\d+)", b).group(1))
    miss = [n for n in range(lo, hi + 1, 5) if not (A / f"soak/console-soak-{n:03d}.txt").exists()]
    print("range", a, b, "missing:", miss)
for a, b in re.findall(r"`(item2/cyc\d+/events\.jsonl)` to `(item2/cyc\d+/events\.jsonl)`", text):
    print("range", a, b, "present:", sorted(p.parent.name for p in A.glob("item2/cyc*/events.jsonl")))
print("missing total:", bad)
