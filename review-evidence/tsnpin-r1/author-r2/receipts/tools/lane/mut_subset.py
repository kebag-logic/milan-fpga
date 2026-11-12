"""mut_subset.py <root> <out> <name,...|@changed>: plant only the named control mutants (scratch; the full campaign runs in the gates)."""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import test_ctrl_firmware as t, ctrl_mutants, fw_gtest
names = sys.argv[3].split(",")
table = tuple(m for m in ctrl_mutants.MUTANTS if m.name in names)
missing = set(names) - {m.name for m in table}
assert not missing, missing
print("unnamed tests (whole table):", ctrl_mutants.unnamed_tests(), flush=True)
ctrl_mutants.MUTANTS = table
ctrl_mutants.unnamed_tests = lambda: []
tree = t.Tree(t.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
t.cut_reuse(tree.reuse)
import os
if os.environ.get("ALL_FAILS"):
    orig = ctrl_mutants.caught
    def caught(test, needle, outcome):
        for ln in outcome.log.splitlines():
            if "[FAIL]" in ln:
                print("   FAILLINE", ln.strip()[:240])
        return orig(test, needle, outcome)
    ctrl_mutants.caught = caught
sys.exit(1 if ctrl_mutants.campaign(out / "mutants", tree.reuse, 4) else 0)
