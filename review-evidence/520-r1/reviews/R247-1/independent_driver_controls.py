#!/usr/bin/env python3
"""Independent seed-only bad-generation/record probes through unchanged driver."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT, OUT = [Path(v).resolve() for v in sys.argv[1:]]
OUT.mkdir(parents=True)
SHIM=r'''
import json, os, shutil, subprocess, sys
from pathlib import Path
a=sys.argv[1:];real=os.environ['R247_PYTHON'];folder=Path(os.environ['R247_LOGDIR'])
name=Path(a[0]).name if a else ''
def log(event):
    with (folder/'events.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
if name in ('gen_ltn_rom.py','gen_ucode.py','gen_gptp_ucode.py'):
    image=Path(a[a.index('-o')+1]);action=os.environ.get('R247_ACTION','') if image.name==os.environ.get('R247_IMAGE') else ''
    log({'generator':name,'action':action})
    if action=='failed':sys.exit(19)
    r=subprocess.run([real,*a]);
    if r.returncode:sys.exit(r.returncode)
    if action=='empty':image.write_bytes(b'')
    if action=='missing':image.unlink()
    if action=='wrong-name':image.rename(image.with_name(image.name+'.wrong'))
    sys.exit(0)
if name=='result_cache.py':
    log({'operation':a[1],'arguments':a[2:]})
    if a[1]=='rom-digest' and os.environ.get('R247_ACTION')=='digest-failed':sys.exit(17)
if a and a[0]=='-' and len(a)==2 and a[1].endswith('.stat.json'):
    p=Path(a[1]);
    if p.exists():shutil.copyfile(p,folder/p.name)
os.execv(real,[real,*a])
'''
binpath=OUT/'bin';binpath.mkdir();shim=binpath/'python3'
shim.write_text('#!'+sys.executable+'\n'+SHIM);shim.chmod(0o755)
ROWS=[]
def snapshot(p):
    return {str(f.relative_to(p)):[hashlib.sha256(f.read_bytes()).hexdigest(), f.stat().st_mode&0o777]
            for f in p.rglob('*') if f.is_file()}
def readonly(p):
    for f in [p,*p.rglob('*')]:f.chmod(f.stat().st_mode & ~0o222)
def run(label,mode,flags,action='',image=''):
    folder=OUT/label;folder.mkdir()
    env=dict(os.environ,PATH=str(binpath)+':'+os.environ['PATH'],R247_PYTHON=sys.executable,
             R247_LOGDIR=str(folder),R247_ACTION=action,R247_IMAGE=image,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1')
    cmd=['rtk','proxy','bash',str(ROOT/'syn/yosys/run.sh'),'--top','cdc_pulse','--top','cdc_handshake',
         '--no-structural','--mode',mode,'--results',str(folder/'results'),*flags]
    start=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    (folder/'stdout').write_text(p.stdout);(folder/'stderr').write_text(p.stderr)
    events=[json.loads(line) for line in (folder/'events.jsonl').read_text().splitlines()]
    cells=dict(re.findall(r'\[PASS\]\s+(\S+)\s+cells=(\d+)',p.stdout))
    row=dict(label=label,command=cmd,mode=mode,action=action,image=image,exit=p.returncode,
             cells=cells,hits=p.stdout.count('(result cache)'),events=events,seconds=round(time.monotonic()-start,3))
    (folder/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');ROWS.append(row)
    (OUT/'rows.json').write_text(json.dumps(ROWS,indent=2)+'\n')
    return row,p.stdout+p.stderr
for mode in ('full','elaborate'):
    head=OUT/(mode+'-head')
    cold,_=run(mode+'-cold',mode,['--cache',str(head)])
    assert cold['exit']==0 and cold['hits']==0 and set(cold['cells'])=={'cdc_pulse','cdc_handshake'}
    seed=OUT/(mode+'-seed');shutil.copytree(head,seed);readonly(seed);before=snapshot(seed)
    warm,_=run(mode+'-seed-hit',mode,['--cache-seed',str(seed)])
    assert warm['exit']==0 and warm['hits']==2 and warm['cells']==cold['cells']
    for image,title in [('ltn_rom.hex','ACMP transition-ROM'),('ucode.hex','AECP microcode'),('gptp_ucode.hex','gPTP microcode')]:
        for action in ('failed','empty','missing','wrong-name'):
            row,output=run(mode+'-'+image+'-'+action,mode,['--cache-seed',str(seed)],action,image)
            assert row['exit']==2 and not row['cells'] and row['hits']==0, row
            expected=title+' generation failed' if action=='failed' else 'generated ROM is empty:'
            assert expected in output,output
            assert not any(e.get('operation') in ('rom-digest','lookup','store') for e in row['events']),row
    row,output=run(mode+'-digest-failed',mode,['--cache-seed',str(seed)],'digest-failed')
    assert row['exit']==2 and 'generated ROM bundle could not be digested' in output
    assert not any(e.get('operation') in ('lookup','store') for e in row['events'])
    for variant in ('legacy-original','legacy-relocated','missing','malformed','mismatch','duplicate','forged-stat'):
        planted=OUT/(mode+'-'+variant+'-seed');shutil.copytree(head,planted)
        for entry in list(planted.iterdir()):
            f=entry/'record';text=f.read_text();fields=dict(line.split('=',1) for line in text.splitlines());romline='rom_sha256='+fields['rom_sha256']+'\n'
            if variant.startswith('legacy'):
                f.write_text(text.replace('milan-yosys-result-cache/2','milan-yosys-result-cache/1').replace(romline,''))
                if variant=='legacy-original':
                    keys=('top','mode','sv2v_sha256','program','yosys_version','yosys_sha256','sv2v_version')
                    old='milan-yosys-result-cache/1\n'+''.join(k+'='+fields[k]+'\n' for k in keys)
                    entry.rename(planted/hashlib.sha256(old.encode()).hexdigest())
            elif variant=='forged-stat':
                (entry/'stat.json').write_text(json.dumps({'design':{'num_cells':int(fields['cells'])+1}}))
            else:
                replacement={'missing':'','malformed':'rom_sha256=bogus\n','mismatch':'rom_sha256='+'f'*64+'\n','duplicate':romline*2}[variant]
                f.write_text(text.replace(romline,replacement))
        readonly(planted);unchanged=snapshot(planted)
        label=mode+'-'+variant+'-live'
        row,output=run(label,mode,['--cache-seed',str(planted)])
        assert row['exit']==0 and row['hits']==0 and row['cells']==cold['cells'],row
        assert not any(e.get('operation')=='store' for e in row['events']),row
        if variant!='legacy-original':assert output.count('cache entry refused, running live')==2,output
        for top,count in row['cells'].items():
            assert json.loads((OUT/label/(top+'.stat.json')).read_text())['design']['num_cells']==int(count)
        assert snapshot(planted)==unchanged
    assert snapshot(seed)==before
(OUT/'complete.json').write_text(json.dumps({'result':'PASS','driver_invocations':len(ROWS),'modes':['full','elaborate'],'tops':['cdc_pulse','cdc_handshake']},indent=2)+'\n')
print(f'PASS: {len(ROWS)} independent real-driver seed/generation/record controls')
