"""Run named firmware arms on a checkout's ctrl tree: arms.py CHECKOUT OUT ARM[,ARM...] [core-filter]."""
import sys
from pathlib import Path
co, out, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3].split(',')
flt = sys.argv[4] if len(sys.argv) > 4 else '*'
sys.path[:0] = [str(co / 'sw/firmware/ctrl/test'), str(co / 'sw/firmware/gtest')]
import fw_gtest, ctrl_arms, aecp_arms
from ctrl_build import CTRL, Tree
tree = Tree(CTRL, out / 'build', out / 'reuse', fw_gtest.Build(jobs=8))
shipping = co / 'configs/endstation_ax7101_1x1_tdm8.yaml'
outs = []
for n in names:
    if n.startswith('core'):
        outs.append(aecp_arms.core_arm(tree, shipping, int(n[-1]), mode='core', selected=flt))
    elif n.startswith('mailbox'):
        outs.append(aecp_arms.core_arm(tree, shipping, int(n[-1]), mode='mailbox', selected=flt))
    else:
        outs.append(getattr(ctrl_arms, 'arm_' + n)(tree))
sys.exit(1 if ctrl_arms.report(outs) else 0)
