#!/usr/bin/env python3
import pathlib,subprocess,stat,os,json,sys
p=pathlib.Path(__file__).resolve().parents[1]
head='80588cdc43ca5605a1d3748d13dd8ed7f22f7000';tree='e20b82dacbc2a3299f47c8e8444537f979d17029'
for root in [pathlib.Path(sys.argv[1]).resolve(),p/'scratch/tree',p/'scratch/id-probe',p/'scratch/figure-probe']:
 def git(*args):return subprocess.check_output(['git','-C',str(root),*args])
 assert git('rev-parse','HEAD').decode().strip()==head
 assert git('rev-parse','HEAD^{tree}').decode().strip()==tree
 entries=git('ls-tree','-r','-z',head).split(b'\0'); checked=0;modes={};gitlinks=[]
 for e in entries:
  if not e:continue
  meta,name=e.split(b'\t',1);mode,kind,oid=meta.decode().split();f=root/os.fsdecode(name)
  if mode=='160000':gitlinks.append((os.fsdecode(name),oid));continue
  if mode=='120000':data=os.fsencode(os.readlink(f));actual_mode='120000'
  else:data=f.read_bytes();actual_mode='100755' if f.stat().st_mode&stat.S_IXUSR else '100644'
  got=subprocess.check_output(['git','-C',str(root),'hash-object','--stdin'],input=data).decode().strip()
  assert got==oid and actual_mode==mode,(str(f),got,oid,actual_mode,mode)
  checked+=1;modes[mode]=modes.get(mode,0)+1
 assert git('diff','--raw',head)==b''
 assert git('diff','--cached','--raw',head)==b''
 index=git('ls-files','--stage','-z')
 expected=b''.join(e.split(b'\t',1)[0].split(b' ')[0]+b' '+e.split(b'\t',1)[0].split(b' ')[2]+b' 0\t'+e.split(b'\t',1)[1]+b'\0' for e in entries if e)
 assert index==expected
 status=git('status','--porcelain=v1').decode();assert not status,status
 print(json.dumps(dict(root=str(root),head=head,tree=tree,index_equal=True,tracked_blobs_rehashed=checked,modes=modes,gitlinks=gitlinks,status=status)))
print('All reviewed tracked bytes, executable modes and index entries match exact head. No processor submodule gitlinks exist.')
