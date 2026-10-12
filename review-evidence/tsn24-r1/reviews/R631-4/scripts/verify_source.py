#!/usr/bin/env python3
import argparse,hashlib,json,pathlib,stat,subprocess
p=argparse.ArgumentParser();p.add_argument("source",type=pathlib.Path);p.add_argument("packet",type=pathlib.Path);a=p.parse_args();head="f13c9c16c2b300d158f980dd7c7f071dcb84df5b";tree="591d38854105564a5d632c18e846b0dd60c2f148"
def git(*args):return subprocess.check_output(["git","-C",str(a.source),*args])
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()==tree
assert git("write-tree").decode().strip()==tree
assert subprocess.run(["git","-C",str(a.source),"symbolic-ref","-q","HEAD"],capture_output=True).returncode==1
files=[];links=[]
for record in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not record:continue
 meta,name=record.split(b"\t",1);mode,kind,blob=meta.decode().split();name=name.decode()
 if mode=="160000":links.append({"path":name,"commit":blob});continue
 f=a.source/name;data=f.read_bytes();actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest();assert actual==blob,name
 actualmode="100755" if f.stat().st_mode&stat.S_IXUSR else "100644";assert actualmode==mode,name
 files.append({"path":name,"mode":mode,"blob":blob,"sha256":hashlib.sha256(data).hexdigest()})
assert len(files)==98 and links==[]
status=git("status","--porcelain=v1","--untracked-files=all").decode();assert not status,status
receipt={"head":head,"tree":tree,"detached":True,"index_matches_tree":True,"all_tracked_bytes_and_modes_match":True,"tracked_files":len(files),"core_gitlinks":links,"status":status,"files":files}
fabric=a.packet/"scratch/fabric";fr=json.loads((a.packet/"receipts/fabric-fetch.json").read_text());assert fr["gitlink"]=="2ad2f845dd583f8310075fa2380cb60a04fd091a"
for x in fr["files"]:
 data=(fabric/x["path"]).read_bytes();assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==x["blob"],x["path"]
receipt["fabric_inputs_restored_and_verified"]=len(fr["files"]);receipt["parent_gitlink"]=fr["gitlink"]
(a.packet/"receipts/source-after.json").write_text(json.dumps(receipt,indent=2)+"\n");print("PASS: exact detached head; 98 tracked blobs/modes; exact index; no core gitlinks; 8 pinned fabric inputs restored")
