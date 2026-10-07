import sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_arms, ctrl_build, ctrl_reuse, fw_gtest
tree=ctrl_build.Tree(ctrl_build.CTRL,out/'build',out/'reuse',fw_gtest.Build(jobs=4))
ctrl_reuse.cut_reuse(tree.reuse)
failed=False
for name in ['model','acmp','acmpif2','acmpwalk','acmpnvm']:
    result=getattr(ctrl_arms,'arm_'+name)(tree)
    print(result.log,flush=True); print(name,'rc',result.rc,flush=True)
    failed=failed or result.rc!=0
sys.exit(int(failed))
