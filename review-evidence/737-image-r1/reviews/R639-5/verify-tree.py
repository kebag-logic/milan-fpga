import pathlib,sys,subprocess,json,hashlib,os,stat
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent/'final-tree.json'
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args])
def verify(path,expected=None):
 head=git(path,'rev-parse','HEAD').decode().strip();tree=git(path,'rev-parse','HEAD^{tree}').decode().strip()
 assert expected is None or head==expected,(str(path),head,expected)
 entries={};index={};mismatches=[];children=[]
 for row in git(path,'ls-tree','-r','-z','HEAD').split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split();entries[name]=(mode,oid)
 for row in git(path,'ls-files','--stage','-z').split(b'\0'):
  if not row:continue
  meta,name=row.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';index[name]=(mode,oid)
 assert entries==index,'Index differs from committed tree'
 blobs=0
 for name,(mode,oid) in entries.items():
  f=path/os.fsdecode(name)
  if mode=='160000':
   initialized=(f/'.git').exists()
   if os.fsdecode(name) in ('protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack'):assert initialized
   children.append({'path':os.fsdecode(name),'oid':oid,'verification':verify(f,oid) if initialized else 'uninitialized optional gitlink; index identity verified'});continue
  try:
   st=f.lstat();data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   actualmode='120000' if stat.S_ISLNK(st.st_mode) else '100755' if st.st_mode&0o111 else '100644'
   if actual!=oid or actualmode!=mode:mismatches.append(os.fsdecode(name))
   blobs+=1
  except OSError:mismatches.append(os.fsdecode(name))
 assert not mismatches,mismatches
 return {'head':head,'tree':tree,'tracked_blobs':blobs,'bytes_modes_index_match':True,'gitlinks':children}
r=verify(root,'4391f353690972f4844cb641b1e77fa94f38cdf4')
r['workflow_diff']=git(root,'diff','--name-only','fa7347fc59173f90e4feec2df207692e6e6e72ec..HEAD','--','.github/workflows').decode().splitlines()
r['status']=git(root,'status','--porcelain=v1','--untracked-files=normal').decode()
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
