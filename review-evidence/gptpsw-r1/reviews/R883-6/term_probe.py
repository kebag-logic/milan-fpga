#!/usr/bin/env python3
"""Scan the two delta files at the predecessor and head commits with the checker's own class-R
regex (RUNTIME_RE) and print every hit. Usage: python3 term_probe.py <checkout> <old> <new>"""
import subprocess
import sys
from pathlib import Path

root, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
sys.path.insert(0, str((root / "scripts").resolve()))
import check_baremetal_only as c  # noqa: E402

FILES = ("sw/firmware/ctrl/test/test_aecp.cpp", "sw/firmware/ctrl/test/aecp_face_mutants.py")
for rev in (old, new):
    for f in FILES:
        text = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{f}"],
                              check=True, capture_output=True, text=True).stdout
        hits = [(n, m.group(0)) for n, line in enumerate(text.splitlines(), 1)
                for m in c.RUNTIME_RE.finditer(line)]
        print(f"{rev[:10]} {f}: {len(hits)} class-R hit(s) {hits}")
