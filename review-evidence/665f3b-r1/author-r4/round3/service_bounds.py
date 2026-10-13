"""Run the repository's compiled service-bound check and its planted controls."""
import argparse
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
root = args.repo.resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build
import ctrl_service_bounds

result = ctrl_service_bounds.arm_service_bounds(
    ctrl_build.Tree(ctrl_build.CTRL, args.out.resolve(), root))
print(result.log)
raise SystemExit(result.rc)
