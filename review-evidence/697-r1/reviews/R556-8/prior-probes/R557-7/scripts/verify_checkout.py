#!/usr/bin/env python3
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]);head="68070cb5723682586c07a6de80a49886732b5dc2";tree="f42024aec0fddde6cf6d552e85e50109a8e6cbb4"
def git(*args):return subprocess.check_output(["git","-C",str(root),*args])
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()==tree
assert git("write-tree").decode().strip()==tree
rows=[];links=[]
for record in git("ls-tree","-rz",head).split(b"\0"):
 if not record:continue
 meta,rawpath=record.split(b"\t",1);mode,kind,oid=meta.decode().split();path=rawpath.decode();file=root/path
 if mode=="160000":links.append({"path":path,"commit":oid});continue
 data=os.readlink(file).encode() if mode=="120000" else file.read_bytes()
 blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 actual="120000" if file.is_symlink() else "100755" if file.stat().st_mode&stat.S_IXUSR else "100644"
 assert blob==oid and mode==actual,path
 rows.append({"path":path,"mode":mode,"blob":oid,"bytes_match":True,"mode_matches":True})
assert not git("diff","--raw") and not git("diff","--cached","--raw")
base_links=[r.decode() for r in git("ls-tree","-r","ae982af85ec97286bd35b39403926d8f0eaec81d").splitlines() if r.startswith(b"160000")]
result={"head":head,"tree":tree,"index_tree":tree,"tracked_entries":len(rows),"gitlinks":links,"base_gitlinks":base_links,"status_including_ignored":git("status","--porcelain=v1","--untracked-files=all","--ignored").decode(),"entries":rows}
out.write_text(json.dumps(result,indent=2)+"\n");print(len(rows),"tracked blobs and modes match; index equals exact tree; gitlinks",len(links))
