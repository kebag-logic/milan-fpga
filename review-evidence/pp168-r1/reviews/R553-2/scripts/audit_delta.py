#!/usr/bin/env python3
"""Audit review boundaries and the single-source record layout without editing source."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
prev = '96d3b78384f34a630d6056ebd8fa5e30f6836650'
head = '66d1b501f4879402fe76485095aef7c6e07c32af'
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True)
paths = git('diff', '--name-only', prev, head).splitlines()
assert len(paths) == 10 and all(p.startswith('docs/') for p in paths)
assert git('rev-parse', head+'^').strip() == prev
protected = ['hdl', 'tb', 'scripts', 'syn', '.github']
unchanged = {}
for p in protected:
    a, b = (git('ls-tree', '-r', rev, '--', p) for rev in (prev, head))
    assert a == b, p
    unchanged[p] = {'identical': True, 'inventory_sha256': hashlib.sha256(a.encode()).hexdigest()}
top = (root/'hdl/top/protocol_processor_top.sv').read_text()
oldtop = git('show', 'ed340b9b85258194247334b85e62cf9c23d4d051:hdl/top/protocol_processor_top.sv')
assert top[:top.index('\n);')] == oldtop[:oldtop.index('\n);')]
doc = (root/'docs/architecture/07_memory_maps.md').read_text()
part = doc[doc.index('<a id="fig-07-sinkrec">'):]
reg = json.loads(part.split('```wavedrom\n', 1)[1].split('```', 1)[0])
offset = 0
fields = []
for field in reg['reg']:
    fields.append({'name': field['name'], 'low': offset, 'high': offset+field['bits']-1})
    offset += field['bits']
assert offset == 384
vlan = next(f for f in fields if f['name']=='settled vlan_id')
sid = next(f for f in fields if f['name']=='settled stream_id')
assert (vlan['low'], vlan['high']) == (304,319)
assert (sid['low'], sid['high']) == (192,255)
print(json.dumps({'head': head, 'previous_head': prev, 'delta_paths': paths,
    'unchanged_implementation': unchanged, 'public_module_header_identical_to_source_base': True,
    'record_bits': offset, 'record_fields': fields}, indent=2))
