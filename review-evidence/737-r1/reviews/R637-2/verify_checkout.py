#!/usr/bin/env python3
"""Independently verify committed blob bytes, modes, index and initialized gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();head="2658a64c408bf87ae36574f36a6deeb34b2f297f"
def git(where,*args):return subprocess.check_output(["git","--no-replace-objects",*args],cwd=where)
assert git(root,"rev-parse","HEAD").decode().strip()==head
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="d78031e7fec0f8439161c59ddf105f68d4b426c8"
reports=[]
def check(directory,revision,label):
 tree={};blobs=0;links=[]
 for entry in filter(None,git(directory,"ls-tree","-rz",revision).split(b"\0")):
  metadata,name=entry.split(b"\t",1);mode,kind,oid=metadata.split();tree[name]=(mode,oid)
  path=directory/os.fsdecode(name)
  if kind==b"commit":
   initialized=(path/".git").exists()
   links.append({"path":os.fsdecode(name),"commit":oid.decode(),"initialized":initialized})
   if initialized:
    assert git(path,"rev-parse","HEAD").strip()==oid
    check(path,oid.decode(),label+"/"+os.fsdecode(name))
   else:assert not path.exists() or not any(path.iterdir())
   continue
  info=path.lstat()
  if mode==b"120000":assert stat.S_ISLNK(info.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(info.st_mode)
   assert bool(info.st_mode&0o111)==(mode==b"100755")
   data=path.read_bytes()
  assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==oid.decode(),label+"/"+os.fsdecode(name)
  blobs+=1
 index={}
 for entry in filter(None,git(directory,"ls-files","--stage","-z").split(b"\0")):
  metadata,name=entry.split(b"\t",1);mode,oid,stage=metadata.split();assert stage==b"0";index[name]=(mode,oid)
 assert index==tree,label+" index differs"
 untracked=git(directory,"ls-files","--others","--exclude-standard","-z")
 assert not untracked,(label,untracked)
 reports.append({"repository":label,"commit":revision,"verified_blobs":blobs,"index_matches_tree":True,"blob_modes_match":True,"gitlinks":links,"untracked_nonignored":0})
check(root,head,"review-checkout")
merge_dev="fa8209889411e8ca95757174c981f720dbcd95a2"
subprocess.run(["git","merge-base","--is-ancestor",merge_dev,head],cwd=root,check=True)
product=git(root,"diff","--name-only",merge_dev+".."+head,"--","hdl","sw",".gitmodules","third_party","protocol-processor","gptp-processor").decode().splitlines()
assert product==["sw/firmware/ctrl/README.md"]
print(json.dumps({"head":head,"tree":"d78031e7fec0f8439161c59ddf105f68d4b426c8","source_restoration":"No tracked source files were edited by review probes.","merged_dev_ancestor":merge_dev,"product_paths_changed_relative_to_merged_dev":product,"repositories":reports},indent=2))
