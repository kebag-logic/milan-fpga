#!/usr/bin/env python3
"""Verify exact tracked bytes, modes, index, gitlinks and main-merge provenance."""
import argparse, hashlib, json, os, pathlib, subprocess
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('output',type=pathlib.Path); a=p.parse_args(); src=a.source.resolve()
def git(*args): return subprocess.check_output(['git',*args],cwd=src)
def tree(ref):
    result={}
    for row in git('ls-tree','-rz',ref).split(b'\0'):
        if row:
            meta,path=row.split(b'\t'); mode,kind,oid=meta.decode().split(); result[path.decode()]=(mode,kind,oid)
    return result
head='5d03517f2ab42416654a8f2be2f71cfc51d82440'
base='c3bff8f3dea03870ea7ae62965db360b509ee3b3'
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='ea28576a2e51dde5c38be79be870c339f920460f'
ht,bt,ot,lt=tree(head),tree(base),tree('a795471c'),tree('175cf9e')
errors=[]; gitlinks=[]
for path,(mode,kind,oid) in ht.items():
    if mode=='160000': gitlinks.append(dict(path=path,oid=oid)); continue
    f=src/path
    raw=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
    if actual!=oid or actual_mode!=mode: errors.append(path)
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if row:
        meta,path=row.split(b'\t'); mode,oid,stage=meta.decode().split(); assert stage=='0'; index[path.decode()]=(mode,oid)
assert index=={path:(val[0],val[2]) for path,val in ht.items()}
changed_left={f for f in set(ot)|set(lt) if ot.get(f)!=lt.get(f)}
changed_right={f for f in set(ot)|set(bt) if ot.get(f)!=bt.get(f)}
both=changed_left & changed_right
merge_errors=[]
for path in set(ot)|set(lt)|set(bt)|set(ht):
    if path in both: continue
    expected=lt.get(path) if path in changed_left else bt.get(path)
    if ht.get(path)!=expected: merge_errors.append(path)
def content(ref,path): return git('show',ref+':'+path).decode()
old=json.loads(content('a795471c','tests/mutations.json'))
left=json.loads(content('175cf9e','tests/mutations.json'))
right=json.loads(content(base,'tests/mutations.json'))
merged=json.loads(content(head,'tests/mutations.json'))
old_map={r['name']:r for r in old}; left_map={r['name']:r for r in left}
expected=[left_map.get(r['name'],r) if left_map.get(r['name'])!=old_map.get(r['name']) else r for r in right]
assert expected==merged
lc=content('175cf9e','CHANGELOG.md'); oc=content('a795471c','CHANGELOG.md'); rc=content(base,'CHANGELOG.md')
prefix='# Change log\n\n## Unreleased\n\n'
assert lc.endswith(oc.split(prefix)[1])
new_entry=lc[len(prefix):len(lc)-len(oc.split(prefix)[1])]
assert content(head,'CHANGELOG.md')==rc.replace(prefix,prefix+new_entry,1)
assert not errors and not merge_errors
result=dict(head=head,tree=git('rev-parse','HEAD^{tree}').decode().strip(),tracked_entries=len(ht),blob_and_mode_mismatches=errors,index_matches_head=True,gitlinks=gitlinks,submodules='none in this repository',merge_parents=git('rev-list','--parents','-n','1',head).decode().strip(),left_only_files=sorted(changed_left-changed_right),main_only_files=sorted(changed_right-changed_left),overlap_files=sorted(both),merge_provenance_mismatches=merge_errors,mutation_union_exact=True,changelog_addition_exact=True,status=git('status','--porcelain').decode())
a.output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
