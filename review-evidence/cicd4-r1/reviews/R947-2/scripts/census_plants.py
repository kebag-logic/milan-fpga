#!/usr/bin/env python3
"""Reviewer's own census-union plants over copies of the retained receipts. Usage: census_plants.py CLONE UNION SCRATCH"""
import json, shutil, subprocess, sys
from pathlib import Path
clone, union, scratch = map(Path, sys.argv[1:4])
def plant(label, edit):
    root = scratch / label.replace(" ", "-"); shutil.rmtree(root, ignore_errors=True); shutil.copytree(union, root)
    edit(root)
    p = subprocess.run([sys.executable, "sw/mailbox/census_legs.py", "union", "--root", str(root)], cwd=clone,
                       capture_output=True, text=True)
    last = [l for l in (p.stdout + p.stderr).splitlines() if l.strip()][-1:]
    print(f"{label}: rc={p.returncode} {last[0][:150] if last else ''}")
    return p.returncode
def rw(root, leg, fn):
    f = root / f"census-leg-{leg}" / f"census-leg-{leg}.json"; r = json.loads(f.read_text()); fn(r); f.write_text(json.dumps(r))
def row_fail(r): r["rows"][5]["ok"] = False
def tree_other(r): r["tree"] = "0" * 40
def selected_swap(r): r["selected"] = r["selected"][1:]
codes = [plant("leg 3 row 5 failed", lambda d: rw(d, 3, row_fail)),
         plant("leg 1 other tree", lambda d: rw(d, 1, tree_other)),
         plant("leg 2 selection short", lambda d: rw(d, 2, selected_swap))]
print("all refused" if all(codes) else "ESCAPE")
sys.exit(0 if all(codes) else 1)
