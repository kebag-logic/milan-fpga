#!/usr/bin/env python3
"""Reproduce offline grader sensitivity without modifying reviewed inputs.

Arguments: public tools directory, disposable output directory.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np

tools, out = map(Path, sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(tools))
import b21_grade as grade

rng=np.random.default_rng(635)
W=(rng.integers(0,3,(2000,4),dtype=np.uint32)<<8)
W.tofile(out/'wire.samples')
M=W[100:1500].copy()
cases={'clean':M.copy(),'six_frame_skip':np.concatenate([M[:300],M[306:]]),
       'one_frame_repeat':np.concatenate([M[:500],M[499:]]),
       'three_zero_insertions':np.concatenate([M[:800],np.zeros((3,4),dtype='u4'),M[800:]])}
# The implementation treats a 64-bit digest as exact equality of 128-bit frames.
P=1000003;MASK=(1<<64)-1
def key(a):
    k=0
    for x in a:k=((k*P)&MASK)^int(x)
    return k
collision=M.copy();details=None
for j in range(100,1000):
    a=[int(x) for x in M[j]];b=a.copy();b[2]^=256
    ka=key(a[:3]);kb=key(b[:3]);delta=((ka*P)&MASK)^((kb*P)&MASK)
    if delta<2**32:
        b[3]^=delta
        assert a!=b and key(a)==key(b)
        collision[j]=b;details={'frame':j,'before':a,'after':b,'same_key':key(a)};break
assert details
cases['unequal_words_same_hash']=collision
results={}
for name,a in cases.items():
    a.astype('<u4').tofile(out/(name+'.pcm'))
    r=subprocess.run([sys.executable,'-B',str(tools/'b21_grade.py'),'mcasp',str(out),name,str(out/'wire.samples'),'4',str(out/name)],capture_output=True,text=True)
    (out/(name+'.stdout')).write_text(r.stdout+r.stderr)
    if r.returncode:
        results[name]={'returncode':r.returncode,'stderr':r.stderr}
        continue
    d=json.loads((out/(name+'-mcasp.json')).read_text());results[name]={'returncode':r.returncode,**d}
assert results['clean']['matched']==len(M) and results['clean']['foreign_frames']==0
assert results['six_frame_skip']['skipped_wire_frames']==6
assert results['one_frame_repeat']['inserted_frames']==1
assert results['three_zero_insertions']['returncode']==1
assert results['unequal_words_same_hash']['matched']==len(M)
assert results['unequal_words_same_hash']['foreign_frames']==0
results['collision_details']=details
print(json.dumps(results,indent=2))
(out/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
