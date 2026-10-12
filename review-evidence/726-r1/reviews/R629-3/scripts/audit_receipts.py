#!/usr/bin/env python3
"""Recompute window, packet and named mutation evidence from runtime lines."""
import argparse
import json
from pathlib import Path
import re

def parent(log,shape,baseline=False):
    lines=log.read_text().splitlines();rows=[];services={};tx=[];conditions=[]
    for line in lines:
        if re.match(r'^\d+,[56],\d+,[01],[0-4],\d+,',line):
            values=line.split(',');rows.append([*map(int,values[:6]),*map(float,values[6:])])
        elif line.startswith('SERVICE,'):
            _,ix,cyc=line.split(',');services[int(ix)]=int(cyc)/1000
        elif line.startswith('TX_COUNT,'):tx.append(list(map(int,line.split(',')[1:])))
        elif line.startswith('OUTPUT_CONDITION,'):conditions.append(line.split(',')[1:])
    assert len(rows)==(shape+1)*2*2*5,(log,len(rows))
    steady=[r for r in rows if r[4]>=2]
    assert len(steady)==(shape+1)*2*2*3
    for r in steady:
        assert r[5]==(0 if baseline and r[1]==5 else 1),(log,r)
        if not baseline:
            slot=r[2]+(shape+1 if r[1]==6 else 0)
            assert r[6]>=1000 and r[7]<=1000+services[slot],(log,r,services)
    if not baseline:
        assert all(got==wire and wire>10 for _,got,wire in tx)
    if 'frames-only' in log.name:
        assert len(conditions)==shape+1
        for c in conditions:assert c[1:] == ['frames-only','0','0','1','0','0','0'],c
    return dict(recorded_windows=len(rows),graded_windows=len(steady),
                counts=sorted(set(r[5] for r in steady)),
                minimum_gap_ms=min(r[6] for r in steady),maximum_gap_ms=max(r[7] for r in steady),
                maximum_service_ms=max(services.values()),tx_count_rows=tx,output_conditions=conditions)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);a=ap.parse_args();p=a.packet.resolve();r=p/'receipts'
    result={'parent':{},'mutants':{},'mailbox':{}}
    for shape in (1,8):
        for condition in ('uncertain','frames-only'):
            name=f'{condition}-{shape}'
            result['parent'][name]=parent(r/(name+'.run.log'),shape)
        log=r/f'public/review-round3/standing-before-{shape}__run.log'
        result['parent'][f'published-before-{shape}']=parent(log,shape,True)
    groups={'tx-interval':'TX','rx-interval':'RX','tx-reset':'TX_RESET','aaf-reset':'RX_RESET',
            'crf-reset':'RX_RESET','rx-saturation':'RX','late':'CADENCE','rate':'RATE','tx-nodirty':'OUTPUT_CADENCE'}
    for name,group in groups.items():
        failure=[line for line in (r/(name+'.run.log')).read_text().splitlines() if '[FAIL]' in line]
        assert failure and all('[726 '+group+']' in line for line in failure),(name,failure)
        escape=(r/(name+'.escape.log')).read_text()
        assert '[FAIL]' not in escape and 'RESULT: PASS' in escape,name
        assert (r/(name+'.rc')).read_text().strip()=='0'
        result['mutants'][name]=dict(group=group,failures=len(failure),omission_pass=True)
    for shape in (1,8):
        lines=(r/f'f5-{shape}-clean.run.log').read_text().splitlines()
        rows=[list(map(int,s.split(',')[1:])) for s in lines if s.startswith('F5,')]
        assert len(rows)==(shape+1)*2*2*5
        assert all(s[4]==1 and s[5]>=1000 and s[6]<=1003 for s in rows)
        result['mailbox'][str(shape)]=dict(row_windows=len(rows),min_gap_ms=min(s[5] for s in rows),max_gap_ms=max(s[6] for s in rows))
    for name,group in (('f5-1-late','CADENCE'),('f5-1-rate','RATE')):
        text=(r/(name+'.run.log')).read_text();escape=(r/(name+'.escape.log')).read_text()
        assert '[F5 '+group+']' in text and 'RESULT: PASS' in escape and 'RESULT: FAIL' not in escape
        result['mutants'][name]=dict(group=group,assertion_messages=text.count('[F5 '+group+']'),omission_pass=True)
    (r/'measurement-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
