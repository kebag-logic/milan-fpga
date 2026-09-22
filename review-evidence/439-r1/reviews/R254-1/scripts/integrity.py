import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve(); output=pathlib.Path(sys.argv[2])
HEAD='f01f237d4b48c7b1ed59c80aca51430901791624'
TREE='ff1c54c52cbb196db754ce6999c661730a3d0e94'
PINS={'protocol-processor':'424c688fa2205b934a7689a58f2aa766420f2326','gptp-processor':'c1b617435824929a790739ea8585c3fe1a328cc0','third_party/verilog-axis':'48ff7a7e2ef782cf778d47910cf85835c64b1bce'}
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0')
def git(repo,*args):
 return subprocess.check_output(['rtk','proxy','git','-C',str(repo),*args],env=env)
def audit(repo,rev):
 expected={}
 for row in git(repo,'ls-tree','-rz',rev).split(b'\0'):
  if not row: continue
  meta,name=row.split(b'\t',1); mode,kind,oid=meta.decode().split(); expected[os.fsdecode(name)]=(mode,kind,oid)
 index={}
 for row in git(repo,'ls-files','--stage','-z').split(b'\0'):
  if not row: continue
  meta,name=row.split(b'\t',1); mode,oid,stage=meta.decode().split()
  assert stage=='0'; index[os.fsdecode(name)]=(mode,oid)
 assert index=={p:(v[0],v[2]) for p,v in expected.items()}
 checked=[]
 for rel,(mode,kind,oid) in expected.items():
  path=repo/rel
  if mode=='160000':
   checked.append({'path':rel,'mode':mode,'gitlink':oid}); continue
  st=path.lstat()
  if mode=='120000': assert stat.S_ISLNK(st.st_mode); b=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(st.st_mode),rel
   assert bool(st.st_mode & 0o111)==(mode=='100755'),rel
   b=path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  assert actual==oid,(rel,actual,oid)
  checked.append({'path':rel,'mode':mode,'blob':oid,'sha256':hashlib.sha256(b).hexdigest()})
 return {'head':git(repo,'rev-parse','HEAD').decode().strip(),'tree':git(repo,'rev-parse',rev+'^{tree}').decode().strip(),'entries':checked,'status':git(repo,'status','--porcelain=v2','--untracked-files=no').decode()}
assert git(root,'rev-parse','HEAD').decode().strip()==HEAD
assert git(root,'rev-parse','HEAD^{tree}').decode().strip()==TREE
result={'root':str(root),'parent':audit(root,HEAD),'submodules':{}}
for name,pin in PINS.items():
 assert git(root,'ls-tree',HEAD,'--',name).decode().split()[2]==pin
 assert git(root/name,'rev-parse','HEAD').decode().strip()==pin
 assert (root/name/'.git').is_file(),name
 result['submodules'][name]=audit(root/name,pin)
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'head':HEAD,'tree':TREE,'parent_entries':len(result['parent']['entries']),'submodule_entries':{k:len(v['entries']) for k,v in result['submodules'].items()},'status':result['parent']['status'],'result':'PASS'}))
