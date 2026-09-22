"""Verify parent tracked bytes and index entries directly against the reviewed commit."""
import hashlib
import json
import os
import pathlib
import stat
import subprocess

ROOT = pathlib.Path.cwd()
OUT = pathlib.Path(__file__).resolve().parent
HEAD = 'ad62493186576144f9fa1568babad012bc9ad8ca'

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

assert git('rev-parse','HEAD').decode().strip() == HEAD
tracked, expected_index, submodules = [], [], []
for row in git('ls-tree','-r','-z',HEAD).split(b'\0'):
    if not row:
        continue
    meta, filename = row.split(b'\t',1)
    mode, kind, oid = meta.decode().split()
    path = os.fsdecode(filename)
    expected_index.append((mode,oid,'0',path))
    if kind == 'commit':
        submodules.append({'path':path,'gitlink':oid})
        continue
    full = ROOT/path
    st = full.lstat()
    if mode == '120000':
        assert stat.S_ISLNK(st.st_mode),path
        data = os.fsencode(os.readlink(full))
    else:
        assert stat.S_ISREG(st.st_mode),path
        assert bool(st.st_mode & 0o111) == (mode == '100755'),path
        data = full.read_bytes()
    got = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got == oid,(path,oid,got)
    tracked.append({'path':path,'mode':mode,'blob':got})
index=[]
for row in git('ls-files','--stage','-z').split(b'\0'):
    if row:
        meta,path=row.split(b'\t',1)
        mode,oid,stage=meta.decode().split()
        index.append((mode,oid,stage,os.fsdecode(path)))
assert sorted(index)==sorted(expected_index)
status=git('status','--porcelain=v1').decode()
assert status == '',status
substatus=git('submodule','status').decode()
assert substatus == (OUT/'receipts/initial-submodules.txt').read_text()
for line in substatus.splitlines():
    assert line.startswith('-'),line
    path=line.split()[1]
    full=ROOT/path
    assert not full.exists() or full.is_dir() and not list(full.iterdir()),path
result={'head':HEAD,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),
        'tracked_blobs_verified_raw':len(tracked),'index_entries_match_head':len(index),
        'status':status,'submodules_unchanged_uninitialized':submodules,
        'submodule_status':substatus,
        'diff_check_exit':subprocess.run(['git','diff','--check',
            'b17580b91deb11f3441dfc5d7f9fafe539d929b8',HEAD]).returncode}
(OUT/'receipts/final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'receipts/tracked-blob-verification.json').write_text(json.dumps(tracked,indent=2)+'\n')
print(json.dumps(result,indent=2))
