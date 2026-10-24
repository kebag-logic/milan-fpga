#!/usr/bin/env python3
"""Read-only source identity and semantic-delta checks; generated files stay in scratch."""
import hashlib,json,os,pathlib,re,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
scratch=packet/'scratch'/'rom';scratch.mkdir(parents=True,exist_ok=True)
head='33d3010cea8e053b1d2e83bcd9fa02f3f57d3f33'
base='93fb0b2d736b36588ea7321e25fba2f8819ea41f'
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='1279c09f5b690c5e94969036baa57ccfa99eccf8'
entries=git('ls-files','--stage','-z').split(b'\0')
tracked=[];links=[]
for entry in entries:
 if not entry:continue
 info,name=entry.split(b'\t');mode,blob,stage=info.decode().split();name=os.fsdecode(name)
 assert stage=='0'
 if mode=='160000':links.append([name,blob]);continue
 p=root/name
 data=os.fsencode(os.readlink(p)) if mode=='120000' else p.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert actual==blob,(name,'blob mismatch')
 if mode!='120000':assert bool(p.stat().st_mode&0o111)==(mode=='100755'),(name,'mode mismatch')
 tracked.append([mode,blob,name])
assert not git('diff','--cached',head)
assert not git('diff',head)
svs=git('diff','--name-only',base,head,'--','hdl').decode().splitlines()
code=[p for p in svs if p.endswith('.sv')]
assert code==['hdl/aecp/KL_aecp_engine.sv'],code
def strip(s):return re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',s,flags=re.S))
old=strip(git('show',base+':'+code[0]).decode());new=strip(git('show',head+':'+code[0]).decode())
needle="elseif(cfg_ix_r!=DT_AVB_INTERFACE_C)beginupc_r<=UPC_NOTIMPL_C;echo_r<=1'b1;endelsebeginupc_r<=UPC_GAVB_C;"
assert old.count(needle)==1
assert old.replace(needle,needle.replace('UPC_NOTIMPL_C','UPC_NSUPPE_C'))==new
roms=[]
for rev in (base,head):
 dest=scratch/rev;dest.mkdir(exist_ok=True)
 prefix='hdl/aecp/ucode/'
 for name in git('ls-tree','-r','--name-only',rev,'--',prefix).decode().splitlines():
  p=dest/pathlib.Path(name).relative_to(prefix);p.parent.mkdir(parents=True,exist_ok=True)
  p.write_bytes(git('show',rev+':'+name))
 subprocess.run([sys.executable,'-B',str(dest/'gen_ucode.py'),'-o',str(dest/'ucode.hex')],check=True,cwd=dest)
 data=(dest/'ucode.hex').read_bytes()
 roms.append({'revision':rev,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
assert roms[0]['sha256']==roms[1]['sha256']
result={'head':head,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'tracked_files_verified':len(tracked),'gitlinks':links,'index_and_worktree_match_head':True,'sole_synthesized_change':'GET_AVB_INFO wrong-type UPC_NOTIMPL_C -> UPC_NSUPPE_C; echo_r unchanged','roms':roms,'status':git('status','--porcelain=v1').decode()}
(packet/'source-identity.json').write_text(json.dumps(result,indent=2)+'\n')
(packet/'tracked-blobs.txt').write_text(''.join(' '.join(x)+'\n' for x in tracked))
print(json.dumps(result,indent=2))
