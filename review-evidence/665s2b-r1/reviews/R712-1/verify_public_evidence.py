#!/usr/bin/env python3
"""Extract only the listed public executable evidence, checking publication hashes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
rev = 'b447e26340def7706919eff18d41f198c29ae5b9'
base = 'review-evidence/665s2b-r1/'
def read(path):
    return subprocess.check_output(['git','-C',str(root),'show',rev+':'+base+path])
manifest = {item['file']: item for item in json.loads(read('MANIFEST.json'))}
paths = (packet/'public-evidence-integrity.log').read_text().splitlines()[2:]
out = packet/'scratch/public-evidence'
for path in paths:
    assert '/receipts/' in path or '/scripts/' in path or '/donor' in path, path
    data = read(path)
    digest = hashlib.sha256(data).hexdigest()
    assert digest == manifest[path]['published_sha256'], path
    target = out/path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
print(len(paths), 'public artifacts verified at', rev)
