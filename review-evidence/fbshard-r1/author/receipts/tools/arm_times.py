"""Time each build-only suite thunk of test_ctrl_firmware.suite_arms whose index is K mod N (measurement only)."""
import sys, time, tempfile
from types import SimpleNamespace
from pathlib import Path
HERE = Path("$LANES/ci-fbshard/sw/firmware/ctrl/test")
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "gtest"))
import test_ctrl_firmware as t, fw_gtest
from ctrl_build import CTRL, Tree, stack_pin
from ctrl_reuse import cut_reuse
fw_gtest.EXECUTION.run = False
k, n = map(int, sys.argv[1].split("/"))
args = SimpleNamespace(require_rv32=True, lwsrp=CTRL.parents[2] / "third_party/lwSRP")
T0 = time.monotonic()
with tempfile.TemporaryDirectory(prefix="a827-arms-") as tmp:
    out = Path(tmp)
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    stack_pin(); cut_reuse(tree.reuse)
    for i, f in enumerate(t.suite_arms(args, tree)):
        if i % n != k: continue
        t0 = time.monotonic(); f(); print(f"{i:2d} {time.monotonic()-t0:7.1f}", flush=True)
print(f"part {k}/{n} total {time.monotonic()-T0:.1f}")
