#!/usr/bin/env python3
"""The failing words each chosen release-control mutant draws from its named arm.

Usage: python3 -I mutant_failing_words.py <tb/tools dir> <work dir> <mutant number>... [--jobs N]

Mutant numbers are 1-based positions in torture_release_mutants.MUTANTS.
Each is applied to a private planner copy; its named arm runs alone, and
the last line of its first failure that is not a
diff marker is printed beside the defect's name.
"""
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

args = sys.argv[1:]
jobs = 8
if "--jobs" in args:
    jobs = int(args[args.index("--jobs") + 1])
    del args[args.index("--jobs"):args.index("--jobs") + 2]
tools, work, numbers = pathlib.Path(args[0]), pathlib.Path(args[1]), [int(a) for a in args[2:]]
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
problems = result.failures + result.errors
lines = [l for l in problems[0][1].splitlines() if l.strip() and not l.lstrip().startswith("?")] if problems else []
print(lines[-1].strip()[:200] if lines else "PASSED")
"""


def words(number: int) -> str:
    """Run mutant `number` against its named arm and return its first failing words."""
    name, old, new, test = m.MUTANTS[number - 1]
    here = work / f"w{number:03d}"
    here.mkdir(parents=True, exist_ok=True)
    (here / "torture_campaign.py").write_text(text.replace(old, new), encoding="utf-8")
    done = subprocess.run([sys.executable, "-B", "-I", "-c", DRIVER, str(here), test],
                          capture_output=True, text=True, timeout=600, check=False)
    return f"{number} | {name} | {test} | {done.stdout.strip() or done.stderr.strip()[-200:]}"


with ThreadPoolExecutor(jobs) as pool:
    for row in pool.map(words, numbers):
        print(row, flush=True)
