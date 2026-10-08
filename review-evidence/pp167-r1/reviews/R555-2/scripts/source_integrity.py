#!/usr/bin/env python3
import hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]); dest=pathlib.Path(sys.argv[2])
def git(*args): return subprocess.check_output(['git','-C',str(root),*args])
head=git('rev-parse','HEAD').decode().strip(); files=[]; errors=[]; links=[]
for line in git('ls-tree','-rz',head).split(b'\0'):
    if not line: continue
    meta,name=line.split(b'\t',1); mode,kind,blob=meta.decode().split(); path=os.fsdecode(name)
    if mode=='160000':
        links.append({'path':path,'expected':blob,'actual':subprocess.check_output(['git','-C',str(root/path),'rev-parse','HEAD']).decode().strip()}); continue
    f=root/path; data=os.fsencode(os.readlink(f)) if mode=='120000' else f.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_mode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode & 0o111 else '100644')
    rec={'path':path,'blob':blob,'actual_blob':actual,'mode':mode,'actual_mode':actual_mode,'sha256':hashlib.sha256(data).hexdigest()}; files.append(rec)
    if actual!=blob or mode!=actual_mode: errors.append(path)
index=git('ls-files','--stage','-z'); expected=[]
for line in git('ls-tree','-rz',head).split(b'\0'):
    if line:
        meta,name=line.split(b'\t',1); mode,kind,blob=meta.split(); expected.append(mode+b' '+blob+b' 0\t'+name+b'\0')
index_ok=index==b''.join(expected)
result={'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'index_equals_head':index_ok,'index_sha256':hashlib.sha256(index).hexdigest(),'submodule_gitlinks':links,'files':files,'errors':errors,'status':git('status','--porcelain=v2').decode()}
dest.write_text(json.dumps(result,indent=2)+'\n'); print(f'{len(files)} tracked blobs/modes checked; index={index_ok}; gitlinks={len(links)}; errors={errors}')
assert index_ok and not errors and all(x['expected']==x['actual'] for x in links)
