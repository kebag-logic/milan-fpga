#!/usr/bin/env python3
"""Audit immutable public source-bank and PP artifacts without running them."""
import hashlib
import json
from pathlib import Path
import re

OUT=Path(__file__).resolve().parent
P=OUT/'public-evidence/review-evidence/520-r1'
manifest={r['file']:r for r in json.loads((P/'MANIFEST.json').read_text())}
verified=[]
for f in P.rglob('*'):
    if f.is_file() and f.name!='MANIFEST.json':
        key=str(f.relative_to(P));row=manifest[key]
        assert hashlib.sha256(f.read_bytes()).hexdigest()==row['published_sha256'],key
        verified.append(key)
pp=P/'author/final-pp'
samples={}
for label in ['01-cold','04-changed','06-changed-uncached']:
    folder=pp/'runs'/(label+'.trace.artifacts')
    staged=folder/'KL_pp_shadow.v'
    cells=json.loads((folder/'KL_pp_shadow.stat.json').read_text())['design']['num_cells']
    images={n:(folder/n).read_bytes() for n in ['gptp_ucode.hex','ltn_rom.hex','ucode.hex']}
    digest=hashlib.sha256(b''.join(n.encode()+b'\0'+len(b).to_bytes(8,'big')+b for n,b in images.items())).hexdigest()
    row=manifest[str(staged.relative_to(P))]
    samples[label]={'cells':cells,'rom_digest':digest,
                    'staged_published_sha256':row['published_sha256'],
                    'staged_original_sha256':row['original_sha256'],
                    'path_redacted':row['path_redacted'],
                    'image_sha256':{n:hashlib.sha256(b).hexdigest() for n,b in images.items()}}
assert samples['01-cold']['cells']==1141365
assert samples['04-changed']['cells']==samples['06-changed-uncached']['cells']==1122602
assert len({x['staged_published_sha256'] for x in samples.values()})==1
assert len({x['staged_original_sha256'] for x in samples.values()})==1
records=[]
for f in (pp/'head-cache').glob('*/record'):
    r=dict(line.split('=',1) for line in f.read_text().splitlines())
    assert int(r['cells'])==json.loads((f.parent/'stat.json').read_text())['design']['num_cells']
    sample=next(s for s in samples.values() if s['cells']==int(r['cells']))
    assert r['sv2v_sha256']==sample['staged_original_sha256']
    assert r['rom_sha256']==sample['rom_digest']
    records.append(r)
assert {k for k in records[0] if records[0][k]!=records[1][k]}=={'cells','rom_sha256'}
summary={'public_manifest_files_verified':len(verified),'pp_samples':samples,'manager_banks':{}}
mgr=P/'source/manager'
for name,count in [('manager-builder',48),('full-native',5)]:
    data=json.loads((mgr/name/'results.json').read_text())
    assert data['head']=='28e350b99ac240a750326b762c6d029f0653362c'
    assert data['base']=='483a133ed08867ea0d300d2b4a027b5b48a4282f'
    assert len(data['results'])==count and all(r['exit_code']==0 for r in data['results'])
    summary['manager_banks'][name]={'commands':count,'head':data['head'],'base':data['base'],'exits':[r['exit_code'] for r in data['results']]}
assert '--cache' not in json.loads((mgr/'full-native/results.json').read_text())['results'][1]['command']
tops=list((mgr/'yosys-results').glob('top-*.result'))
assert len(tops)==54
inventory=set((OUT/'inventory.txt').read_text().splitlines())
for f in tops:
    fields=dict(line.split('=',1) for line in f.read_text().splitlines())
    assert fields['status']=='PASS' and fields['mode']=='full' and fields['cells'].isdigit()
    assert fields['name'] in inventory
    inventory.remove(fields['name'])
assert not inventory
summary['manager_yosys_top_records']=len(tops)
summary['physical_limits']={'field_campaigns':'four declared skips; ran nothing',
                           'builder_calibration':'physical_calibration_evidence NOT RUN'}
(OUT/'public-evidence-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
