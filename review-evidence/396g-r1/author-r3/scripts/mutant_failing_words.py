#!/usr/bin/env python3
"""For each planted defect this round adds or re-anchors, print the named
failing test and the first assertion line the unchanged self-test prints
against it. Only a temporary planner copy changes; defects run in parallel.

Usage: python3 -I mutant_failing_words.py <repository-root> [jobs]
"""
import concurrent.futures
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RE_ANCHORED = {"inserted silence not told apart"}
root = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
sys.path.insert(0, str(root / "tb" / "tools"))
import torture_release_mutants as driver  # noqa: E402

text = (root / "tb" / "tools" / "torture_campaign.py").read_text(encoding="utf-8")
start = next(i for i, m in enumerate(driver.MUTANTS) if m[0] == "qualified interval runs to the capture's end")
chosen = [m for m in driver.MUTANTS[:start] if m[0] in RE_ANCHORED] + list(driver.MUTANTS[start:])


def words(mutant: tuple) -> str:
    name, old, new, test = mutant
    assert text.count(old) == 1, name
    with tempfile.TemporaryDirectory(prefix="failing-words-") as scratch:
        candidate = Path(scratch) / "torture_campaign.py"
        candidate.write_text(text.replace(old, new), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                             capture_output=True, text=True, timeout=600)
    block = run.stderr.split(f"FAIL: {test} ", 1)[1] if f"FAIL: {test} " in run.stderr else ""
    found = next((line.strip() for line in block.splitlines()
                  if re.match(r"\s*AssertionError", line)), "<no AssertionError line>")
    return f"{name} | {test} | rc={run.returncode} | {found[:160]}"


with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(words, chosen):
        print(line, flush=True)
print(f"{len(chosen)} planted defects")
