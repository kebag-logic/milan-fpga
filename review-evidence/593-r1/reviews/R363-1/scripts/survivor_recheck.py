#!/usr/bin/env python3
"""R363-1: re-grade surviving and text mutants against self-test AND behave.

Usage: python3 -B survivor_recheck.py <repo-root> <scratch-dir>
Builds a disposable copy tree (tb/tools, tests) under <scratch-dir>/tree,
applies each mutation to the copy's planner, runs the planner self-test and
`behave tests/features --tags=@torture` in the copy. The repository is only read.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
repo = Path(sys.argv[1]).resolve()
tree = Path(sys.argv[2]).resolve() / "tree"
if tree.exists():
    shutil.rmtree(tree)
(tree / "tb").mkdir(parents=True)
shutil.copytree(repo / "tb" / "tools", tree / "tb" / "tools")
shutil.copytree(repo / "tests", tree / "tests")
planner = tree / "tb" / "tools" / "torture_campaign.py"
original = (repo / "tb" / "tools" / "torture_campaign.py").read_text(encoding="utf-8")

import reviewer_mutants_table as table  # noqa: E402

TEXT = [
    ("T1 tu text drops GM-minimum rule", '"after each GM change, clear + observation_resolution_s must be at least "\n', '""\n'),
    ("T2 tu text drops B.1.1 minimum and missing GM history",
     '"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "',
     '"clock validity "'),
    ("T3 mr text drops allowed cause kinds",
     '"media-clock-source change, CRF disruption, or received CRF mr toggle "', '""'),
    ("T4 mr text drops toggle and increment scope",
     '"every mr toggle and MEDIA_RESET increment needs a recorded "', '""'),
    ("T5 tu text drops discontinuity kinds (control)",
     '"GM-identity edge, GM time-source change, or other detected gPTP discontinuity "', '""'),
]


def run(cmd):
    return subprocess.run(cmd, cwd=tree, capture_output=True, text=True, timeout=900)


def grade():
    st = run([sys.executable, "-B", "tb/tools/torture_campaign.py", "--self-test"])
    bh = run([sys.executable, "-B", "-m", "behave", "tests/features", "--tags=@torture", "-f", "progress"])
    tail = [line for line in bh.stdout.splitlines() if "scenarios" in line]
    return st.returncode, bh.returncode, tail[-1] if tail else bh.stdout[-200:]


planner.write_text(original, encoding="utf-8")
base = grade()
print("BASELINE self-test rc=%s behave rc=%s [%s]" % base)
# The copy tree lacks non-planner assets, so counters_contract_milan.feature
# errors identically at baseline; a behave kill needs a failure or a changed error count.
BASE_ERRORS = int(re.search(r"(\d+) error", base[2]).group(1))
for name, old, new in table.SURVIVORS + TEXT:
    if original.count(old) != 1:
        print(f"INVALID: {name}")
        continue
    planner.write_text(original.replace(old, new), encoding="utf-8")
    st, bh, tail = grade()
    m = re.search(r"(\d+) scenarios passed, (\d+) failed, (\d+) error", tail)
    killed_bh = bool(m) and (int(m.group(2)) > 0 or int(m.group(3)) != BASE_ERRORS)
    status = "KILLED" if st or killed_bh else "SURVIVED"
    print(f"{status}: {name}: self-test rc={st} behave rc={bh} [{tail}]")
planner.write_text(original, encoding="utf-8")
