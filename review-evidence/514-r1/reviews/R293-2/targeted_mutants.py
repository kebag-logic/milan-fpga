#!/usr/bin/env python3
"""Targeted mutants that keep every self-test guard string intact.

    python3 -B targeted_mutants.py HEAD_SCRIPTS_DIR SCRATCH_DIR GIT_REPO
Reports the named linear example results under each mutant's self-test run.
"""
import shutil
import subprocess
import sys
from pathlib import Path

SRC, SCRATCH, REPO = (Path(a).resolve() for a in sys.argv[1:4])
ANCHOR = b"    if not (tip[0] == branch[0]\n"
MUTANTS = {
    "mode-rule-neutralised": ANCHOR, 
    "kind-and-mode-bypassed": b"    if not all(entry is None or (entry[0] in REGULAR_MODES\n",
}
INSERT = {
    "mode-rule-neutralised": b"    tip = (branch[0],) + tuple(tip[1:])\n",
    "kind-and-mode-bypassed": b"    return _merge_is_noop(original,tip,branch)\n",
}
WATCH = ("linear-mode-loss ", "linear-file-kind-change ", "linear-later-mode-change ",
         "linear-exact-retention ", "replay-10-later-exec-bit-loss")
for name, anchor in MUTANTS.items():
    work = SCRATCH / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(SRC, work)
    path = work / "merge_containment_replay.py"
    data = path.read_bytes()
    assert data.count(anchor) == 1, name
    path.write_bytes(data.replace(anchor, INSERT[name] + anchor))
    p = subprocess.run([sys.executable, "-B", str(work / "check_merge_containment.py"),
                        "--selftest"], cwd=REPO, capture_output=True, text=True,
                       errors="backslashreplace")
    print(f"== {name}: rc={p.returncode} PASS={'selftest: PASS' in p.stdout} "
          f"FAIL-lines={sum(l.startswith('  FAIL') for l in p.stdout.splitlines())}")
    for line in p.stdout.splitlines():
        if any(w in line + " " for w in WATCH):
            print("  ", line.strip())
