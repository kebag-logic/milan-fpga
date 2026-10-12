"""Run a tree's tsn-c-stack pin controls (ctrl_pin.pin_controls) and its census alone, with the Git PATH names.

usage: python3 -B run_pin_controls.py TREE WORK
"""
import shutil
import subprocess
import sys
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))
from ctrl_configs import makefiles  # noqa: E402
from ctrl_pin import pin_controls, proof_census  # noqa: E402
import ctrl_build  # noqa: E402

print("git:", ctrl_build.GIT, subprocess.run([ctrl_build.GIT, "--version"], capture_output=True, text=True).stdout.strip(),
      flush=True)
if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
census = proof_census()
bad, count = pin_controls(work, makefiles())
print(f"SUMMARY pin controls {count}, misbehaved {bad}, census findings {len(census)}", flush=True)
for f in census:
    print("  CENSUS", f)
sys.exit(1 if bad or census else 0)
