#!/usr/bin/env python3
import hashlib,json,os,pathlib,stat,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path(sys.argv[1]).resolve()
head='b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad';tree='6ecc64cb8c3434106e71bbb191aebe9a0249db1e'
def git(*a):return subprocess.check_output(['git',*a],cwd=repo)
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
expected={};gitlinks={};bad=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not row:continue
 meta,rawpath=row.split(b'\t',1);mode,kind,oid=meta.decode().split();path=rawpath.decode()
 expected[path]=(mode,oid)
 if mode=='160000':
  gitlinks[path]=oid;continue
 f=repo/path
 b=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
 digest=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
 actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & stat.S_IXUSR else '100644')
 if (actualmode,digest)!=(mode,oid):bad.append(path)
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
 if not row:continue
 meta,rawpath=row.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0'
 index[rawpath.decode()]=(mode,oid)
assert index==expected
assert not bad,bad
assert git('diff','--raw','HEAD')==b''
for path,oid in gitlinks.items():
 actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo/path).decode().strip()
 assert actual==oid,(path,actual,oid)
result={'head':head,'tree':tree,'tracked_entries':len(expected),'tracked_blob_bytes_and_modes_match':not bad,'index_matches_head':index==expected,'gitlinks':gitlinks,'status_porcelain':git('status','--porcelain=v1').decode()}
(p/'receipts/final-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
