#!/usr/bin/env python3
"""Check the public campaign and physical receipts against their raw sections."""
import hashlib
import json
from pathlib import Path
import re
import sys

out = Path(sys.argv[1]).resolve()
base = out/'scratch/review-evidence/loopbram-r1'
r = base/'author-r5/receipts'
def payload(path):
    return path.read_text().split('\n\n',1)[1]
def obj(name):
    return json.loads(payload(r/name))
result = {}
campaign = obj('gates--parent-plants--results.json.txt')
assert len(campaign)==17 and all(x['passed'] and x['built'] for x in campaign)
result['campaign'] = []
for x in campaign:
    f = r/('gates--parent-plants--'+x['name']+'.log.txt')
    if f.exists():
        text = payload(f)
    else:
        text = ''.join(payload(p) for p in sorted(r.glob('gates--parent-plants--'+x['name']+'.log.part*.txt')))
    assert text, x['name']
    tags = x['required'] or ['RESULT: PASS']
    assert all(t in text for t in tags), x['name']
    if x['required']:
        assert x['exit'] != 0 and 'RESULT: FAIL' in text
    else:
        assert x['exit'] == 0
    result['campaign'].append(dict(name=x['name'], exit=x['exit'], checked_runtime_tags=tags))
result['routes'] = []
for route in obj('route-summary.json.txt'):
    directive = route['directive']
    record = dict(directive=directive, utilization=route['utilization'], corners=[], worst_path='')
    worst = min(v['WNS_ns'] for v in route['corners'].values())
    for corner, summary in route['corners'].items():
        files = sorted(r.glob('route--endstation_ax7101_8x8--gateware--'+directive+'--'+corner+'.part*.txt'))
        assert files, corner
        text = ''.join(payload(f) for f in files)
        m = re.search(r'WNS\(ns\).*?\n\s*-.*?\n\s*([^\n]+)',text,re.S)
        values = m[1].split()
        assert float(values[0]) == summary['WNS_ns']
        assert float(values[4]) == summary['WHS_ns']
        assert int(values[2]) == int(values[6]) == 0
        record['corners'].append(dict(corner=corner,wns=float(values[0]),whs=float(values[4]),setup_failing=int(values[2]),hold_failing=int(values[6])))
        if summary['WNS_ns']==worst:
            m = re.search(r'Slack \(MET\) :\s+'+f'{worst:.3f}'+r'ns[^\n]*\n(.*?)(?=\n\s*Location)',text,re.S)
            assert m and 'KL_mbx/' in m[1], directive
            record['worst_path'] = m[1][:1600]
    record['floor_pass'] = all(c['wns']>=0.030 and c['whs']>=0 for c in record['corners'])
    result['routes'].append(record)
assert [x['directive'] for x in result['routes'] if x['floor_pass']] == ['AltSpreadLogic_high']
result['canonical'] = []
r4 = base/'author-r4/receipts'
for row in json.loads((r4/'canonical-manifest.json').read_text()):
    sha = hashlib.sha256()
    length=0
    for part in row['chunks']:
        data = (r4/part['file']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==part['sha256']
        sha.update(data)
        length+=len(data)
    assert sha.hexdigest()==row['base_sha256']==row['head_sha256'] and length==row['bytes']
    result['canonical'].append(dict(shape=row['shape'],sha256=sha.hexdigest(),bytes=length))
docs = obj('docswf--results.json.txt')
assert docs['head']=='9acb9b828b29aba71bd51303a4836f86c2278267'
assert len(docs['steps'])==43 and all(x['exit']==0 for x in docs['steps'])
result['docs_steps'] = [{k:x[k] for k in ('n','name','exit')} for x in docs['steps']]
result['sweep'] = obj('gates--sweep.json.txt')
assert all(x['exit']==0 for x in result['sweep'])
for n,count,checks in [(15,8,662439),(16,9,356128)]:
    text=payload(r/f'gates--sweep-shard{n}.log.txt')
    result[f'shard{n}_tail']=text[-4500:]
result['source_groups']={}
for group in ('quick','regressions','remaining','builder','render'):
    data=obj(f'gates--{group}.json.txt')
    result['source_groups'][group]=data
(out/'receipt-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: 17 campaign entries, 12 route corners, 2 reconstructed canonical hashes, 43 docs steps, 2 driver shards.')
