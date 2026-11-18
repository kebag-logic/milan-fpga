#!/usr/bin/env python3
"""Verify published receipt hashes without opening reviewer reports."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
ref='66fea879135dec78ecfb2410d5dc2115c1a29077';base='review-evidence/train1117-r1/'
def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
data=json.loads(git('show',ref+':'+base+'MANIFEST.json'))
proc=subprocess.Popen(['git','-C',str(root),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
failed=[];size=0
for row in data:
 proc.stdin.write((ref+':'+base+row['file']+'\n').encode());proc.stdin.flush()
 header=proc.stdout.readline().split();n=int(header[2]);blob=proc.stdout.read(n);proc.stdout.read(1);size+=n
 if hashlib.sha256(blob).hexdigest()!=row['published_sha256']:failed.append(row['file'])
proc.stdin.close();assert proc.wait()==0
header=git('cat-file','commit',ref).split(b'\n\n',1)[0]
paths=git('ls-tree','-r','--name-only',ref,'--',base).decode().splitlines()
signatures=[name for name in paths if name.endswith(('.sig','.asc','.pub')) or 'signature' in name.lower()]
result={'archive_commit':ref,'entries':len(data),'bytes_verified':size,'hash_mismatches':failed,'commit_signature_present':b'\ngpgsig ' in header,'detached_signature_candidates':signatures,'claim':'Manifest consistency only; no signer authenticity established.'}
(packet/'evidence-verification.json').write_text(json.dumps(result,indent=2)+'\n')
assert not failed
print(json.dumps(result,indent=2))
