#!/usr/bin/env python3
"""Run a named subset of the AECP planted controls (sw/firmware/ctrl/test/aecp_mutants.py) on a copy of the tree,
and an unmutated baseline of the same named tests, which must pass.

usage: aecp_subset.py CLONE OUTDIR SHARD_INDEX SHARD_COUNT [--baseline]
The subset: every face-as-path-* plant (aecp_face_mutants.ROWS) and every SET_CONFIGURATION plant
(aecp_configuration_mutants.ROWS), the two tables the sync merge of the three conflicts composed.
"""
import sys
from pathlib import Path

clone, out, k, n = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import aecp_mutants as m  # noqa: E402
import aecp_face_mutants as fm  # noqa: E402
import aecp_configuration_mutants as cm  # noqa: E402
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Tree, ROOT, CTRL, STACK  # noqa: E402

names = {r[0] for r in fm.ROWS} | {r[0] for r in cm.ROWS}
subset = tuple(d for d in m.DEFECTS if d.name in names)
assert len(subset) == len(names), (len(subset), len(names))

if "--baseline" in sys.argv:
    import shutil
    root = out
    root.mkdir(parents=True, exist_ok=True)
    src = root / "work/ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
    tree = Tree(src, root / "work/build", root / "work/reuse", fw_gtest.Build(jobs=4), STACK)
    config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    tests = sorted({t for d in subset for t, _ in d.checks})
    bad = 0
    for mode in ("app",):
        for interfaces in (2,):
            r = aecp_arms.core_arm(tree, config, interfaces, mode, ":".join(tests))
            (root / f"baseline-{mode}-if{interfaces}.log").write_text(r.log)
            print(f"baseline {mode} if{interfaces}: rc {r.rc}, {len(tests)} named tests", flush=True)
            bad |= r.rc != 0
    sys.exit(int(bad))

m.controls()  # the whole table's drift check, on the unfiltered table, before the subset replaces it
m.DEFECTS = subset
m.controls = lambda: None  # the drift check requires the whole table; it ran above
print(f"table controls PASS; subset {len(subset)} plants, shard {k}/{n}", flush=True)
sys.exit(int(m.campaign(out, jobs=4, shard=(k, n), stack=STACK)))
