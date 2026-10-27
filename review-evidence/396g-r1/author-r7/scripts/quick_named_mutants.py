#!/usr/bin/env python3
"""Apply named release controls to a temporary planner copy and run only each one's named arm.

Usage: python3 -I quick_named_mutants.py <tb/tools dir> <jobs> [defect name]...

Reads the driver's MUTANTS table from <tb/tools dir>/torture_release_mutants.py
(the audio entries included) and, for each named defect, or every entry when
none is named, runs the named arm alone on a mutated copy. KILLED needs the
arm to fail; the full-suite criterion is the driver's. It prints the failure's
last AssertionError line (the outermost) and the end of its message.
"""
import importlib.util
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tools = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
sys.path.insert(0, str(tools))
spec = importlib.util.spec_from_file_location("release_mutants", tools / "torture_release_mutants.py")
table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table)
text = (tools / "torture_campaign.py").read_text(encoding="utf-8")
names = set(sys.argv[3:]) or None
DRIVER = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
class T(t._ReleaseGateChecks, unittest.TestCase):
    pass
result = unittest.TestResult()
T(sys.argv[2]).run(result)
problems = result.failures + result.errors
lines = [line for line in problems[0][1].strip().splitlines() if line.strip()] if problems else []
first = ([line for line in lines if line.startswith("AssertionError")] or lines[-1:] or [""])[-1]
print("FAIL" if result.failures else "ERROR" if result.errors else "ok", first[:240],
      "|", lines[-1][-120:] if lines else "")
"""


def one(mutant: tuple) -> str:
    name, old, new, test = mutant
    if text.count(old) != 1:
        return f"INVALID: {name}: anchor occurs {text.count(old)} times"
    with tempfile.TemporaryDirectory(prefix="r7-quick-") as directory:
        (Path(directory) / "torture_campaign.py").write_text(text.replace(old, new), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, directory, test],
                             capture_output=True, text=True, timeout=900)
    verdict = (run.stdout.strip() or run.stderr.strip()[-200:])
    return f"{'KILLED' if verdict.startswith('FAIL') else 'SURVIVED'}: {name}: {test}: {verdict}"


mutants = [m for m in table.MUTANTS if names is None or m[0] in names]
with ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(one, mutants):
        print(line, flush=True)
