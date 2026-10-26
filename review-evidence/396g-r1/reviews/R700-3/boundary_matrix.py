#!/usr/bin/env python3
"""Independent guarded endpoints, mask lengths and compound events."""
import hashlib
import json
from pathlib import Path
import struct
import sys

out=Path(__file__).resolve().parent
# Reuse only the unchanged independent encoder and arm log, not its probes.
exec((out/'delta_probes.py').read_text().split('rows=[]')[0])
rows=[]
def grade(name,ops=(),frames=N,order='big',chunk=None,required=None):
    global arms
    original_arms=arms
    if frames>2*N:
        arms=[dict(a,index=frames-(N-a['index'])) if a['index']>N//2 else dict(a) for a in arms]
    b=capture(ops,frames)
    if order=='little':
        b=b''.join(b[i:i+4][::-1] for i in range(0,len(b),4))
    data=b if chunk is None else [b[i:i+chunk] for i in range(0,len(b),chunk)]
    span=frames/RATE
    v,d=t.grade_audio_counter_capture(data,t.CounterCapture(C,order,RATE,100.,200.,
        anchors=((frames,100.+span,200.+span),),gptp_steps_wall_s=()),t.CounterRunLog(arms,[],0),
        required_s=(frames-126)/RATE if required is None else required)
    ev=[e for e in d.get('events',[]) if e['attribution']=='dut']
    row=dict(name=name,ops=ops,frames=frames,order=order,chunk=chunk,verdict=v,
             qualified=d.get('qualified'),why=d.get('why'),missed=d.get('planted_missed'),
             sha256=hashlib.sha256(b).hexdigest(),events=ev)
    rows.append(row)
    arms=original_arms
    return v,d,ev

for order in ('big','little'):
    for chunk in (None,113):
        for at,n in ((8191,2048),(8190,8192),(8191,4096),(8172,4096),(10,4096),(30,4096)):
            for guards in (0,64,128):
                grade(f'boundary-{at}-{n}-guard-{guards}-{order}-{chunk}',[('shift',at,n)],
                      frames=N+guards,order=order,chunk=chunk)
        grade(f'clean-{order}-{chunk}',order=order,chunk=chunk)
        grade(f'whole-capture-required-{order}-{chunk}',required=N/RATE,order=order,chunk=chunk)

for n in (63,64,65,100,65535,65536,65537,66000):
    for mask in (0x100,0x80000,0x200):
        v,d,ev=grade(f'mask-{mask:x}-{n}',[('xor',1000,n,2,mask)],frames=max(N,n+6000),chunk=113)
        good=v=='FAIL' and not d['planted_missed'] and all(e['class']=='bit-flip' and
             e['mask']==f'0x{mask:08X}' and e['channel']==2 for e in ev) and sum(e['n'] for e in ev)==n
        rows[-1]['matches_constant_mask_rule']=good

for shift in (3,-2,4096):
    for gap in (1,2,5,40,63):
        for mask in (0x100,0x80000):
            v,d,ev=grade(f'compound-{shift}-{gap}-{mask:x}',[('shift',3000,shift),('xor',3000+gap,1,2,mask)])
            slips=[e for e in ev if e['class']==('dropped' if shift>0 else 'repeated')]
            flips=[e for e in ev if e['class']=='bit-flip']
            rows[-1]['matches_compound_rule']=(v=='FAIL' and not d['planted_missed'] and
                len(slips)==4 and all(e['n']==abs(shift) for e in slips) and len(flips)==1 and
                flips[0]['capture_index']==3000+gap and flips[0]['n']==1 and flips[0]['mask']==f'0x{mask:08X}')

(out/'boundary-matrix.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:
    print(row['name'],row['verdict'],row.get('matches_constant_mask_rule',row.get('matches_compound_rule','')),
          len(row['events']),[(e['class'],e.get('n'),e.get('unresolved')) for e in row['events'][:4]],flush=True)
print('ROWS',len(rows))
