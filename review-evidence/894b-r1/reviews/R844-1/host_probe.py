"""Build a selected AECP mailbox arm; all products stay in the supplied scratch directory."""
import sys
from pathlib import Path
root, out = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms, ctrl_build, fw_gtest
selected = sys.argv[3]
t = ctrl_build.Tree(root / 'sw/firmware/ctrl', out, out / 'reuse', fw_gtest.Build(jobs=4))
r = aecp_arms.core_arm(t, root / 'configs/endstation_ax7101_8x8.yaml', 1, mode='mailbox', selected=selected)
print(r.log)
print('EXIT', r.rc)
raise SystemExit(r.rc)
