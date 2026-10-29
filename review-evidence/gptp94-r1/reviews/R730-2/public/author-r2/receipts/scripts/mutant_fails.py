"""Print every FAIL line one named arm mutant produces, and its tally.

usage: mutant_fails.py <engine tb dir> <mutant name>
"""
import sys
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402

name = sys.argv[2]
mutation = next(m for m in mutants.MUTATIONS if m[0] == name)
work = Path(sys.argv[0]).resolve().parent.parent / "tmp" / ("fails-" + "".join(
    c if c.isalnum() else "_" for c in name))
work.mkdir(parents=True, exist_ok=True)
_, fname, pattern, replacement, _ = mutation
src = mutants.stage(work, "m", (fname, mutants.edits_of(pattern, replacement)))
run = work / "run_m"
assert mutants.generate_image(src, run)
exe = mutants.build(src, work, "m")
rc, out = mutants.run_harness(exe, run)
for line in out.splitlines():
    if line.startswith("FAIL") or "checks:" in line:
        print(line)
print("rc", rc)
