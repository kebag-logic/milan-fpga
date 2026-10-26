#!/usr/bin/env python3
"""Run chosen release-control mutants against their named self-test arm only, in parallel.

Usage: python3 -I quick_named_mutants.py <tb/tools dir> <work dir> <first mutant number> [jobs]

A fast pre-check of tb/tools/torture_release_mutants.py: each mutant from
the given 1-based number on is applied to a private planner copy, and only
its named arm runs. KILLED needs that arm to fail; the full driver, which
runs the whole self-test per mutant, remains the gate. Exit status 0.
"""
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

tools, work, first = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), int(sys.argv[3])
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
sys.path.insert(0, str(tools))
import torture_release_mutants as m  # noqa: E402

text = (tools / "torture_campaign.py").read_text(encoding="utf-8")
DRIVER = """
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as t
for name in dir(t):
    mixin = getattr(t, name)
    if isinstance(mixin, type) and hasattr(mixin, sys.argv[2]):
        break
class T(mixin, unittest.TestCase):
    pass
result = unittest.TestResult()
T(sys.argv[2]).run(result)
print("FAILED" if result.failures else "ERRORED" if result.errors else "PASSED")
"""


def run(number: int) -> str:
    """Apply mutant `number` in its own directory and run its named arm."""
    name, old, new, test = m.MUTANTS[number - 1]
    if text.count(old) != 1:
        return f"{number} INVALID {name}"
    here = work / f"m{number:03d}"
    here.mkdir(parents=True, exist_ok=True)
    (here / "torture_campaign.py").write_text(text.replace(old, new), encoding="utf-8")
    done = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, str(here), test],
                          capture_output=True, text=True, timeout=600, check=False)
    state = done.stdout.strip() or "CRASHED"
    return f"{number} {'KILLED' if state == 'FAILED' else 'SURVIVED'} {name}: {test} ({state})"


with ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(run, range(first, len(m.MUTANTS) + 1)):
        print(line, flush=True)
