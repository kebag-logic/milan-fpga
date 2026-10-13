import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"sw/firmware/ctrl/test"))
import ctrl_configs,ctrl_capture
root=Path.cwd(); work=Path(os.environ['WORK']); cap=work/"capture-small"
for i in (0,2,4,5):
 b=ctrl_configs.BUILDERS[i]
 for words in b.runs:
  args=[w.format(python=sys.executable,work=work/"small-builders",verilator="") for w in words]
  rc=ctrl_capture.run(cap,args,cwd=root).returncode
  print(b.path,rc,flush=True)
  if rc: raise SystemExit(rc)
