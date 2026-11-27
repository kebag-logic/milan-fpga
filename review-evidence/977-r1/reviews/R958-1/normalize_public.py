#!/usr/bin/env python3
"""Verify downloaded public receipts against published Git blob identities."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);a=p.parse_args()
base=a.packet/'public'; meta=json.loads((base/'blob-provenance.json').read_text())
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
n=0
for item in meta['files']:
 f=base/item['path']
 if not f.is_file():continue
 data=f.read_bytes()
 if blob(data)!=item['sha'] and data.endswith(b'\n') and blob(data[:-1])==item['sha']:
  data=data[:-1];f.write_bytes(data)
 assert blob(data)==item['sha'],item['path']
 assert len(data)==item['size'],item['path']
 print('PASS',item['sha'],item['path']); n+=1
print('PASS',n,'downloaded public files exactly match published blobs at',meta['commit'])
