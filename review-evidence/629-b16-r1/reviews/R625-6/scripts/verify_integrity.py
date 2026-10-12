#!/usr/bin/env python3
"""Usage: verify_integrity.py REPO AUTHOR_PACKET OUTPUT_JSON. Read bytes and modes independently of index flags."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
repo,packet,out=map(lambda s:Path(s).resolve(),sys.argv[1:])
HEAD="e91a62ee266e182a804ca1f45a0f18f715096563"
EVIDENCE="b616e7ea76e375940886f0853b24470bb8efe6ec"
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1"))
def verify(root,commit):
 entries={};blobs=0;links={}
 for rec in git(root,"ls-tree","-rz",commit).split(b"\0"):
  if not rec:continue
  info,name=rec.split(b"\t",1);mode,kind,oid=info.decode().split();name=os.fsdecode(name);entries[name]=(mode,oid)
  if mode=="160000":links[name]=oid;continue
  f=root/name;s=f.lstat()
  if mode=="120000":assert stat.S_ISLNK(s.st_mode);data=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(s.st_mode),name
   assert bool(s.st_mode&0o111)==(mode=="100755"),name
   data=f.read_bytes()
  actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
  assert actual==oid,name
  blobs+=1
 idx={}
 for rec in git(root,"ls-files","--stage","-z").split(b"\0"):
  if not rec:continue
  info,name=rec.split(b"\t",1);mode,oid,stage=info.decode().split();assert stage=="0"
  idx[os.fsdecode(name)]=(mode,oid)
 assert idx==entries,"index differs from tree"
 return dict(commit=commit,blobs_verified=blobs,index_entries=len(idx),gitlinks=links)
assert git(repo,"rev-parse","HEAD").decode().strip()==HEAD
r={"source":verify(repo,HEAD),"tree":git(repo,"rev-parse","HEAD^{tree}").decode().strip(),"required_submodules":{}}
for name in ("protocol-processor","gptp-processor","third_party/verilog-axis"):
 sub=repo/name;pin=r["source"]["gitlinks"][name]
 assert git(sub,"rev-parse","HEAD").decode().strip()==pin
 assert Path(git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==repo
 r["required_submodules"][name]=verify(sub,pin)
base="review-evidence/629-b16-r1/"
manifest=json.loads(git(repo,"show",EVIDENCE+":"+base+"MANIFEST.json"))
assert len({x["file"] for x in manifest})==len(manifest)
files=[x for x in manifest if x["file"].startswith("author-r6/")]
for x in files:
 f=packet/x["file"].removeprefix("author-r6/")
 assert hashlib.sha256(f.read_bytes()).hexdigest()==x["published_sha256"],x["file"]
 assert (x["original_sha256"]!=x["published_sha256"])==x["path_redacted"]
r["publication"]=dict(commit=EVIDENCE,manifest_entries=len(manifest),author_r6_files_verified=len(files),path_redacted=sum(x["path_redacted"] for x in files))
r["probes"]={}
for rel in ("R624-4/tools/probe_escape_forms.py","R625-4/probe_coverage.py","R625-3/scripts/probe_figure_coverage.py","R624-5/scripts/probe_row3200.py","R624-5/scripts/probe_r624_5_escapes.py","R625-5/probe_comment_separator.py"):
 blob=git(repo,"show",EVIDENCE+":"+base+"reviews/"+rel)
 local=packet/"tools/review-probes"/Path(rel).name
 assert blob==local.read_bytes(),rel
 r["probes"][rel]=hashlib.sha256(blob).hexdigest()
for name in ("rows","coverage"):
 r["publication"]["figures_"+name+"_byte_equal"]=(out.parent/f"figures-{name}.tsv").read_bytes()==(packet/f"r6/figures-{name}.tsv").read_bytes()
r["tracked_source_delta"]=git(repo,"diff","--name-status","c20c85bd",HEAD).decode().splitlines()
r["working_status"]=git(repo,"status","--porcelain=v1").decode().splitlines()
r["status"]="PASS"
out.write_text(json.dumps(r,indent=2)+"\n");print(json.dumps(r,indent=2))
