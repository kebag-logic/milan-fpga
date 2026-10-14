import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import ctrl_mutants as m
import ctrl_reuse
part=int(sys.argv[1])
work=Path(os.environ['WORK'])/f"control-slice-{part}"
ctrl_reuse.cut_reuse(work/"reuse")
raise SystemExit(m.campaign(work,work/"reuse",4,(part,4)))
