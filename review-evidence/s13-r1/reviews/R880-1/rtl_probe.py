#!/usr/bin/env python3
"""Build and run the split leg and its new VERSION mutation in a disposable clone."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
repo, packet, executable = map(Path, sys.argv[1:4])
env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet/'scratch'),
         PATH=str(executable.parent)+':'+os.environ['PATH'])
identity=subprocess.check_output([str(executable),'--version'],text=True)
assert 'Verilator 5.050 ' in identity, identity
print(identity.strip(), 'sha256',hashlib.sha256(executable.read_bytes()).hexdigest(),flush=True)
cwd=repo/'tb/verilator/milan_dp'
source=repo/'hdl/milan/milan_datapath.sv'
old='    .CTRL_SPLIT_P(CTRL_SPLIT_P)'
text=source.read_text()
assert text.count(old)==1
mutant=packet/'scratch/version-mutant.sv'
mutant.write_text(text.replace(old,'    .CTRL_SPLIT_P(0)'))
for name, path in [('clean',source),('mutant',mutant)]:
 out=packet/'scratch'/('rtl-'+name)
 argv=['make','-j16','--no-print-directory','build-split',f'VERILATOR={executable}',
       'VERILATOR_JOBS=12',f'SPLIT_MDIR={out}',f'DP_SRC={path}']
 with (packet/f'rtl-{name}-build.log').open('w') as log:
  log.write('COMMAND '+json.dumps(argv)+'\n'); log.flush()
  built=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
 (packet/f'rtl-{name}-build.rc').write_text(str(built.returncode)+'\n')
 assert built.returncode==0, name+' build failed'
 result=subprocess.run([str(out/'Vmilan_dp_split')],cwd=cwd,env=env,text=True,capture_output=True)
 (packet/f'rtl-{name}.log').write_text(result.stdout+result.stderr)
 (packet/f'rtl-{name}.rc').write_text(str(result.returncode)+'\n')
 if name=='clean': assert result.returncode==0
 else:
  assert result.returncode>0 and 'FAIL [ID] the split datapath reads VERSION major 0x0003 (VERSION >> 16)' in result.stdout
 print(name,'rc',result.returncode,flush=True)
print('PASS: clean split datapath and targeted VERSION defect detection',flush=True)
