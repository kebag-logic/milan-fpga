"""Plant leg INDEX of COUNT of adp_first_mutants.MUTANTS (the #970 draw's defects) through ctrl_mutants.campaign,
on the checkout given. Per-mutant [ok]/[ESCAPED] lines are the verdict; the campaign's whole-table
"no defect names the test" lines do not apply to a sub-table and are ignored.
Usage: python3 -B adp_mutants_leg.py <checkout> <work-dir> INDEX COUNT."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import test_ctrl_firmware as t  # noqa: E402
import ctrl_mutants, adp_first_mutants, fw_gtest  # noqa: E402,E401
out = Path(sys.argv[2]).resolve()
i, n = int(sys.argv[3]), int(sys.argv[4])
tree = t.Tree(t.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
t.cut_reuse(tree.reuse)
ctrl_mutants.unnamed_tests = lambda: []
ctrl_mutants.MUTANTS = tuple(adp_first_mutants.MUTANTS)
print(f"adp_first_mutants leg {i}/{n}: {len(ctrl_mutants.MUTANTS[i::n])} of {len(ctrl_mutants.MUTANTS)}")
sys.exit(1 if ctrl_mutants.campaign(out / "mutants", tree.reuse, 4, shard=[i, n]) else 0)
