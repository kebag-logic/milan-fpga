import sys
from pathlib import Path
root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_arms, fw_gtest
from ctrl_build import CTRL, Tree
from ctrl_reuse import cut_reuse
tree = Tree(CTRL, work / 'checkout', work / 'reuse', fw_gtest.Build(jobs=4)); cut_reuse(tree.reuse)
o = ctrl_arms.arm_unit(tree)
print('\n'.join(l for l in o.log.splitlines() if 'PROBE' in l or 'ReviewProbe' in l)); sys.exit(o.rc)
