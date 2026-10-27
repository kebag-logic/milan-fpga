"""Transplant one self-test arm from a newer planner onto an older one and run it alone on each.

usage: python3 -I -B transplant_pin.py <old torture_campaign.py> <new torture_campaign.py> <test name> <scratch dir>
The arm's method text is cut from the new planner (from its def to the next def at the same indent) and inserted
before the old planner's test_audio_anchor_gaps_are_reported. Prints each run's outcome and failure's last lines.
"""
import os
import re
import subprocess
import sys

old_path, new_path, name, scratch = sys.argv[1:5]
new = open(new_path, encoding="utf-8").read()
start = new.index(f"    def {name}(")
end = re.compile(r"\n    (?:def |@)").search(new, start + 10).start() + 1
method = new[start:end]
old = open(old_path, encoding="utf-8").read()
anchor = "    def test_audio_anchor_gaps_are_reported("
assert old.count(anchor) == 1 and f"def {name}(" not in old
os.makedirs(scratch, exist_ok=True)
target = os.path.join(scratch, "torture_campaign.py")
open(target, "w", encoding="utf-8").write(old.replace(anchor, method + "\n" + anchor))
DRIVER = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
class T(t._ReleaseGateChecks, unittest.TestCase):
    pass
result = unittest.TestResult()
T(sys.argv[2]).run(result)
problems = result.failures + result.errors
print("FAIL" if result.failures else "ERROR" if result.errors else "ok")
for line in (problems[0][1].strip().splitlines()[-3:] if problems else []):
    print("  " + line[:300])
"""
for label, directory in (("old planner with the arm", scratch), ("new planner", os.path.dirname(new_path))):
    run = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, directory, name], capture_output=True, text=True,
                         timeout=600)
    print(f"{label}: {run.stdout.strip() or run.stderr.strip()[-300:]}")
