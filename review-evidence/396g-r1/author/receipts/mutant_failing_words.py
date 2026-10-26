"""For each mutant added for issue #396's 2026-10-26 decisions, print the
named failing test and the first assertion line the unchanged self-test
prints against it. Only a temporary planner copy changes.

Usage: mutant_failing_words.py <repository-root>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tb" / "tools"))
import torture_release_mutants as driver  # noqa: E402

text = (root / "tb" / "tools" / "torture_campaign.py").read_text(encoding="utf-8")
start = next(i for i, m in enumerate(driver.MUTANTS) if m[0] == "soak returns to seven days")
with tempfile.TemporaryDirectory(prefix="failing-words-") as scratch:
    candidate = Path(scratch) / "torture_campaign.py"
    for name, old, new, test in driver.MUTANTS[start:]:
        assert text.count(old) == 1, name
        candidate.write_text(text.replace(old, new), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                             capture_output=True, text=True, timeout=600)
        block = run.stderr.split(f"FAIL: {test} ", 1)[1] if f"FAIL: {test} " in run.stderr else ""
        words = next((line.strip() for line in block.splitlines()
                      if re.match(r"\s*AssertionError", line)), "<no AssertionError line>")
        print(f"{name} | {test} | {words[:160]}")
