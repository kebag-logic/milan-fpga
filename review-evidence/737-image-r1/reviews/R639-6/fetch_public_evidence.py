#!/usr/bin/env python3
"""Fetch only the exact public artifacts consumed by verify_evidence.py."""
import hashlib,json,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parent
for row in json.loads((p/'public-evidence-index.json').read_text()):
 data=subprocess.check_output(['gh','api','-H','Accept: application/vnd.github.raw+json','repos/kebag-logic/milan-fpga/git/blobs/'+row['git_blob']])
 assert hashlib.sha256(data).hexdigest()==row['sha256']
 target=p/'scratch/public'/row['name'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print('Public evidence hashes verified')
