#!/usr/bin/env python3
"""Compare tracked bytes/modes/index to HEAD, including required initialized gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args])
def audit(repo,expected=None):
    head=git(repo,'rev-parse','HEAD').decode().strip();tree=git(repo,'rev-parse','HEAD^{tree}').decode().strip()
    if expected:assert head==expected
    entries=[];links=[];errors=[];expected_index=[]
    for raw in git(repo,'ls-tree','-r','-z','HEAD').split(b'\0'):
        if not raw:continue
        info,name=raw.split(b'\t',1);mode,kind,oid=info.split();path=repo/os.fsdecode(name)
        expected_index.append(mode+b' '+oid+b' 0\t'+name)
        if mode==b'160000':links.append((os.fsdecode(name),oid.decode()));continue
        actual_mode=path.lstat().st_mode
        if mode==b'120000':
            assert stat.S_ISLNK(actual_mode);data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(actual_mode)
            assert bool(actual_mode&0o111)==(mode==b'100755'),str(path)
            data=path.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid.decode(),str(path)
        entries.append({'path':os.fsdecode(name),'mode':mode.decode(),'blob':actual})
    actual_index=[x for x in git(repo,'ls-files','--stage','-z').split(b'\0') if x]
    assert expected_index==actual_index,'index differs from HEAD'
    flags=git(repo,'ls-files','-v','-z').split(b'\0')
    assert all(not f or f[:1]==b'H' for f in flags),'nonordinary index flags'
    assert not git(repo,'status','--porcelain','--untracked-files=all'),'dirty or untracked files'
    return {'head':head,'tree':tree,'tracked_blobs_checked':len(entries),'gitlinks':dict(links),'index_matches':True,'bytes_and_modes_match':True},links
head='edeef61c5a0cc6c18caa61db4019a8e378baf366'
parent,links=audit(root,head);assert parent['tree']=='164108f28665ce5ad1a24f350bf28b056100cb56'
sub={}
for path,oid in links:
    if path=='external':continue
    assert (root/path/'.git').is_file(),path
    sub[path]=audit(root/path,oid)[0]
unchanged=['hdl','tb','sw/mailbox','docs/reference/MAILBOX_CONTRACT.md','sw/firmware/ctrl/mbx/mbx_contract.h']
assert not git(root,'diff','d8b355fe..HEAD','--',*unchanged),'unexpected RTL or contract diff'
print(json.dumps({'parent':parent,'required_submodules':sub,'unused_external':'not initialized','rtl_and_mailbox_equal_source_base':True},indent=2))
