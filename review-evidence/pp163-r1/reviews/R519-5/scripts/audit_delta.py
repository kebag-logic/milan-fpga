#!/usr/bin/env python3
"""Independently bind the unchanged logic and the measurement digest delta."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
public = packet/'receipts/public'
old = json.loads((public/'author-r3/measurement-m3final/inputs-digest/inputs-components.json').read_text())
new = json.loads((public/'author-r4/measurement-digest/inputs-components-8947baf.json').read_text())
images = json.loads((public/'author-r3/measurement-m3final/inputs-digest/baseline_images.json').read_text())
def git(*args):
    return subprocess.check_output(['git', *args], cwd=source)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def digest(c):
    h = hashlib.sha256()
    for row in c['files']:
        h.update(row['name'].encode()+b'\0'+bytes.fromhex(row['component_sha256']))
    for g in c['generics']:
        h.update(g.encode()+b'\0')
    for im in sorted(images, key=lambda x:Path(x['path']).name):
        h.update(f"{Path(im['path']).name}\0{im['sha256']}\0".encode())
    return h.hexdigest()
def code(text):
    # Preserve quoted strings, remove comments. Directives remain part of the comparison.
    pattern = r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/'
    stripped = re.sub(pattern, lambda m: m[0] if m[0].startswith('"') else '', text)
    return '\n'.join(line.rstrip() for line in stripped.splitlines() if line.strip())
assert len(old['files']) == len(new['files']) == 124
assert old['generics'] == new['generics']
changed = []
verified = []
for a,b in zip(old['files'],new['files']):
    assert all(a[k]==b[k] for k in ('order','name','path','normalized'))
    if a != b:
        changed.append({'order':a['order'],'name':a['name'],'old':a['component_sha256'],'new':b['component_sha256']})
    if '/protocol-processor/' in a['path']:
        rel = a['path'].split('/protocol-processor/')[1]
        base = git('show','c4539ff1:'+rel)
        head = (source/rel).read_bytes()
        assert sha(base)==a['component_sha256'], rel
        assert sha(head)==b['component_sha256'], rel
        assert code(base.decode())==code(head.decode()), rel
        verified.append({'order':a['order'],'path':rel,'sha256':sha(head),'non_comment_equal':True})
    elif a['order'] in (117,118,119,120):
        name = 'alinx_ax7101.normalized.v' if a['order']==120 else a['name']
        data = (public/'author-r3/measurement-m3final/inputs-digest/inputs'/name).read_bytes()
        assert sha(data)==a['component_sha256']==b['component_sha256']
        verified.append({'order':a['order'],'path':'published inputs/'+name,'sha256':sha(data)})
    elif a['order']==121:
        data = (public/'author-r3/measurement-m3final/ooc-m3final/clock.xdc').read_bytes()
        assert sha(data)==a['component_sha256']==b['component_sha256']
        verified.append({'order':a['order'],'constraint':data.decode(),'sha256':sha(data)})
assert [c['order'] for c in changed]==[46]
assert digest(old)==old['recorded_inputs_sha256']==new['recorded_inputs_sha256_c4539ff1']
assert digest(new)==new['inputs_sha256_8947baf']
diff = git('diff','--unified=0','c4539ff1..HEAD','--','hdl').decode()
changed_lines = [s[1:] for s in diff.splitlines() if s.startswith(('+','-')) and not s.startswith(('+++','---'))]
noncomments = [s for s in changed_lines if s.strip() and not s.lstrip().startswith('//')]
assert not noncomments
hdl_delta = git('diff','--name-only','c4539ff1..HEAD','--','hdl').decode().splitlines()
assert hdl_delta==['hdl/top/protocol_processor_top.sv']
report = {'old_inputs_digest':digest(old),'new_inputs_digest':digest(new),
          'changed_components':changed,'file_components':124,'generics':len(new['generics']),
          'images':len(images),'verified_bytes':verified,'non_comment_changed_lines':len(noncomments),
          'changed_hdl_files':hdl_delta,'remaining_component_records_equal':True,
          'limit':'Unchanged parent/dependency components retain the accepted R519-4 provenance audit; this delta audit rehashes all 46 processor inputs, four supplied generated inputs and the clock constraint.'}
(packet/'receipts/delta-digest-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='verified_bytes'},indent=2))
