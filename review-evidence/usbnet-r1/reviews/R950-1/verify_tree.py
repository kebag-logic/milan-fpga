#!/usr/bin/env python3
"""Verify exact raw tree blobs, modes, index entries and populated gitlinks."""
import argparse,hashlib,json,os,pathlib,stat,subprocess
ap=argparse.ArgumentParser(); ap.add_argument("repo",type=pathlib.Path); a=ap.parse_args()
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1"); rows=[]; problems=[]
def git(r,*args): return subprocess.check_output(["git","-C",str(r),*args],env=env)
def check(r,rev,label):
 tree={}; links=[]
 for row in git(r,"ls-tree","-rz",rev).split(b"\0"):
  if not row: continue
  meta,name=row.split(b"\t",1); mode,kind,oid=meta.split(); tree[name]=(mode,oid)
  path=r/os.fsdecode(name)
  if kind==b"commit": links.append((name,oid)); continue
  try:
   st=path.lstat(); actual_mode=b"120000" if stat.S_ISLNK(st.st_mode) else b"100755" if st.st_mode&0o111 else b"100644"
   data=os.fsencode(os.readlink(path)) if stat.S_ISLNK(st.st_mode) else path.read_bytes()
   digest=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
   if actual_mode!=mode or digest!=oid: problems.append(label+":"+os.fsdecode(name)+" blob/mode mismatch")
  except OSError as e: problems.append(label+":"+os.fsdecode(name)+" unavailable")
 index={}
 for row in git(r,"ls-files","--stage","-z").split(b"\0"):
  if not row: continue
  meta,name=row.split(b"\t",1); mode,oid,stage=meta.split(); index[name]=(mode,oid)
  if stage!=b"0": problems.append(label+" nonzero stage")
 if index!=tree: problems.append(label+" index differs from tree")
 rows.append({"repository":label,"head":git(r,"rev-parse","HEAD").decode().strip(),"checked_revision":rev,"blobs":len(tree)-len(links),"index_matches":index==tree})
 for name,oid in links:
  path=r/os.fsdecode(name); lab=label+"/"+os.fsdecode(name)
  if not (path/".git").exists():
   rows.append({"repository":lab,"gitlink":oid.decode(),"populated":False})
   if name!=b"external": problems.append(lab+" required gitlink absent")
   continue
  actual=git(path,"rev-parse","HEAD").strip()
  if actual!=oid: problems.append(lab+" gitlink mismatch")
  check(path,oid.decode(),lab)
r=a.repo.resolve(); head="cc49123d2db1e01e80859efa10f8da43a01344ef"; check(r,head,"root")
if git(r,"rev-parse","HEAD").decode().strip()!=head: problems.append("parent HEAD changed")
print(json.dumps({"tree":git(r,"rev-parse",head+"^{tree}").decode().strip(),"checks":rows,"problems":problems,"pass":not problems},indent=2))
raise SystemExit(bool(problems))
