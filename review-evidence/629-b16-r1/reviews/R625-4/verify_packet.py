#!/usr/bin/env python3
"""Verify public author files without opening review reports. Usage: verify_packet.py REPO OUT_JSON."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo, out = map(Path,sys.argv[1:3])
ref='b83e5d76ede6597eb9831c2a90b0a1058abc85aa'
base='review-evidence/629-b16-r1/'
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
manifest=json.loads(git('show',ref+':'+base+'MANIFEST.json'))
rows=[x for x in manifest if x['file'].split('/')[0] in ['author-r1','author-r2','author-r3','author-r4']]
batch=git('cat-file','--batch') if not rows else subprocess.run(
    ['git','-C',str(repo),'cat-file','--batch'],
    input=''.join(ref+':'+base+x['file']+'\n' for x in rows).encode(),capture_output=True,check=True).stdout
pos=0; counts=collections.Counter(); reds=collections.Counter()
for x in rows:
    end=batch.index(b'\n',pos); head=batch[pos:end].decode().split(); assert head[1]=='blob'
    size=int(head[2]); data=batch[end+1:end+1+size]; pos=end+2+size
    assert hashlib.sha256(data).hexdigest()==x['published_sha256'],x['file']
    assert (x['original_sha256']!=x['published_sha256'])==x['path_redacted'],x['file']
    counts[x['file'].split('/')[0]]+=1
    if x['path_redacted']:reds[x['file'].split('/')[0]]+=1
inner=git('show',ref+':'+base+'author-r4/MANIFEST.sha256').decode()
lookup={x['file']:x for x in rows}; matched=0
for line in inner.splitlines():
    h,path=line.split(maxsplit=1); path=Path(path.lstrip('*')).as_posix()
    assert lookup['author-r4/'+path]['original_sha256']==h,path
    matched+=1
result={'evidence_commit':ref,'publication_manifest_sha256':hashlib.sha256(git('show',ref+':'+base+'MANIFEST.json')).hexdigest(),
        'author_files_verified':dict(counts),'redacted_files':dict(reds),'author_r4_original_manifest_rows':matched,
        'review_report_contents_read':False,'status':'PASS'}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
