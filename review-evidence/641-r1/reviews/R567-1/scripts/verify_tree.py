#!/usr/bin/env python3
"""Verify tracked bytes, modes and index directly against immutable Git trees."""
import hashlib, json, os, pathlib, stat, subprocess
root=pathlib.Path.cwd()
head='759d1d248fad095ab07bfcc480a0828117501f39'
required=('protocol-processor','gptp-processor','third_party/verilog-axis')
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(directory,*args):
    return subprocess.check_output(['git','-C',str(directory),*args],env=env)
def verify(directory,revision):
    assert git(directory,'rev-parse','HEAD').decode().strip()==revision
    entries={}
    for row in git(directory,'ls-tree','-rz','--full-tree',revision).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1); mode,kind,oid=meta.split()
        entries[name]=(mode,oid)
        if kind==b'commit':continue
        path=directory/os.fsdecode(name); status=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(status.st_mode),str(path)
            blob=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(status.st_mode),str(path)
            actual_mode=b'100755' if status.st_mode & stat.S_IXUSR else b'100644'
            assert actual_mode==mode,(str(path),actual_mode,mode)
            blob=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest().encode()
        assert actual==oid,('blob mismatch',str(path))
    index={}
    for row in git(directory,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1); mode,oid,stage=meta.split()
        assert stage==b'0',('unmerged',name)
        assert name not in index
        index[name]=(mode,oid)
    assert index==entries,'index differs from tree'
    return entries
entries=verify(root,head)
rows=[dict(repository='review clone',head=head,tree=git(root,'rev-parse','HEAD^{tree}').decode().strip(),tracked_entries=len(entries),bytes_modes_index='MATCH')]
for name in required:
    mode,oid=entries[name.encode()]; assert mode==b'160000'
    directory=root/name
    assert (directory/'.git').is_file(),'required checkout is not a registered submodule'
    revision=oid.decode(); checked=verify(directory,revision)
    superproject=git(directory,'rev-parse','--show-superproject-working-tree').decode().strip()
    assert pathlib.Path(superproject).resolve()==root.resolve()
    rows.append(dict(repository=name,head=revision,tracked_entries=len(checked),bytes_modes_index='MATCH'))
print(json.dumps(rows,indent=2))
