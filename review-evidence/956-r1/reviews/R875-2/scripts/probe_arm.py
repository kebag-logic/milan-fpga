"""Reviewer probe driver (#956/#957): copy a checkout's sw/firmware/ctrl into a disposable work directory, append probe
sources to one test file, and run one SRP or AECP arm of that copy with a gtest filter.
Usage:
  python3 -B probe_arm.py <checkout> <work> srp <interfaces> <config.yaml> <test.cpp> <filter> [probe.cpp ...]
  python3 -B probe_arm.py <checkout> <work> aecp <interfaces> <config.yaml> test_aecp.cpp <filter> [probe.cpp ...]
Prints the arm's log; exit status is the arm's."""
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
kind, interfaces, config, test, selected = sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
probes = [Path(p).resolve() for p in sys.argv[8:]]
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest  # noqa: E402
import ctrl_build  # noqa: E402

src = work / "ctrl"
for name in ("ctrl", "ctrl_nvm"):
    if (work / name).exists():
        shutil.rmtree(work / name)
    shutil.copytree(root / "sw/firmware" / name, work / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
target = src / "test" / test
text = target.read_text()
for p in probes:
    text += "\n" + p.read_text()
target.write_text(text)
tree = ctrl_build.Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=4))
if kind == "srp":
    import srp_arms  # noqa: E402
    srp_arms.HERE = src / "test"
    o = srp_arms.arm_srp(tree, (root / "third_party/lwSRP").resolve(), interfaces, test=(test, selected),
                         config=root / config)
else:
    import aecp_arms  # noqa: E402
    aecp_arms.HERE = src / "test"
    o =aecp_arms.core_arm(tree, root / config, interfaces, mode="app", selected=selected)
print(o.log)
sys.exit(o.rc)
