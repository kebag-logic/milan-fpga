#!/usr/bin/env python3
"""Check the recorded route sets' report bytes against the author's published route-reports.tsv.
usage: verify_routes.py <route-reports.tsv>"""
import hashlib, os, sys
from pathlib import Path
S = Path(os.environ["VALIDATION_STORAGE"]) / "scratch"
ROOT = {"dev-1e80128f": S / "814-a703/viv-dev/w1", "head-8b28ebaf": S / "814-a703b/w-h1", "control-c1": S / "814-a703b/w-c1"}
ok = bad = 0
for row in Path(sys.argv[1]).read_text().splitlines()[1:]:
    label, d, name, size, sha = row.split("\t")
    data = (Path(ROOT[label]) / d / name).read_bytes()
    if len(data) == int(size) and hashlib.sha256(data).hexdigest() == sha: ok += 1
    else: bad += 1; print("MISMATCH", label, d, name)
print(f"route reports: {ok} match, {bad} differ")
