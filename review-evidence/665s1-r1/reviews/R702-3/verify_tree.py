#!/usr/bin/env python3
"""Verify tracked bytes, modes, index trees and required submodule gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
head='44d95625bde2c46d7070c090fc29ed0ba85ab64a'
tree='2b5b52bb8d0c1b43d8ce9ef24684d3a5374acde3'
def git(where,*args): return subprocess.check_output(['git','-C',str(where),*args],env=env).strip()
def verify(where,commit):
    assert git(where,'rev-parse','HEAD').decode()==commit
    want_tree=git(where,'rev-parse',commit+'^{tree}')
    assert git(where,'write-tree')==want_tree,'index differs from commit'
    checked=0; links={}
    for entry in git(where,'ls-tree','-rz',commit).split(b'\0'):
        if not entry: continue
        meta,name=entry.split(b'\t'); mode,kind,oid=meta.split(); name=name.decode()
        if mode==b'160000': links[name]=oid.decode();continue
        path=where/name; st=path.lstat()
        if mode==b'120000':
            assert stat.S_ISLNK(st.st_mode),name
            data=os.readlink(path).encode()
        else:
            assert stat.S_ISREG(st.st_mode),name
            assert bool(st.st_mode & 0o111)==(mode==b'100755'),name
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid.decode(),name
        checked+=1
    return {'head':commit,'tree':want_tree.decode(),'tracked_blobs_verified':checked,'gitlinks':links}
result={'main':verify(root,head),'submodules':{}}
assert result['main']['tree']==tree
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    path=root/name
    assert (path/'.git').is_file(),'registered submodule required: '+name
    result['submodules'][name]=verify(path,result['main']['gitlinks'][name])
(packet/'tree-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
