#!/usr/bin/env python3
"""Validate the report and write a relative SHA-256 publication manifest."""
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

packet=Path(sys.argv[1]).resolve()
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R891] POSITIVE - exact head 55852269db3554900d2b71e6f9a7b153cff69e14'
assert report.splitlines()[-1]=='R891-2 FINISHED'
assert 'SKELETON' not in report
gates=json.loads((packet/'receipts/validate/gates.json').read_text())
assert len(gates)==28 and all(x['rc']==0 for x in gates)
mutants=json.loads((packet/'receipts/validate/mutations/results.json').read_text())
assert len(mutants)==479 and all(x['status']=='CAUGHT' for x in mutants)
assert json.loads((packet/'integrity-after.json').read_text())['bytes_modes_index_match']
files=[]
for p in sorted(packet.rglob('*')):
    if not p.is_file(): continue
    relative=p.relative_to(packet)
    if 'scratch' in relative.parts or p.name in ('MANIFEST.sha256','prior-findings.json'):
        continue
    if p.suffix=='.xml': ET.parse(p)
    files.append((relative,hashlib.sha256(p.read_bytes()).hexdigest()))
(packet/'MANIFEST.sha256').write_text(''.join(digest+'  '+str(relative)+'\n' for relative,digest in files))
print('Report finalized;',len(files),'files listed; scratch and copied prior reports excluded.')
