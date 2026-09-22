import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]); dest=Path(sys.argv[2])
def git(*args):
 return subprocess.check_output(["rtk","proxy","git","-C",str(repo),*args])
entries=[]; failures=[]
for raw in git("ls-files","--stage","-z").split(b"\0"):
 if not raw: continue
 meta,name=raw.split(b"\t",1); mode,oid,stage=meta.decode().split(); path=os.fsdecode(name); f=repo/path
 record=dict(path=path,mode=mode,oid=oid,stage=stage)
 if mode=="160000":
  record["contents"]=sorted(x.name for x in f.iterdir()) if f.is_dir() else None
 else:
  st=f.lstat(); data=os.fsencode(os.readlink(f)) if stat.S_ISLNK(st.st_mode) else f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  actual_mode="120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & 0o111 else "100644")
  record.update(sha256=hashlib.sha256(data).hexdigest(),actual_blob=actual,actual_mode=actual_mode)
  if actual!=oid or actual_mode!=mode: failures.append(path)
 entries.append(record)
index=Path(git("rev-parse","--git-path","index").decode().strip())
if not index.is_absolute(): index=repo/index
head_tree=git("rev-parse","HEAD^{tree}").decode().strip()
index_tree=git("write-tree").decode().strip()
result=dict(head=git("rev-parse","HEAD").decode().strip(),tree=head_tree,index_tree=index_tree,detached=subprocess.run(["rtk","proxy","git","-C",str(repo),"symbolic-ref","-q","HEAD"],capture_output=True).returncode==1,status=git("status","--porcelain=v2","--untracked-files=all","--ignored").decode(),diff=git("diff","--raw").decode(),staged=git("diff","--cached","--raw").decode(),index_sha256=hashlib.sha256(index.read_bytes()).hexdigest(),refs=git("show-ref").decode(),entries=entries,failures=failures)
assert not failures and head_tree==index_tree and not result["status"] and not result["diff"] and not result["staged"]
dest.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("entries","refs")},indent=2));print("Tracked entries",len(entries))
