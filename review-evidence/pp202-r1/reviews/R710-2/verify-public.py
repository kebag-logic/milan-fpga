#!/usr/bin/env python3
"""Check downloaded public bytes against the immutable manifest and Git tree."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
def digest(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
mfile=p/'public-manifest.json'
b=mfile.read_bytes()
if blob(b[:-1])=='125cd71bd9d958885b232d674ce9e7228f16d4e9': mfile.write_bytes(b[:-1])
assert blob(mfile.read_bytes())=='125cd71bd9d958885b232d674ce9e7228f16d4e9'
manifest={x['file']:x for x in json.loads(mfile.read_text())}
tree={x['path']:x for x in json.loads((p/'public-author-tree.json').read_text())['tree'] if x['type']=='blob'}
selected=json.loads((p/'selected-receipts.json').read_text())
mapping={'public-handoff.md':'HANDOFF.md','public-parent.patch':'parent-src-stream-id-wiring.patch'}
mapping.update({'public/'+x['path']:x['path'] for x in selected})
results=[]
for local,remote in sorted(mapping.items()):
    f=p/local
    if not f.exists() and tree[remote]['size']==0:
        f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b'')
    b=f.read_bytes(); expected=manifest['author-r3/'+remote]['published_sha256']
    # The text transport adds a terminal LF. Remove only when doing so
    # gives exactly the publisher's independently specified digest.
    if digest(b)!=expected and digest(b[:-1])==expected:
        b=b[:-1];f.write_bytes(b)
    assert digest(b)==expected,(local,'sha256')
    assert blob(b)==tree[remote]['sha'],(local,'git blob')
    results.append({'file':local,'sha256':digest(b),'git_blob':blob(b),'verified':True})
sig=json.loads((p/'packet-commit.json').read_text())['verification']
out={'publication':'015d2d6a83eeedc6af5bc3be992b43cf93d2610e','manifest_git_blob':blob(mfile.read_bytes()),'files_verified':len(results),'commit_signature':sig,'files':results}
(p/'public-evidence-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('verified',len(results),'files; publication signature:',sig['reason'])
