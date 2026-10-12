#!/usr/bin/env python3
"""Disposable synthetic controls of the published reduction scripts.

Usage: probe_reductions.py AUTHOR_EVIDENCE PACKET
All fabricated inputs are written beneath PACKET/scratch, with no bench access.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
tmp=packet/'scratch'/'reduction-probes'
tmp.mkdir(exist_ok=True)
receipts=[]
def put(p,obj):p.write_text(json.dumps(obj,indent=1)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def invoke(name,args):
    p=subprocess.run([sys.executable,'-I',str(root/'tools'/name),*map(str,args)],
                     capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=30)
    return p
def check(name,ok,observed):
    assert ok,name
    receipts.append(dict(control=name,result='PASS',observed=observed))

# Exercise the public-only B0 reduction on a disposable copy.
b0=tmp/'b0'
b0.mkdir(exist_ok=True)
for name in ['summary/b0-2/c-b9-grade.json','summary/b0-2/align-a-c.json',
             'summary/b0-2/align-b-c.json','summary/b0-2/a-peer-tap.json',
             'runs/b0-2/events.jsonl','tools/run_b16.py']:
    dest=b0/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,dest)
f=b0/'summary/b0-2/align-a-c.json';d=json.loads(f.read_text());d['covered_recording_frames'][1]=1000000;put(f,d)
r=invoke('r2_b0_receipt.py',[b0,tmp/'shortened.json']);d=json.loads((tmp/'shortened.json').read_text())
check('Shortened tap overlap changes attribution',r.returncode==0 and d['overlap']['degraded_inside']==19 and d['overlap']['degraded_beyond']==112,d['overlap'])

# Entirely synthetic console records with independently known word meanings.
spec=importlib.util.spec_from_file_location('poll_receipt',root/'tools/r2_poll_b16c.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
marks={'poll-start':7000000000,'peer-set':7500000000,'dut-set':10000000000,
       'window-start':12000000000,'window-end':15000000000,'restored':16000000000}
rows=[]
for n,start in enumerate(range(7,18),1):
    state=0 if start<10 or start>=16 else (3 if start<12 else 4)
    words={w:'00000000' for w in module.WORDS}
    words.update({'0x8f8':format((0xffa0<<16)|0x30|state,'08x'),'0x8d4':'000000a2',
                  '0x738':'80000000','0x748':'00001600','0x8e0':'001e0007','0x8e4':'00001600'})
    rows.append(dict(n=n,raw0=start*10**9,raw1=start*10**9+10**8,t0=start,servo_state=state,words=words))
spans={f'{a}..{b}':(marks[a],marks[b]) for a,b in zip(marks,list(marks)[1:])}
spans['restored..poll-end']=(marks['restored'],None)
poll=tmp/'poll-run.jsonl';events=tmp/'events.jsonl'
poll.write_text(''.join(json.dumps(x)+'\n' for x in rows))
ev=[dict(kind='raw',file='poll-run.jsonl',sha256=digest(poll),bytes=poll.stat().st_size),
    dict(kind='bind',t=9.5),dict(kind='poll-summary',marks_raw=marks,spans=module.published_rule(rows,spans))]
events.write_text(''.join(json.dumps(x)+'\n' for x in ev))
receipt=tmp/'poll-receipt.json';trace=tmp/'trace.tsv'
r=invoke('r2_poll_b16c.py',[poll,events,receipt,trace]);d=json.loads(receipt.read_text())
check('Synthetic poll decodes signed trim and rates',r.returncode==0 and d['spans']['window-start..window-end']['trim_ppm']==[-6,-6] and d['spans']['window-start..window-end']['crf_rate_ppm']==[11,11],{'rc':r.returncode,'trim':[-6,-6],'rate':[11,11]})
original=poll.read_bytes();poll.write_bytes(original+b' ')
badout=tmp/'should-not-exist.json';badtrace=tmp/'should-not-exist.tsv'
r=invoke('r2_poll_b16c.py',[poll,events,badout,badtrace])
check('Changed raw bytes refused before output',r.returncode==2 and not badout.exists() and not badtrace.exists(),{'rc':r.returncode,'output_written':badout.exists()})
poll.write_bytes(original)
for row in rows:
    if row['raw0']>=13000000000:row['words']['0x8d4']='000000a4'
poll.write_text(''.join(json.dumps(x)+'\n' for x in rows))
ev[0].update(sha256=digest(poll),bytes=poll.stat().st_size)
events.write_text(''.join(json.dumps(x)+'\n' for x in ev))
r=invoke('r2_poll_b16c.py',[poll,events,receipt,trace]);d=json.loads(receipt.read_text())
check('Planted post-lock step is exposed and old summary rejected',r.returncode==1 and not d['matches_published_summary'] and len(d['slip_lb_steps'])==1 and d['slip_lb_steps'][0]['servo']==['LOCKED','LOCKED'],{'rc':r.returncode,'steps':d['slip_lb_steps']})

# A synthetic role map verifies disclosure boundaries and changed values.
cmap={'meter':r'^meter/', 'meter_roles':[{'role':'synthetic output','channels':['meter/output']}],
      'level_settings':[{'role':'synthetic output','channels':['level']}],
      'entry_classes':[{'class':'clock setting','match':'clock'}]}
cm=tmp/'synthetic-map.json';put(cm,cmap)
reads=[]
for label,level,clock in [('first',-38.5,0),('second',-30.0,1)]:
    f=tmp/(label+'.json')
    put(f,{'t0':1,'msgs':[{'addr':'meter/output','args':[level,level,-20.0,-20.0,0]},
                        {'addr':'level','args':[-18.5]},{'addr':'clock','args':[clock]}]})
    reads.append({'label':label,'path':str(f),'kind':'state'})
rs=tmp/'reads.json';put(rs,{'reads':reads,'compare':[['first','second']]})
r=invoke('r2_source_b16.py',[cm,rs,tmp/'source.json']);d=json.loads((tmp/'source.json').read_text())
check('Source extraction preserves changed class, level and hashes',r.returncode==0 and d['compare'][0]['differ']==1 and d['reads']['second']['meters']['synthetic output'][0]['leaving_dbfs']==[-30,-30,-30] and d['reads']['second']['sha256']==digest(tmp/'second.json'),{'rc':r.returncode,'differ':1,'meter':[-30,-30,-30],'hash_bound':True})
(packet/'reduction-probes.json').write_text(json.dumps({'controls':receipts,'all_pass':True},indent=2)+'\n')
print('PASS:',len(receipts),'independent reduction controls')
