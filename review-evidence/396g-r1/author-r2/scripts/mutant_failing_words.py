#!/usr/bin/env python3
"""For each planted defect this round adds or re-anchors, print the named
failing test and the first assertion line the unchanged self-test prints
against it. Only a temporary planner copy changes.

Usage: python3 -I mutant_failing_words.py <repository-root>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROUND_TWO = {
    "planted window need only meet the read interval", "planted window excludes its start read",
    "planted window excludes its end read", "audio control drop removed", "lone corrupted word kept as a slip pair",
    "slip size not folded around zero", "inserted silence not told apart", "swap read as corruption",
    "arm position ignored", "arms need not bracket the run", "arm edges widened to the halves",
    "fast path compares the capture with itself",
}
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tb" / "tools"))
import torture_release_mutants as driver  # noqa: E402

text = (root / "tb" / "tools" / "torture_campaign.py").read_text(encoding="utf-8")
start = next(i for i, m in enumerate(driver.MUTANTS) if m[0] == "block code bit dropped from the word")
chosen = [m for m in driver.MUTANTS[:start] if m[0] in ROUND_TWO] + list(driver.MUTANTS[start:])
with tempfile.TemporaryDirectory(prefix="failing-words-") as scratch:
    candidate = Path(scratch) / "torture_campaign.py"
    for name, old, new, test in chosen:
        assert text.count(old) == 1, name
        candidate.write_text(text.replace(old, new), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                             capture_output=True, text=True, timeout=600)
        block = run.stderr.split(f"FAIL: {test} ", 1)[1] if f"FAIL: {test} " in run.stderr else ""
        words = next((line.strip() for line in block.splitlines()
                      if re.match(r"\s*AssertionError", line)), "<no AssertionError line>")
        print(f"{name} | {test} | {words[:160]}")
print(f"{len(chosen)} planted defects")
