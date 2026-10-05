#!/usr/bin/env python3
"""Check publication boundaries and make a relative-path checksum manifest.

Usage: python3 package_packet.py PACKET_DIRECTORY REPOSITORY EVIDENCE_ROOT
"""
import hashlib
import json
import re
import sys
from pathlib import Path

packet,repo,evidence=map(Path,sys.argv[1:])
sys.path.insert(0,str(repo/'scripts'))
import docs_check
report=(packet/'REPORT.md').read_text()
assert report.splitlines()[0]=='[R498] NEGATIVE - exact head bef8dd7036f711bf286929fa4cba6bf724c7118d'
assert report.splitlines()[-1]=='R498-1 FINISHED' and 'SKELETON' not in report
assert all('| '+lens+' |' in report for lens in ('Conformance','RTL','Robustness','Tests','Docs'))
identity=json.loads((evidence/'author/identity.json').read_text())
raw=bytes.fromhex(identity['descriptor_payload'])
private=[m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{6,}',raw)
         if m.start() in (52,248)]
files=[packet/'REPORT.md']+[f for name in ('scripts','receipts') for f in (packet/name).rglob('*') if f.is_file()]
errors=[]
for f in files:
    data=f.read_text()
    for pattern,category,*_ in (*docs_check.IDENTITY_RULES,*docs_check.LOCAL_RULES):
        if pattern.search(data):errors.append({'file':str(f.relative_to(packet)),'class':category})
    for value in private:
        if value in data or value.encode().hex() in data.lower():
            errors.append({'file':str(f.relative_to(packet)),'class':'identity value'})
assert not errors,json.dumps(errors)
receipt=packet/'receipts/packet-verification.json'
receipt.write_text(json.dumps({'report_format':'PASS','all_five_lenses_present':True,
                               'publication_privacy':'PASS','scratch_excluded':True},indent=2)+'\n')
files=sorted(set(files+[receipt]))
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(packet))+'\n' for f in files)
(packet/'MANIFEST.sha256').write_text(manifest)
print('PASS: report format, publication privacy, scratch exclusion')
print('Manifest entries: '+str(len(files)))
