# Reviewer probe (R584-14): R585-12's F1 shape (the pinned src/ tree's object forged to hold an edit) at three real
# entry points of the head, each run as a separate process on the forged clone.
# Usage: python3 -I forged_entrypoints.py <clone-root> <work-dir>
# The clone is built with the head's own ctrl_pin_store.forged_tree (every object loose in its own store, the
# forged object written as a new file). Each entry point must exit 2 naming the forged tree, before any build.
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_pin_env import Scene, answer  # noqa: E402
import ctrl_pin_store  # noqa: E402

if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
pin = answer(root, "ls-files", "--stage", "--", "third_party/tsn-c-stack").split()[1]
stack = work / "stack"
answer(work, "clone", "--quiet", "--no-hardlinks", str(root / "third_party/tsn-c-stack"), str(stack))
answer(stack, "-c", "advice.detachedHead=false", "checkout", "--quiet", pin)
scene = Scene(stack, pin, work / "own")
(work / "own").mkdir()
ctrl_pin_store.forged_tree(scene)
print(f"forged clone: {answer(stack, 'status', '--porcelain').strip()} (edited, src/ tree object forged)")
T = root / "sw/firmware/ctrl/test"
env = dict(os.environ, VERILATOR="false")
points = [
    ("ctrl_build.py --stack-pin", [sys.executable, "-B", str(T / "ctrl_build.py"), "--stack-pin", str(stack)]),
    ("maap_differential.py --stack", [sys.executable, "-B", str(T / "maap_differential.py"), "--stack", str(stack)]),
    ("aecp_arms.py --stack", [sys.executable, "-B", str(T / "aecp_arms.py"), "--stack", str(stack),
                              "--output", str(work / "aecp-out")]),
]
for what, argv in points:
    res = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=work)
    said = [ln for ln in (res.stdout + res.stderr).splitlines() if "tsn-c-stack" in ln or "REFUSED" in ln]
    built = sorted(p.name for p in work.rglob("*.o"))
    print(f"{what}: exit {res.returncode}; {said[-1].strip() if said else 'no pin verdict'}; objects built: {len(built)}")
