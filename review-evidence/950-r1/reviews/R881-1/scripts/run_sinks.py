"""run_sinks.py <tree-root> <out> <8x8|1x1> [gtest filter]: build one tree's platsinks arm
(plat_arms.arm_platsinks) at one shape, then run its binary with the filter; prints the failures and rc."""
import subprocess, sys
from pathlib import Path
root, out, shape = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
flt = sys.argv[4] if len(sys.argv) > 4 else "*"
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
from ctrl_build import CTRL, STACK, Tree  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
assert str(CTRL).startswith(str(root)), CTRL
cfg, n = {"8x8": (root / "configs/endstation_ax7101_8x8.yaml", 7),
          "1x1": (root / "configs/endstation_ax7101_1x1_tdm8.yaml", 0)}[shape]
tree = Tree(CTRL, out, out / "reuse", fw_gtest.Build(coverage=False, address_sanitizer=False, jobs=4), STACK)
try:
    outcome = plat_arms.arm_platsinks(tree, cfg, n)
except Exception as exc:
    print(f"REFUSED: {exc}"); raise SystemExit(2)
exe = next(out.rglob(f"test_plat_sinks_{cfg.stem}"))
r = subprocess.run([str(exe), f"--gtest_filter={flt}"], capture_output=True, text=True)
lines = r.stdout.splitlines()
for l in lines:
    if l.startswith(("[  PASSED", "[  FAILED", "[       OK", "[ RUN", "[FAIL]")) or "Failure" in l or "tally" in l.lower():
        print(l)
print(f"filtered rc={r.returncode} (whole arm rc={outcome.rc})")
raise SystemExit(r.returncode)
