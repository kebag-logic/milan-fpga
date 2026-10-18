#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, sys, time
packet=pathlib.Path(__file__).resolve().parent
source=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else packet/'scratch/source'
v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
def run(job):
 name,cmd,cwd=job
 with (packet/(name+'.log')).open('w') as log:
  log.write('COMMAND '+repr(cmd)+'\n');log.flush()
  r=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
 (packet/(name+'.rc')).write_text(str(r.returncode)+'\n')
 return name,r.returncode
jobs=[]
for suite in ['srp_encoder','srp_top']:
 flags='--cc --exe --build -j 4 '+('--savable ' if suite=='srp_top' else '')+'--top-module '+('srp_tb_wrap' if suite=='srp_encoder' else 'srp_top_wrap')+' -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I'+str(source/'tb'/suite)+' -Wall -Wextra"'
 jobs.append((suite,['make','-j16','run','VERILATOR='+v,'VFLAGS='+flags],source/'tb'/suite))
jobs.append(('matrix',['python3','scripts/gen_matrix.py','--check'],source))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for name,rc in pool.map(run,jobs):print(name,'rc='+str(rc),flush=True)
