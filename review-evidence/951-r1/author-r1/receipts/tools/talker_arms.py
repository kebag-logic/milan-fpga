#!/usr/bin/env python3
"""talker_arms.py TREE OUT JOBS: the firmware gate's Talker arms (srp_arms.talker_arms: srp_talker.cpp at 1x1/1if and
8x8/2if, the composition's SrpGate at 8x8/2if) on TREE's sources, as test_ctrl_firmware.py runs them; each arm's
verdict and log tail. Exit 0 when every arm passes."""
import sys
from pathlib import Path

tree_root, out, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(tree_root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(tree_root / 'sw/firmware/gtest'))
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

assert CTRL == tree_root / 'sw/firmware/ctrl', CTRL
out.mkdir(parents=True, exist_ok=True)
tree = Tree(CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=jobs))
outcomes = srp_arms.talker_arms(tree, tree_root / 'third_party/lwSRP')
bad = 0
for o in outcomes:
    (out / f'{o.arm}.log').write_text(o.log)
    print(f'== {o.arm}: rc {o.rc}')
    lines = o.log.splitlines()
    keep = [l for l in lines if l.startswith(('[  PASSED', '[  FAILED', '[==========]', '== ', '[       OK', '[ RUN'))
            or 'Failure' in l or 'failures' in l or l.startswith(('Expected', 'Value of', '  Actual', 'Which is', '  Which'))
            or (lines.index(l) > 0 and 'Failure' in lines[lines.index(l) - 1])]
    print('\n'.join(keep[-80:]))
    bad += o.rc != 0
print(f'talker arms: {len(outcomes) - bad} of {len(outcomes)} pass')
sys.exit(1 if bad else 0)
