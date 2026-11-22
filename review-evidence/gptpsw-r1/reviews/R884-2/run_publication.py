#!/usr/bin/env python3
"""Exercise the actual publication crossing with sequential committed writes."""
from pathlib import Path
import os
import subprocess
import sys
p=Path(__file__).resolve().parent
(p/"scratch").mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode=True
r=Path(sys.argv[1]).resolve()
v=os.environ.get('VERILATOR','verilator')
cmd=[v,'--binary','--timing','--build','-j','4','--top-module','probe_publication','--Mdir',str(p/'scratch/publication'),'-Wno-fatal','-Wno-PINMISSING','-Wno-TIMESCALEMOD',str(r/'hdl/milan/mailbox/KL_mbx_pkg.sv'),str(r/'hdl/common/cdc_handshake.sv'),str(r/'hdl/common/cdc_pulse.sv'),str(r/'hdl/milan/mailbox/KL_mbx_cdc_window.sv'),str(r/'hdl/milan/mailbox/KL_mbx_cdc.sv'),str(p/'probe_publication.sv')]
with (p/'publication-build.log').open('w') as log:
 log.write('COMMAND: '+repr(cmd)+'\n');log.flush()
 subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
import resource
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
results=[]
for name, args in [('publication-control',['+CONTROL']),('publication',[])]:
 with (p/(name+'.log')).open('w') as log:
  result=subprocess.run([str(p/'scratch/publication/Vprobe_publication')]+args,stdout=log,stderr=subprocess.STDOUT,cwd=p/'scratch')
 (p/(name+'.rc')).write_text(str(result.returncode)+'\n')
 print(name+':\n'+(p/(name+'.log')).read_text())
 results.append(result.returncode)
sys.exit(any(results))
