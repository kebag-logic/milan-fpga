"""Run the port arm, the lwSRP arm and srp_arms.arm_srp at 1 and 2 interfaces over srp_mbx.cpp and srp_rx_retry.cpp,
from a tree (a probe copy). Usage: python3 -I run_srp_arms.py <tree root> <out dir>"""
import sys
from pathlib import Path
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import ctrl_arms, srp_arms, fw_gtest
from ctrl_build import CTRL, Tree
tree = Tree(CTRL, out / 'checkout', out / 'reuse', fw_gtest.Build(jobs=4))
lw = root / 'third_party/lwSRP'
outs = [ctrl_arms.arm_port(tree), ctrl_arms.arm_lwsrp(tree, lw)]
for i in (1, 2):
    outs.append(srp_arms.arm_srp(tree, lw, i))
    outs.append(srp_arms.arm_srp(tree, lw, i, test='srp_rx_retry.cpp'))
rc = 0
for o in outs:
    fails = [l for l in o.log.splitlines() if '[  FAILED  ]' in l]
    print(f'arm {o.arm}: rc {o.rc}; FAILED lines {len(fails)}')
    for l in fails[:6]:
        print('   ', l[:200])
    rc |= o.rc != 0
sys.exit(rc)
