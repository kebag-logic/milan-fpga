#!/usr/bin/env python3
"""Per-file analysis of the consumer-derived list at the exact merge head."""
import argparse, hashlib, importlib.util, json, re, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('packet',type=Path);p.add_argument('--xvlog',required=True,type=Path);a=p.parse_args()
sys.dont_write_bytecode=True
source=a.packet/'public/pp_srcs.py'
s=importlib.util.spec_from_file_location('consumer_sources',source);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.PP_HDL=a.repo/'hdl'; files=m.pp_sources('hdl')
out=a.packet/'receipts/analysis';out.mkdir(exist_ok=True)
work=a.packet/'scratch/analysis';work.mkdir(exist_ok=True)
(out/'sources.txt').write_text('\n'.join(files)+'\n')
rows=[]
for i,f in enumerate(files):
    start=time.monotonic()
    r=subprocess.run([str(a.xvlog),'-sv','--work','work',str(a.repo/f)],cwd=work,capture_output=True,text=True)
    text=r.stdout+r.stderr
    (out/f'{i:02d}-{Path(f).stem}.log').write_text(text)
    row=dict(file=f,rc=r.returncode,vrfc_3380=text.count('VRFC 10-3380'),vrfc_8530=text.count('VRFC 10-8530'),
             seconds=round(time.monotonic()-start,3),source_sha256=hashlib.sha256((a.repo/f).read_bytes()).hexdigest())
    rows.append(row); print(json.dumps(row),flush=True)
result=dict(head=subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip(),
            derived_list_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),count=len(rows),files=rows)
(out/'table.json').write_text(json.dumps(result,indent=2)+'\n')
rc=int(any(r['rc'] or r['vrfc_3380'] or r['vrfc_8530'] for r in rows))
(out/'result.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)
