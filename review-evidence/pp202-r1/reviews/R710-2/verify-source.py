#!/usr/bin/env python3
"""Check every tracked blob/mode and index, and enumerate gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='ebb1f0010bde76c38cc5270a6366ee9e3157ec54'
assert tree=='ce4931d11f3730d05e6ff8934ec96ddc2366578f'
checked=0;gitlinks=[]
for row in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not row: continue
    info,path=row.split(b'\t',1); mode,kind,oid=info.decode().split();name=path.decode()
    if kind=='commit':gitlinks.append({'path':name,'sha':oid});continue
    f=root/name;b=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert actual==oid,(name,'blob')
    if mode!='120000': assert bool(f.stat().st_mode & stat.S_IXUSR)==(mode=='100755'),(name,'mode')
    checked+=1
assert git('write-tree').decode().strip()==tree
status=git('status','--porcelain=v1','--untracked-files=all').decode(); assert not status,status
out={'head':head,'tree':tree,'tracked_blobs_verified':checked,'mode_check':'PASS','index_tree_matches':True,'status':status,'gitlinks':gitlinks}
(packet/'source-integrity.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
