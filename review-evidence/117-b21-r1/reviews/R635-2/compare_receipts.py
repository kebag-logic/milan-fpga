#!/usr/bin/env python3
"""Compare replayed issue #117 figures, page table and public gate receipts.

Usage: compare_receipts.py PUBLIC_AUTHOR_PACKET CHECKOUT OUTPUT_DIRECTORY
"""
import json
from pathlib import Path
import re
import sys

author, checkout, out = map(Path,sys.argv[1:4])
r = out/'receipts'
mapping = {
    'bound-as-measured.json':'pr2/rA/rA-bound.json',
    'restart-controls.json':'pr2/rA/rA-controls.json',
    'direction-b-mcasp.json':'pr2/dB/dB-mcasp.json',
    'direction-b-exact.json':'pr2/dB/dB-exact.json',
    'grader-controls.json':'pr2/probes/probes.json',
    'step1.json':'pr2/mst-long/step1-verdict.json',
    'transit-crf.json':'pr2/dA/dA-transit-crf.json',
}
matches={}
for ours, published in mapping.items():
    a=json.loads((r/ours).read_text())
    b=json.loads((author/published).read_text())
    if ours=='transit-crf.json':
        a.pop('inputs'); b.pop('inputs')
    matches[ours]=a==b
published_floors=(author/'pr2/mst-long/floor-groups.txt').read_text()
published_floors=published_floors.replace('mst-long.ts','selftest-times').replace('mst-long.samp','selftest-sampler')
matches['floor-groups.txt']=(r/'floor-groups.txt').read_text()==published_floors
page=(checkout/'docs/findings/117_AUDIO_CONTINUITY.md').read_text()
section=page.split('### B21 round 3: corrections after review',1)[1]
printed=re.findall(r'^\| (\d+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| yes \|$',section,re.M)
bound=json.loads((r/'bound-as-measured.json').read_text())
table=[]
for printed_row,row in zip(printed,bound['cycles']):
    cycle,lo,hi,width=printed_row
    expected=[f"{row['lower_s']*1000:.1f}",f"{row['upper_s']*1000:.1f}",f"{(row['upper_s']-row['lower_s'])*1000:.1f}"]
    table.append(dict(cycle=int(cycle),equal=int(cycle)==row['cycle'] and [lo,hi,width]==expected))
old=[]
for name, maximum in [('st-long',4.5),('st-long2',7.8)]:
    text=(author/f'selftest/{name}/{name}-selftest.txt').read_text()
    rows=re.findall(r'loss at t\s+([\d.]+) s:.*?USB shortfall ([+-][\d.]+)',text)
    old.append(dict(run=name,losses=len(rows),above_control=sum(float(v)>maximum for _,v in rows),
                    exceptions=[dict(time_s=float(t),shortfall=float(v)) for t,v in rows if float(v)<=maximum]))
gates=(author/'pr2/gates-head/gates.txt').read_text()
gate_rows=re.findall(r'gate-(\d+) rc=(\d+):',gates)
gate_summary=[]
for n,rc in gate_rows:
    text=(author/f'pr2/gates-head/gate-{n}.txt').read_text()
    gate_summary.append(dict(gate=int(n),rc=int(rc),first_line=text.splitlines()[0] if text.splitlines() else '(empty successful receipt)'))
result=dict(replayed_equals_published=matches,table_rows=len(printed),table=table,
            prior_loss_counts=old,source_gate_head=gates.splitlines()[0],source_gates=gate_summary)
(r/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(matches.values()) and len(printed)==20 and all(x['equal'] for x in table)
assert len(gate_rows)==11 and all(rc=='0' for _,rc in gate_rows)
