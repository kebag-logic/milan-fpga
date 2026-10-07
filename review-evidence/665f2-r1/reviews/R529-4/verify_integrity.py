#!/usr/bin/env python3
"""Verify HEAD, every tracked blob/mode/index entry, and required gitlinks."""
import argparse,subprocess,hashlib,json,os,stat
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r=a.root.resolve()
def git(*args,cwd=r):return subprocess.check_output(['git',*args],cwd=cwd)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert head=='5968967e19411428b71dde5c4712d4a8fa528cfb';assert tree=='df2c47e21f7c068b245236ab477b5c6313036538'
index=git('ls-files','--stage','-z');expected={}
for row in git('ls-tree','-r','-z','HEAD').split(b'\0'):
 if row:
  meta,n=row.split(b'\t');mode,kind,oid=meta.split();expected[n]=(mode,oid)
bad=[];count=0;pins={}
for row in index.split(b'\0'):
 if not row:continue
 meta,n=row.split(b'\t');mode,oid,stage=meta.split();path=r/os.fsdecode(n)
 if stage!=b'0' or expected.pop(n,None)!=(mode,oid):bad.append(os.fsdecode(n)+': index')
 if mode==b'160000':
  if os.fsdecode(n) in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
   top=git('rev-parse','--show-toplevel',cwd=path).decode().strip();actual=git('rev-parse','HEAD',cwd=path).decode().strip();status=git('status','--porcelain',cwd=path).decode()
   assert Path(top)==path and actual==oid.decode() and not status
   subindex=git('ls-files','--stage','-z',cwd=path);subexpected={}
   for subrow in git('ls-tree','-r','-z','HEAD',cwd=path).split(b'\0'):
    if subrow:
     sm,sn=subrow.split(b'\t');smod,skind,soid=sm.split();subexpected[sn]=(smod,soid)
   subcount=0
   for subrow in subindex.split(b'\0'):
    if not subrow:continue
    sm,sn=subrow.split(b'\t');smod,soid,sstage=sm.split();sp=path/os.fsdecode(sn)
    assert sstage==b'0' and subexpected.pop(sn,None)==(smod,soid)
    if smod==b'160000':continue
    sd=os.readlink(sp).encode() if smod==b'120000' else sp.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(sd)).encode()+b'\0'+sd).hexdigest()==soid.decode()
    assert smod==b'120000' or bool(sp.stat().st_mode&stat.S_IXUSR)==(smod==b'100755')
    subcount+=1
   assert not subexpected
   pins[os.fsdecode(n)]={'expected':oid.decode(),'actual':actual,'clean':not status,'tracked_blobs_verified':subcount,'index_sha256':hashlib.sha256(subindex).hexdigest()}
  else:pins[os.fsdecode(n)]={'expected':oid.decode(),'initialized':False}
  continue
 data=os.readlink(path).encode() if mode==b'120000' else path.read_bytes()
 h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if h!=oid.decode():bad.append(os.fsdecode(n)+': bytes')
 if mode!=b'120000' and bool(path.stat().st_mode&stat.S_IXUSR)!=(mode==b'100755'):bad.append(os.fsdecode(n)+': mode')
 count+=1
assert not expected and not bad
status=git('status','--porcelain').decode();assert not status,status
receipt={'head':head,'tree':tree,'tracked_blobs_verified':count,'mismatches':bad,'index_sha256':hashlib.sha256(index).hexdigest(),'status':status,'submodules':pins}
a.out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
