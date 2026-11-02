#!/usr/bin/env python3
"""Feasibility: one more listing in owner_stated_seconds pins a resume inside grace after pass 1 (review probe).

Usage: python3 -I rv7_pin_feasibility.py <repo> <scratch>
Copies <repo>/scripts under <scratch>, adds a resume at 1 s (child gone at 1 s, trap's command listed
from then) to owner_stated_seconds, and runs that control unmutated and under each rv7 mutant.
"""
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
ANCHOR = '        kept("a first-pass resume", resumed_at(0), window(0), shell)\n'
EXTRA = ANCHOR + '        kept("an in-grace resume", resumed_at(1), window(1), shell)\n'
NEW = "                    if (pid, start) not in initial:\n                        continue\n                elif"
MUTANTS = {
    "none": None,
    "rv7-sigterm-trap-command-later-grace-resume": (NEW,
        "                    if (pid, start) not in initial and not (resumed is not None and resumed > 0):\n"
        "                        continue\n                elif"),
    "rv7-no-resume-later-in-grace": ("and root_pid in owned and not (live - {root_pid}):",
        "and root_pid in owned and not (live - {root_pid}) and not (passes > 1 and clock < deadline):"),
    "rv7-no-window-later-in-grace": ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
        "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline or passes == 1 else kill_all"),
}
bad = 0
for name, edit in MUTANTS.items():
    root = scratch / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(repo / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    test = root / "scripts/test_suite_cancellation.py"
    text = test.read_text()
    assert text.count(ANCHOR) == 1
    test.write_text(text.replace(ANCHOR, EXTRA))
    if edit:
        product = root / "scripts/owned_process.py"
        text = product.read_text()
        assert text.count(edit[0]) == 1, name
        product.write_text(text.replace(*edit))
    run = subprocess.run([sys.executable, "-B", str(test), "--control", "owner_stated_seconds"], cwd=root,
                         capture_output=True, text=True, timeout=120)
    last = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()][-1]
    want_red = edit is not None
    ok = bool(run.returncode) == want_red and (not want_red or "an in-grace resume" in last)
    bad += not ok
    print(f"{name}: rc {run.returncode} {'OK' if ok else 'UNEXPECTED'}: {last[:260]}", flush=True)
print(f"pin feasibility: {'PASS' if not bad else 'FAIL'}")
sys.exit(1 if bad else 0)
