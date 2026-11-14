"""Run one AECP arm on a tree: the mailbox arm at a configuration and interface count with a gtest filter; print the
outcome and the run's summary lines. usage: python3 -B arm8.py TREE OUT CONFIG IFS MODE FILTER"""
import sys
from pathlib import Path
tree_root, out, config, ifs, mode, filt = sys.argv[1:7]
sys.path.insert(0, str(Path(tree_root) / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(Path(tree_root) / 'sw/firmware/gtest'))
import aecp_arms, ctrl_build, fw_gtest
t = ctrl_build.Tree(Path(tree_root) / 'sw/firmware/ctrl', Path(out), Path(out) / 'reuse', fw_gtest.Build(jobs=8))
r = aecp_arms.core_arm(t, Path(tree_root) / 'configs' / config, int(ifs), mode=mode, selected=filt)
print(r.arm, 'rc', r.rc)
print('\n'.join(l for l in r.log.splitlines() if l.startswith(('[  PASSED', '[  FAILED', '[==========', '[       OK', '[  FAILED  ]'))))
sys.exit(r.rc)
