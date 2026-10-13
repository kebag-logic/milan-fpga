import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'sw/firmware/ctrl/test'))
import ctrl_build as b
import ctrl_service_bounds as s
r=s.arm_service_bounds(b.Tree(b.CTRL,Path(os.environ['WORK']) / 'bounds',Path('.')))
print(r.log)
raise SystemExit(r.rc)
