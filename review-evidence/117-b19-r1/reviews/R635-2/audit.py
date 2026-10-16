#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index and gitlinks; audit the public packet hashes.
Usage: audit.py REPOSITORY AUTHOR_PACKET PUBLIC_MANIFEST OUTPUT_PACKET
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo, author, manifest, out = map(Path, sys.argv[1:])
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args],env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})
head=git('rev-parse','HEAD').decode().strip()
tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='c2243f791ced37dd2288dbf870758d93c5aa5325'
assert tree=='ece348805565c8c0b12bd6c90eccf512ef46c222'
expected={}
failures=[]
links={}
for entry in git('ls-tree','-r','-z','HEAD').split(b'\0'):
    if not entry: continue
    meta,name=entry.split(b'\t',1)
    mode,kind,oid=meta.decode().split()
    name=os.fsdecode(name)
    expected[name]=(mode,oid,'0')
    if kind=='commit':
        links[name]=oid
        continue
    path=repo/name
    s=path.lstat()
    if mode=='120000':
        assert stat.S_ISLNK(s.st_mode), name
        data=os.fsencode(os.readlink(path))
    else:
        assert stat.S_ISREG(s.st_mode), name
        assert bool(s.st_mode & stat.S_IXUSR)==(mode=='100755'),name
        data=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=oid: failures.append(name)
actual={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if entry:
        meta,name=entry.split(b'\t',1)
        actual[os.fsdecode(name)]=tuple(meta.decode().split())
assert actual==expected
assert not failures
rows=[r for r in json.loads(manifest.read_text()) if r['file'].startswith('author-r2/')]
bad=[]
redacted=0
for row in rows:
    data=(author.parent/row['file']).read_bytes()
    if hashlib.sha256(data).hexdigest()!=row['published_sha256']: bad.append(row['file'])
    redacted+=bool(row['path_redacted'])
assert not bad
receipt=dict(head=head,tree=tree,tracked_entries=len(expected),tracked_blob_mismatches=failures,
             index_equal=True,tracked_modes_equal=True,gitlinks=links,submodules_initialized=False,
             public_packet_rows=len(rows),public_packet_mismatches=bad,public_redacted_rows=redacted,
             evidence_commit='633b6e33244545b0dd5a1ef9a01fb96a0209d35e',
             signature_status='Git reports N: no commit signature. Verification is by object ID and SHA-256 manifests.')
(out/'integrity.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
