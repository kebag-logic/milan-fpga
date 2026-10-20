#!/usr/bin/env python3
"""Verify HEAD, tree, tracked bytes and executable modes against the Git tree."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*args): return subprocess.check_output(['git',*args],cwd=root)
head=git('rev-parse','HEAD').decode().strip(); tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='807b673e59ebff33378b7a78d13f34b8eccd64aa'
assert tree=='9b90a6cf899ac333c7413f1219ee4bf378f7b52d'
entries=[]; links=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not row: continue
    meta,name=row.split(b'\t',1); mode,kind,oid=meta.decode().split(); path=os.fsdecode(name)
    if mode=='160000': links.append({'path':path,'commit':oid}); continue
    f=root/path
    data=os.fsencode(os.readlink(f)) if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
    assert (actual,actual_mode)==(oid,mode),(path,actual,actual_mode)
    entries.append({'path':path,'mode':mode,'blob':actual})
assert git('write-tree').decode().strip()==tree
assert not git('diff','--raw','HEAD')
base=git('show','24c7f853:hdl/top/protocol_processor_top.sv').decode()
now=(root/'hdl/top/protocol_processor_top.sv').read_text()
assert base[:base.index(');')+2]==now[:now.index(');')+2]
assert not git('diff','24c7f853','HEAD','--','docs/architecture/07_memory_maps.md','hdl/common/pp_pkg.sv')
print(json.dumps({'head':head,'tree':tree,'index_tree':tree,'tracked_files_verified':len(entries),'gitlinks':links,'top_declaration':'byte-identical to base','memory_map_document_and_common_package':'unchanged','status':git('status','--porcelain').decode(),'files':entries},indent=2))
