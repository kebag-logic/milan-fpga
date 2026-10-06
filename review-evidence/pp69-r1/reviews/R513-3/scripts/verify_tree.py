#!/usr/bin/env python3
"""Verify tracked bytes, executable modes, index and all submodule gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
src=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
head="669ded57b1fabc2bbf274b8ad05493c7593e0a0a";tree="4bce83358cf24f551909ab46aeb19c5f93787106"
def git(*a):return subprocess.check_output(["git","-C",str(src),*a])
assert git("rev-parse","--show-toplevel").decode().strip()==str(src)
assert subprocess.run(["git","-C",str(src),"symbolic-ref","-q","HEAD"],capture_output=True).returncode==1
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()==tree
assert git("write-tree").decode().strip()==tree
index={}
for record in git("ls-files","--stage","-z").split(b"\0"):
 if not record:continue
 fields,name=record.split(b"\t",1);mode,oid,stage=fields.decode().split();assert stage=="0"
 index[os.fsdecode(name)]=(mode,oid)
rows=[];gitlinks=[]
for record in git("ls-tree","-rz",head).split(b"\0"):
 if not record:continue
 fields,name=record.split(b"\t",1);mode,kind,oid=fields.decode().split();name=os.fsdecode(name)
 assert index.pop(name)==(mode,oid),(name,"index")
 path=src/name
 if mode=="160000":
  actual=subprocess.check_output(["git","-C",str(path),"rev-parse","HEAD"],text=True).strip();assert actual==oid
  gitlinks.append({"path":name,"oid":oid});continue
 if mode=="120000":
  assert path.is_symlink();data=os.fsencode(os.readlink(path))
 else:
  st=path.lstat();assert stat.S_ISREG(st.st_mode)
  assert bool(st.st_mode&0o111)==(mode=="100755"),(name,"mode")
  data=path.read_bytes()
 actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();assert actual==oid,(name,"bytes")
 rows.append(mode+" "+oid+" "+name)
assert not index
assert not git("diff","--raw",head)
assert not git("status","--porcelain","--untracked-files=all")
assert not git("ls-files","--others","--ignored","--exclude-standard")
record={"head":head,"tree":tree,"index_tree":tree,"detached_head":True,"worktree_root":str(src),"tracked_blobs_verified":len(rows),"tracked_bytes_and_modes_exact":True,"required_gitlinks":gitlinks,"worktree_clean":True}
(out/"receipts/tree-integrity.json").write_text(json.dumps(record,indent=2)+"\n")
(out/"receipts/tracked-blobs.txt").write_text("\n".join(rows)+"\n")
print(json.dumps(record,indent=2))
