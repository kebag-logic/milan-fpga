#!/usr/bin/env python3
"""Print each REQ_TAG under tb/ with the statement that follows it (C++) or the
enclosing def (Python), and the enclosing control lines just above, for sampling.
usage: tag_context.py REPO"""
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
files = subprocess.run(["git", "-C", str(root), "ls-files", "tb"], capture_output=True,
                       text=True, check=True).stdout.split()
TAG = re.compile(r'REQ_TAG\("(REQ-[A-Z]+-\d{3})", "([A-Z]+)", "([^"]+)"\)')
for f in files:
    if f.startswith("tb/common/"): continue
    lines = (root / f).read_text(errors="replace").splitlines()
    for i, l in enumerate(lines):
        m = TAG.search(l)
        if not m: continue
        j = i + 1
        while j < len(lines) and TAG.search(lines[j]): j += 1
        stmt = []
        for k in range(j, min(j + 8, len(lines))):
            stmt.append(lines[k].strip())
            if lines[k].rstrip().endswith(";") or f.endswith(".py"): break
        print(f"{f}:{i+1} {m[1]} {m[2]} [{m[3]}]\n    PREV: {lines[i-1].strip()[:160]}\n    NEXT: {' '.join(stmt)[:400]}")
