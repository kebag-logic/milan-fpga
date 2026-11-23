#!/usr/bin/env python3
"""Compare disk blobs, modes, stage-zero index and required gitlinks with the requested head."""
from pathlib import Path
import subprocess,sys,hashlib,os,stat
R=Path(sys.argv[1]).resolve(); H='8267b8951616cfd570baf690835d4b0d38f14596'
def git(r,*args):return subprocess.check_output(['git',*args],cwd=r)
def verify(r,head):
    assert git(r,'rev-parse','HEAD').decode().strip()==head
    entries={}
    for row in git(r,'ls-tree','-rz',head).split(b'\0'):
        if not row:continue
        fields,path=row.split(b'\t');mode,kind,oid=fields.decode().split();entries[path]=(mode,oid)
    index={}
    for row in git(r,'ls-files','--stage','-z').split(b'\0'):
        if not row:continue
        fields,path=row.split(b'\t');mode,oid,stage=fields.decode().split();assert stage=='0';index[path]=(mode,oid)
    assert entries==index,'index differs'
    n=0
    for raw,(mode,oid) in entries.items():
        if mode=='160000':continue
        p=r/os.fsdecode(raw);st=p.lstat()
        if mode=='120000': assert stat.S_ISLNK(st.st_mode); data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode); assert bool(st.st_mode&0o111)==(mode=='100755'),str(p)
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(); assert actual==oid,str(p);n+=1
    print(r.name,head,'PASS',n,'disk blobs/modes and exact stage-zero index')
    return entries
entries=verify(R,H)
assert git(R,'rev-parse','HEAD^{tree}').decode().strip()=='b8f11886504b95ab3f48d7553de8ef173d2a67cd'
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    mode,pin=entries[name.encode()]; assert mode=='160000'; assert (R/name/'.git').is_file();verify(R/name,pin)
print('external intentionally uninitialized, not a required simulation input')
assert not git(R,'status','--porcelain').strip()
print('Exact requested head/tree and all required submodule gitlinks preserved; clean tracked state.')
