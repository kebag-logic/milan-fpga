"""Apply each round-7 audio control to a scratch copy of the planner and run its named test.

Usage: python3 -I probe_new_mutants.py <repo> <scratch_dir> <count_from_end>
A control is killed when the pristine named test passes and the mutated one fails.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

REPO, SCRATCH, COUNT = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(REPO / "tb/tools"))
from torture_release_audio_mutants import AUDIO_GRADER_MUTANTS  # noqa: E402

RUNNER = '''
import sys, unittest
sys.path.insert(0, sys.argv[1])
import torture_campaign as tc
class T(tc._ReleaseGateChecks, unittest.TestCase):
    pass
r = unittest.TextTestRunner(verbosity=1).run(unittest.TestLoader().loadTestsFromName(sys.argv[2], T))
sys.exit(0 if r.wasSuccessful() else 1)
'''


def run(label, old, new, test):
    work = SCRATCH / f"mut-{abs(hash(label)) % 10**8}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    text = (REPO / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
    if old is not None:
        if text.count(old) != 1:
            return label, test, "ANCHOR-COUNT", text.count(old), ""
        text = text.replace(old, new)
    (work / "torture_campaign.py").write_text(text, encoding="utf-8")
    (work / "runner.py").write_text(RUNNER, encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", "-B", str(work / "runner.py"), str(work), test],
                       capture_output=True, text=True, timeout=1200)
    tail = [l for l in p.stderr.splitlines() if l.startswith(("AssertionError", "FAIL", "OK", "Ran"))]
    return label, test, "rc", p.returncode, " | ".join(tail)[:400]


mutants = AUDIO_GRADER_MUTANTS[-COUNT:]
jobs = [("PRISTINE " + t, None, None, t) for t in sorted({m[3] for m in mutants})] + list(mutants)
with concurrent.futures.ThreadPoolExecutor(8) as pool:
    for result in pool.map(lambda m: run(*m), jobs):
        print(*result, sep="\t")
