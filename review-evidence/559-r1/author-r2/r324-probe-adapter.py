import runpy, sys
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).parent
sys.path.insert(0,str(p/'harness'))
import soc, run
original=soc.eb._derive_artifacts
def derive(*a,**kw):
 art=original(*a,**kw)
 art.cfg['constraints']['milan_clk_hz']=50000000
 return art
soc.eb._derive_artifacts=derive
actual_run=run.subprocess.run
def compile_phase(argv,**kw):
 argv=[str(p/'phase.cpp') if a==str(p/'harness/sim_main.cpp') else a for a in argv]
 return actual_run(argv,**kw)
step=sys.argv[1]
if step=='verilate':
 # probe_step temporarily wraps this and calls it with its --build removed.
 run.subprocess.run=compile_phase
runpy.run_path(str(p/'probe_step.py'),run_name='__main__')
