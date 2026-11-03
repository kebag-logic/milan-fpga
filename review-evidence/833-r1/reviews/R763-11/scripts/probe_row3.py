#!/usr/bin/env python3
"""Disposable probe mutants of owned_process.py over row 3's stubborn-parent cells.

Usage: python3 -I probe_row3.py <clean clone> <scratch dir>
Each probe copies scripts/ to scratch, applies one edit, runs --control owner_stated_seconds,
and reports rc and the failing words.
"""
import shutil, subprocess, sys
from pathlib import Path

SPARE = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
ELIF = "                elif clock < kill_all:\n"
T = "2 ** -20"
PROBES = {
    "under-only-first-census-unspared": [(SPARE, SPARE.replace("child in live", "child in live and not (self.root_notified and (child, _start) in initial and owned[pid][0] == root_pid)"))],
    "beside-only-first-census-unspared": [(SPARE, SPARE.replace("child in live", "child in live and not (self.root_notified and (child, _start) in initial and owned[pid][0] != root_pid)"))],
    "shell-first-census-parent-a-tick-early": [(SPARE, SPARE.replace("child in live", f"child in live and not (self.root_notified and (child, _start) in initial and clock >= kill_all - 2 * {T})"))],
    "under-first-census-parent-a-tick-early": [(SPARE, SPARE.replace("child in live", f"child in live and not (self.root_notified and (child, _start) in initial and owned[pid][0] == root_pid and clock >= kill_all - 2 * {T})"))],
    "shell-first-census-parent-a-pass-late": [(ELIF, "                elif clock < kill_all + (0.5 if self.root_notified and resumed is None and any((c, s) in initial and c in live for c, (p, s) in owned.items() if p == pid) else 0):\n")],
    "shell-first-census-parent-never-killed": [(ELIF, "                elif clock < kill_all or (self.root_notified and resumed is None and any((c, s) in initial and c in live for c, (p, s) in owned.items() if p == pid)):\n")],
    "under-first-census-parent-killed-at-grace": [("                    if clock < deadline + 1.0 and pid in initial.values():\n",
        "                    if clock < deadline + 1.0 and pid in initial.values() and not (self.root_notified and owned[pid][0] == root_pid and pid != root_pid):\n"),
        (SPARE, SPARE.replace("child in live", "child in live and not (self.root_notified and owned[pid][0] == root_pid and (child, _start) in initial)"))],
}

clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for name, edits in PROBES.items():
    root = scratch / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(clone / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    product.write_text(text)
    run = subprocess.run([sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py"), "--control",
                          "owner_stated_seconds"], cwd=root, capture_output=True, text=True, timeout=150)
    lines = [l for l in (run.stdout + run.stderr).splitlines() if l.strip()]
    verdict = "red" if run.returncode else "SURVIVED"
    bad += not run.returncode
    print(f"{name}: {verdict} rc {run.returncode}: {lines[-1][:260] if lines else ''}", flush=True)
print(f"probes: {len(PROBES)}, survivors: {bad}")
