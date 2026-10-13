import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
repo,packet=map(lambda s:Path(s).resolve(),sys.argv[1:3])
head="651ccb5aea1bc4d99f356503c188947d39e0c9e4";tree="efe717466398cf59ad71dc436feb74c6d1fe9c9d"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=env)
def check(root,revision):
 assert git(root,"rev-parse","HEAD").decode().strip()==revision
 records=[r for r in git(root,"ls-tree","-rz",revision).split(b"\0") if r]
 index={};links={};failures=[];count=0
 for record in records:
  meta,name=record.split(b"\t",1);mode,kind,oid=meta.split();index[name]=(mode,oid)
  path=root/os.fsdecode(name)
  if mode==b"160000":links[os.fsdecode(name)]=oid.decode();continue
  st=path.lstat();actual_mode=b"120000" if stat.S_ISLNK(st.st_mode) else b"100755" if st.st_mode&0o111 else b"100644"
  data=os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
  blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
  if actual_mode!=mode or blob!=oid:failures.append(os.fsdecode(name))
  count+=1
 actual_index={}
 for record in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not record:continue
  meta,name=record.split(b"\t",1);mode,oid,stage=meta.split();assert stage==b"0",name
  actual_index[name]=(mode,oid)
 assert actual_index==index,"index/tree mismatch"
 assert not failures,failures
 return {"revision":revision,"tree":git(root,"rev-parse",revision+"^{tree}").decode().strip(),"blob_bytes_and_modes_verified":count,"index_equals_tree":True,"gitlinks":links,"untracked":git(root,"ls-files","--others","--exclude-standard","-z").decode().split("\0")[:-1]}
result={"superproject":check(repo,head),"submodules":{}}
assert result["superproject"]["tree"]==tree
for sub,pin in result["superproject"]["gitlinks"].items():
 if sub=="external":continue
 assert (repo/sub/".git").is_file(),sub
 result["submodules"][sub]=check(repo/sub,pin)
result["uninitialized_unused_gitlink"]="external"
(packet/"receipts/final-tree-verification.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
