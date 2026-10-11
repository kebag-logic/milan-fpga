#!/usr/bin/env python3
"""Re-run public round-two probes with copied-input updates recorded separately."""
import concurrent.futures,json,os,subprocess
from pathlib import Path
p=Path(__file__).resolve().parents[1];src=Path(os.environ.get('REVIEW_SOURCE',str(p/'scratch/head')))
r=p/'receipts';env=os.environ.copy();env.update(TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',MAKEFLAGS='-j16')
py=['python3','-B'];s=p/'scripts';pub=p/'public/reviews'
cases=[('table-probes',py+[str(s/'prior_table_probes.py'),'--src',str(src),'--out',str(r/'table-probes')]),
 ('generator-probes',py+[str(s/'prior_generator_probes.py'),'--src',str(src),'--out',str(r/'generator-lines.txt')]),
 ('export-fields',py+[str(pub/'R609-2/scripts/probe_export_fields.py'),'--root',str(src)]),
 ('prior-rom-size',py+[str(pub/'R609-1/scripts/rom_size_probe.py'),str(src)]),
 ('prior-size-sweep',py+[str(pub/'R609-1/scripts/size_sweep.py'),str(src),str(p/'scratch/size-sweep')])]
def run(case):
 name,cmd=case
 with (r/(name+'.log')).open('w') as f:rc=subprocess.run(cmd,cwd=src,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 (r/(name+'.rc')).write_text(str(rc)+'\n');print(name,rc,flush=True);return dict(name=name,rc=rc)
with concurrent.futures.ThreadPoolExecutor(3) as pool:res=list(pool.map(run,cases))
res.append(run(('echo-size-sweep',py+[str(s/'prior_size_sweep_r608.py'),'--jobs','4','--src',str(src),'--out',str(r/'echo-size-lines.txt')])))
(r/'probe-execution.json').write_text(json.dumps(res,indent=2)+'\n')
raise SystemExit(int(any(x['rc'] for x in res)))
