#!/usr/bin/env python3
"""Verify tracked on-disk bytes, executable modes, index and gitlinks against exact HEAD."""
import hashlib,json,os,pathlib,stat,subprocess,sys
ROOT=pathlib.Path(sys.argv[1]).resolve();OUT=pathlib.Path(__file__).resolve().parent
HEAD='a8aa626e1cba30625ac764c70e1fb8fb02c69c40'
TREE='7eb73a9f7b4b00799fd9e0206bda786cf0c3c0f1'
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip()==TREE
index={}
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    meta,path=entry.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0'
    index[path]=(mode,oid)
records=[];links=[]
for entry in git('ls-tree','-r','-z','HEAD').split(b'\0'):
    if not entry:continue
    meta,rel=entry.split(b'\t',1);mode,kind,oid=meta.split()
    assert index.pop(rel)==(mode,oid)
    p=ROOT/os.fsdecode(rel)
    if kind==b'commit':links.append(dict(path=os.fsdecode(rel),oid=oid.decode()));continue
    data=os.fsencode(os.readlink(p)) if mode==b'120000' else p.read_bytes()
    observed=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert observed==oid.decode(),p
    if mode!=b'120000':assert bool(p.stat().st_mode&stat.S_IXUSR)==(mode==b'100755'),p
    records.append(dict(path=os.fsdecode(rel),mode=mode.decode(),blob=oid.decode()))
assert not index
assert not git('status','--porcelain','--untracked-files=all').strip()
assert not git('diff','bba84945..HEAD','--','hdl','tb','scripts','syn','Makefile').strip()
result=dict(head=HEAD,tree=TREE,tracked_files=len(records),index_matches=True,bytes_and_modes_match=True,status_clean=True,gitlinks=links,
            executable_inputs_identical_to_bba84945=True,files=records)
(OUT/'source-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
