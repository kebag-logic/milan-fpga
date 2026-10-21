#!/usr/bin/env python3
"""Base vs head campaign logs, normalized as compare.py does, then sorted, so the
order in which parallel arms finish does not count; the work-directory
paths are tokenized too.

usage: compare_sorted.py <base dir> <head dir> <out dir>
"""
import csv, difflib, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
spec = importlib.util.spec_from_file_location("cmp", Path(__file__).resolve().parent / "compare.py")
EXTRA = [(re.compile(r"<scratch>/r[23]/rec/[A-Za-z0-9_-]+/work/"), "<work>/")]


def norm(text):
    out = []
    for line in text.splitlines():
        for rx, tok in NORM + EXTRA:
            line = rx.sub(tok, line)
        out.append(line)
    return sorted(out)


src = (Path(__file__).resolve().parent / "compare.py").read_text()
NORM = eval(src.split("NORM = ", 1)[1].split("\n]\n", 1)[0] + "\n]", {"re": re})
base, head, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
rows = []
for hl in sorted(head.glob("*.log")):
    bl = base / hl.name
    if not bl.exists():
        rows.append((hl.stem, "head only"))
        continue
    d = list(difflib.unified_diff(norm(bl.read_text(errors="replace")), norm(hl.read_text(errors="replace")),
                                  "base/" + hl.name, "head/" + hl.name, lineterm="", n=0))
    (out / (hl.stem + ".sorted.diff")).write_text("\n".join(d) + ("\n" if d else ""))
    n = sum(1 for x in d if x[:1] in "+-" and x[:3] not in ("+++", "---"))
    rows.append((hl.stem, "identical" if not d else f"{n} lines differ"))
with (out / "SUMMARY-sorted.csv").open("w", newline="") as fh:
    csv.writer(fh).writerows([("log", "normalized and sorted, base vs head")] + rows)
print("ok")
