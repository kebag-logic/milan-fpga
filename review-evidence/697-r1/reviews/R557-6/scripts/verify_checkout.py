#!/usr/bin/env python3
import datetime,hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve(); output=pathlib.Path(sys.argv[2]); head="6bb706e2c75c7a437d9a0b2e44eb9ebb6d7f54d5"; tree="74f57eca0b0f93e6ed8681c9385635914c25701c"
def git(*args):return subprocess.check_output(["git","-C",str(root),*args])
assert git("rev-parse","HEAD").decode().strip()==head and git("rev-parse","HEAD^{tree}").decode().strip()==tree
assert git("write-tree").decode().strip()==tree
rows=[]; links=[]
for entry in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not entry:continue
 metadata,name=entry.split(b"\t",1); mode,kind,oid=metadata.decode().split(); rel=name.decode(); path=root/rel
 if mode=="160000":links.append({"path":rel,"gitlink":oid});continue
 data=os.readlink(path).encode() if mode=="120000" else path.read_bytes(); calculated=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest(); actual="120000" if path.is_symlink() else ("100755" if path.stat().st_mode & stat.S_IXUSR else "100644")
 assert calculated==oid and actual==mode,rel
 rows.append({"path":rel,"blob":oid,"mode":mode,"bytes_match":True,"mode_matches":True})
base_links=[x.decode() for x in git("ls-tree","-r","ae982af85ec97286bd35b39403926d8f0eaec81d").splitlines() if x.startswith(b"160000")]
assert not links and not base_links
status=git("status","--porcelain=v1","--untracked-files=all").decode(); ignored=git("ls-files","--others","--ignored","--exclude-standard").decode(); assert not status and not ignored
result={"verified_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":head,"tree":tree,"index_tree":tree,"tracked_files":len(rows),"blobs_and_modes_match":True,"status":status,"ignored":ignored,"base_gitlinks":base_links,"head_gitlinks":links,"files":rows}
output.write_text(json.dumps(result,indent=2)+"\n"); print("exact head/tree/index verified;",len(rows),"tracked files have exact blob bytes and modes; no untracked/ignored files; no required gitlinks at base/head")
