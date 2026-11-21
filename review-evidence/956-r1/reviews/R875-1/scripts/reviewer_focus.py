"""Reviewer driver (#956/#957): focused suites and named planted defects, run from a checkout's
sw/firmware/ctrl/test with that checkout's own campaign code. Usage:
  python3 -B reviewer_focus.py <checkout> suites <out>
  python3 -B reviewer_focus.py <checkout> srp <out> <interfaces> <name>[,<name>...]
  python3 -B reviewer_focus.py <checkout> aecp <out> <name>[,<name>...]
"""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
mode, out = sys.argv[2], Path(sys.argv[3]).resolve()
if mode == "suites":
    import srp_arms, aecp_arms, ctrl_arms  # noqa: E402
    from ctrl_reuse import cut_reuse  # noqa: E402
    tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    cut_reuse(tree.reuse)
    lw = (root / "third_party/lwSRP").resolve()
    which = sys.argv[4] if len(sys.argv) > 4 else "srp"
    if which == "srp":
        outs = srp_arms.talker_arms(tree, lw)
    else:
        shipping = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
        eight = root / "configs/endstation_ax7101_8x8.yaml"
        outs = [aecp_arms.core_arm(tree, shipping, i, mode="app") for i in (1, 2)]
        outs.append(aecp_arms.core_arm(Tree(tree.src, tree.out / "outputs", tree.reuse, tree.build, tree.stack), eight,
                                       1, mode="app", selected=aecp_arms.OUTPUTS))
    bad = 0
    for o in outs:
        tail = [ln for ln in o.log.splitlines() if "PASSED" in ln or "FAILED" in ln or "tests ran" in ln]
        print(f"ARM {o.arm}: rc {o.rc} | {' | '.join(tail[-3:])}", flush=True)
        bad |= o.rc != 0
    sys.exit(1 if bad else 0)
names = set(sys.argv[-1].split(","))
if mode == "srp":
    import srp_mutants  # noqa: E402
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
    assert {d.name for d in srp_mutants.DEFECTS} == names, ("missing", names - {d.name for d in srp_mutants.DEFECTS})
    failed = srp_mutants.campaign(out, (root / "third_party/lwSRP").resolve(), 2, int(sys.argv[4]))
else:
    import aecp_mutants  # noqa: E402
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
    assert {d.name for d in aecp_mutants.DEFECTS} == names, ("missing", names - {d.name for d in aecp_mutants.DEFECTS})
    aecp_mutants.controls = lambda: None  # the full-table drift control; this run plants a named subset
    failed = aecp_mutants.campaign(out, 2)
print("CAMPAIGN", "FAIL" if failed else "ALL CAUGHT", sorted(names), flush=True)
sys.exit(1 if failed else 0)
