#!/usr/bin/env python3
"""Independently compare retained censuses and raw controller exchanges."""
import json
from pathlib import Path
import sys

p = Path(sys.argv[1])


def rows(name):
    return [json.loads(s) for s in (p / name).read_text().splitlines()]


def stable(x):
    if isinstance(x, dict):
        return {k:stable(v) for k,v in x.items() if k not in ('t','seq','rtt_ms','sequence_id','t_tx','t_rx')}
    if isinstance(x, list):
        return [stable(v) for v in x]
    return x


result = {}
for suffix in ('','b','c'):
    before, after = [list(map(stable, rows(f'restore/census-{end}{suffix}.jsonl'))) for end in ('start','end')]
    diff = [i for i,(x,y) in enumerate(zip(before, after)) if x != y]
    assert len(before)==len(after)==46 and diff==[8]
    x,y = before[8],after[8]
    assert x['cmd']==y['cmd']=='GET_AVB_INFO'
    assert {k:v for k,v in x.items() if k!='payload'} == {k:v for k,v in y.items() if k!='payload'}
    for name in ('clock','format','map'):
        assert all(x==y for x,y in zip(before,after) if name in str(x.get('what','')))
    result['B16'+suffix] = {'entries':46, 'equal':45, 'only_difference':{'before':x,'after':y}}

for run in ('bcrf','baaf'):
    ctl = rows(f'runs/{run}/ctl.jsonl')
    records = [r['line'] for r in ctl if isinstance(r.get('line'),dict)]
    clock = [r for r in records if r.get('cmd') in ('SET_CLOCK_SOURCE','GET_CLOCK_SOURCE')]
    pairs = []
    for i,r in enumerate(clock):
        if r['cmd']!='SET_CLOCK_SOURCE':
            continue
        following = next(z for z in clock[i+1:] if z['cmd']=='GET_CLOCK_SOURCE' and z['role']==r['role'])
        assert r['status']==following['status']=='SUCCESS'
        # Descriptor type/index and clock source are the first six bytes.
        # The last two bytes are reserved, not the selected source.
        assert r['payload'][:12]==following['payload'][:12]
        pairs.append({'role':r['role'], 'source':int(r['payload'][8:12],16),
                      'set_get_fields_equal':True, 'set_payload':r['payload'],
                      'get_payload':following['payload']})
    assert [(r['role'],r['source']) for r in pairs] == [('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
    result[run] = {'clock_pairs':pairs}
print(json.dumps(result,indent=2))
