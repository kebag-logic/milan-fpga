#!/usr/bin/env python3
"""Select verbatim runtime output and describe public evidence without host paths."""
import csv
import hashlib
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1]
r = p/'receipts'
provenance = []
for name in ['head-engine-suite', 'head-length-probe', 'base-length-probe',
             'head-edge-control', 'reserved-word-mutant']:
    raw = (r/(name+'.log')).read_bytes()
    lines = raw.splitlines(keepends=True)
    selected = b''.join(line for line in lines if line.startswith(
        (b'LENGTH ', b'SEMANTICS ', b'REVIEW_', b'EDGE ', b'aecp_cmds:', b'aecp_cmds sweep:')))
    assert selected
    out = name+'.runtime.log'
    (r/out).write_bytes(selected)
    provenance.append({'receipt': out, 'full_log_sha256': hashlib.sha256(raw).hexdigest(),
                       'runtime_sha256': hashlib.sha256(selected).hexdigest(),
                       'selection': 'Verbatim complete runtime result lines; build transcript excluded.',
                       'rc': int((r/(name+'.rc')).read_text())})
(r/'runtime-provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')

checks=[]
for item in json.loads((r/'public/MANIFEST.json').read_text()):
    actual=hashlib.sha256((r/'public'/item['file']).read_bytes()).hexdigest()
    assert actual==item['published_sha256']
    checks.append({'artifact':item['file'], 'sha256':actual, 'matches_published_manifest':True})
rom=[]
for name in ['base-length-probe','head-length-probe']:
    raw=(p/'scratch'/name/'tb/aecp_cmds/ucode.hex').read_bytes()
    rom.append({'revision':name,'sha256':hashlib.sha256(raw).hexdigest()})
assert rom[0]['sha256']==rom[1]['sha256']
(r/'artifact-checks.json').write_text(json.dumps({'public_artifacts':checks,'generated_rom':rom},indent=2)+'\n')

rows=list(csv.DictReader((r/'public/author/EXTERNAL-RECORDS.csv').open()))
parent=[row for row in rows if row['path (under the scratch root)'].startswith(('cons/base/','cons/head/','cons/devpin/'))
        and any(x in row['path (under the scratch root)'] for x in ['check_submodule_docs','measure_test_evidence','milan_dp'])]
(r/'parent-record-index.json').write_text(json.dumps(parent,indent=2)+'\n')

hosted=[]
for f in sorted(r.glob('jobs-*.json')):
    for j in json.loads(f.read_text())['jobs']:
        hosted.append({key:j[key] for key in ['id','run_id','head_sha','name','status','conclusion','html_url','started_at','completed_at','steps']})
(r/'hosted-summary.json').write_text(json.dumps(hosted,indent=2)+'\n')
print('Runtime receipts, published artifact hashes, identical ROM hash, parent digest index and hosted step snapshot prepared.')
