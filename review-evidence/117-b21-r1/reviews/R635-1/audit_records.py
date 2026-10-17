#!/usr/bin/env python3
"""Verify public manifests, selected raw hashes, CSR state and format transactions.

Arguments: extracted evidence directory, retained raw directory, receipt destination.
No private host inventories, handoffs or other review reports are read.
"""
import concurrent.futures as cf
import gzip
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
import numpy as np

E,RAW,DEST=map(Path,sys.argv[1:4]);A=E/'author'
manifest=json.loads((E/'MANIFEST.json').read_text());verified=0
for item in manifest:
    p=E/item['file']
    if not p.exists():continue
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['published_sha256'],item['file']
    verified+=1
result={'published_manifest_verified_files':verified}
raws=json.loads((A/'RAW-ARTIFACTS-r3.json').read_text())['files']
wanted=[]
for r in raws:
    name=Path(r['path']).name
    if name.startswith('host-') or not (name.endswith(('.pcap','.pcm','.ts','.samp')) or name in ('cap-lr.raw','cap-ts.bin')):continue
    parts=Path(r['path']).parts;sub=parts[-2]
    candidates=[p for p in (RAW/sub).iterdir() if p.is_file() and p.stat().st_size==r['bytes']]
    if len(candidates)!=1:continue
    wanted.append((sub,name,r,candidates[0]))
def verify(w):
    sub,name,r,p=w;h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    assert h.hexdigest()==r['sha256']
    return {'directory':sub,'kind':p.suffix,'bytes':r['bytes'],'sha256':r['sha256']}
with cf.ThreadPoolExecutor(max_workers=4) as pool:result['raw_media_verified']=list(pool.map(verify,wanted))
result['csr']={}
for run in ['dA','dB']:
    txt=(A/'r3/runs'/run/'dut-poll.txt').read_text();regs={}
    for b in re.split(r'^### ',txt,flags=re.M)[1:]:
        m=re.match(r"(\S+) cmd='mem_read (0x[0-9a-f]+) (\d+)'",b)
        if not m:continue
        base=int(m[2],16);data=b''
        for ln in b.splitlines():
            z=re.match(r'^0x[0-9a-f]{8}\s+((?:[0-9a-f]{2} )+)',ln)
            if z:data+=bytes.fromhex(z[1])
        for k in range(len(data)//4):regs.setdefault(base+4*k,[]).append((m[1],struct.unpack_from('<I',data,4*k)[0]))
    render=np.array([v for t,v in regs[0x900008dc]],dtype='u4')
    row={'samples':len(render),'fill':[int((render&255).min()),int((render&255).max())],
         'prefill_set':int(np.count_nonzero(render&256)),'converged_clear':int(np.count_nonzero((render&512)==0)),
         'max_rails':int((render>>16).max())}
    for addr,name in [(0x900008d4,'SLIP_LB'),(0x900008d8,'SLIP_TDM'),(0x900006b8,'AVTPRX_STAT'),(0x900006c0,'AVTPRX_ERR')]:row[name]=sorted(set(hex(v) for t,v in regs[addr]))
    for addr,name in [(0x90000660,'AAF_FRAMES'),(0x90000664,'AAF_PAIRS')]:
        vs=regs[addr];row[name]={'delta':(vs[-1][1]-vs[0][1])%2**32,'start':vs[0][0],'end':vs[-1][0]}
    result['csr'][run]=row

rows=[json.loads(s) for s in (A/'r3/runs/rA/agent.jsonl').read_text().splitlines() if s.startswith('{')]
fmts=[r for r in rows if r.get('cmd')=='GET_STREAM_FORMAT']
result['restart_formats']={'reads':len(fmts),'status':sorted(set(str(r.get('status')) for r in fmts)),
                           'payloads':sorted(set(r.get('payload','') for r in fmts))}
cy=[json.loads(s) for s in (A/'r3/runs/rA/cycles.jsonl').read_text().splitlines()]
binds=[r for r in cy if r.get('kind')=='bind'];rules=[r for r in cy if r.get('kind')=='binding-rule']
result['restart_bindings']={'count':len(binds),'successful':sum(r['status']==0 for r in binds),
                           'rule_entries':len(rules),'null_comparisons':sum(r['talker'] is None and r['listener'] is None for r in rules)}
result['round1_derived']={}
for name,dt in [('st-long','<u2'),('st-long2','<u4')]:
    d=A/'selftest'/name;meta=json.loads((d/(name+'-reads.json')).read_text());rec=d/meta['record']['file']
    data=rec.read_bytes() if rec.exists() else gzip.decompress(Path(str(rec)+'.gz').read_bytes())
    assert hashlib.sha256(data).hexdigest()==meta['record']['sha256']
    intervals=np.frombuffer(data,dtype=dt);t=np.r_[0,np.cumsum(intervals)]/1e6
    f=np.full(len(t),480,dtype='i8')
    for i,n in meta['reads_not_one_period']:f[i]=n
    delivered=np.cumsum(f);assert delivered[-1]==meta['window_frames'][1]
    D=t*48000-(delivered-delivered[0]);W=10;GB=3;GA=2
    pos=np.arange(GB+W,len(intervals)-GA-W)
    steps=np.array([D[x+GA:x+GA+W+1].min()-D[x-GB-W:x-GB+1].min() for x in pos]);drift=np.median(steps)
    bad=pos[np.abs(steps-drift)>4];groups=[]
    for i in bad:
        if groups and i-groups[-1][-1]<=2*(GB+GA+W+1):groups[-1].append(int(i))
        else:groups.append([int(i)])
    maxima=[max((steps[x-pos[0]]-drift for x in g),key=abs) for g in groups]
    stalls=np.flatnonzero(intervals>15000)+1;spacing=np.diff(t[stalls])
    result['round1_derived'][name]={'intervals':len(intervals),'seconds':float(t[-1]),'stalls':len(stalls),
       'longest_ms':float(intervals.max()/1000),'spacings_2_99_to_3_02':int(np.count_nonzero((spacing>=2.99)&(spacing<=3.02))),
       'step_groups':len(groups),'loss_events_over_1ms':int(sum(x>52 for x in maxima)),
       'loss_frames_over_1ms':float(sum(x for x in maxima if x>52)),
       'median_floor_drift_frames':float(drift),
       'loss_frames_before_drift_subtraction':float(sum(x+drift for x in maxima if x>52)),
       'one_ms_groups':int(sum(abs(x-48)<=4 for x in maxima))}
DEST.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
