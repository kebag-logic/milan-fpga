import hashlib,json,os,stat,subprocess,datetime
from pathlib import Path
OUT=Path(__file__).resolve().parent;REPO=Path('$VALIDATION_STORAGE/reviews/r237-437-r1')
HEAD='65df1df50a80cd5f540a93d8f0cfabc97da3da75';TREE='da06c8609b7a574e3df121fbcb8a1fc8f207dcb7'
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(repo,*args):return subprocess.check_output(['rtk','proxy','git','-C',str(repo),*args],env=ENV)
def inspect(repo,expected):
 head=git(repo,'rev-parse','HEAD').decode().strip();assert head==expected,(repo,head)
 tree=git(repo,'rev-parse','HEAD^{tree}').decode().strip()
 records=git(repo,'ls-tree','-rz',head).split(b'\0');blobs=[];links={}
 for record in records:
  if not record:continue
  meta,p=record.split(b'\t',1);mode,kind,oid=meta.decode().split();name=p.decode();path=repo/name
  if mode=='160000':links[name]=oid;continue
  st=path.lstat()
  if mode=='120000':assert stat.S_ISLNK(st.st_mode);data=os.readlink(path).encode()
  else:
   assert stat.S_ISREG(st.st_mode),(path,'kind');assert bool(st.st_mode&0o111)==(mode=='100755'),(path,'mode');data=path.read_bytes()
  got=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert got==oid,(path,'blob')
  blobs.append({'path':name,'mode':mode,'kind':kind,'blob':oid})
 expected_index={(x['path'],x['mode'],x['blob']) for x in blobs}|{(p,'160000',v) for p,v in links.items()}
 actual_index=set()
 for r in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if not r:continue
  meta,p=r.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';actual_index.add((p.decode(),mode,oid))
 assert expected_index==actual_index,(repo,'index')
 return {'head':head,'tree':tree,'verified_blobs_modes_kinds':len(blobs),'index_matches_committed_tree':True,'gitlinks':links,'status':git(repo,'status','--porcelain=v2','--untracked-files=all').decode()}
parent=inspect(REPO,HEAD);assert parent['tree']==TREE
sub={}
for name in ['third_party/verilog-axis','protocol-processor','gptp-processor']:
 path=REPO/name;assert path.is_dir() and not path.is_symlink();assert (path/'.git').is_file()
 sub[name]=inspect(path,parent['gitlinks'][name]);assert git(path,'rev-parse','--show-superproject-working-tree').decode().strip()==str(REPO)
assert not parent['status'];assert all(not v['status'] for v in sub.values())
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent':parent,'submodules':sub,'external':'Unused optional gitlink unchanged; not initialized or claimed as executed','result':'PASS'}
(OUT/'final-integrity.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
