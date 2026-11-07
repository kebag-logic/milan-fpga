#!/usr/bin/env python3
"""Sizing trials on a disposable export: can survivors be killed at zero line cost?

Usage: trial_kills.py REPO HEAD SCRATCH
"""
import shutil, subprocess, sys
from pathlib import Path
repo, head, scratch = sys.argv[1], sys.argv[2], Path(sys.argv[3])
GEN = "scripts/docs_inventory.py"
CELL = 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked else "area lane"'
D0_FIRST = 'verified = "D0" if path in checked else "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'
ARM_OLD = '("archive page is obsolete with its successor", lambda root: None, 0,'
ARM_NEW = '("archive is obsolete", edit_data(lambda d: d["verified_pages"].append("docs/history/v1/OLD.md")), 0,'
SAYS_OLD = '("a D0 page that left the tree", lambda root: (root / "README.md").unlink(), 2, "", "verified_pages"),'
SAYS_NEW = '("a D0 page that left the tree", lambda root: (root / "README.md").unlink(), 2, "", "update it when"),'
ADVICE = "`verified_pages` must list tracked pages; update it when a listed page moves or leaves"

def case(name, edits):
    work = scratch / "trial"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    subprocess.run(f"git -C {repo} archive {head} | tar -x -C {work}", shell=True, check=True)
    path = work / GEN
    text = path.read_text(encoding="utf-8")
    for old, new in edits:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    r = subprocess.run(["python3", str(path), "--selftest"], cwd=work, capture_output=True, text=True)
    last = (r.stdout + r.stderr).strip().splitlines()[-1][:150]
    print(f"{name}: selftest rc {r.returncode}; lines {text.count(chr(10))}; max col {max(map(len, text.splitlines()))}; {last}")
    shutil.rmtree(work, ignore_errors=True)

needles = [(ARM_OLD, ARM_NEW), (SAYS_OLD, SAYS_NEW)]
case("T0 head unchanged", [])
case("T1 arm and needle changed, generator unchanged", needles)
case("T2 same, plus D0 tested before archive", needles + [(CELL, D0_FIRST)])
case("T3 same, plus refusal loses its advice", needles + [(ADVICE, "`verified_pages` is bad")])
