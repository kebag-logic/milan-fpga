# SPDX-License-Identifier: Apache-2.0
"""Check exact head, every tracked blob/mode/index entry, and source anchors."""
import hashlib,re,stat
from common import *
HEAD="14c8b364863be49bc222f4913830b79d23dcf173"
TREE="0d2f7e8cfb5f1e2886c7cfabde530b7cf1ed3921"
def git(*args):return subprocess.check_output(["git",*args],cwd=SOURCE)
assert git("rev-parse","HEAD").decode().strip()==HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip()==TREE
entries={};gitlinks=[];files=[]
for row in git("ls-tree","-rz","HEAD").split(b"\0"):
 if not row:continue
 meta,name=row.split(b"\t",1);mode,kind,oid=meta.decode().split();name=name.decode();entries[name]=(mode,oid)
 if mode=="160000":gitlinks.append(dict(path=name,sha=oid));continue
 path=SOURCE/name;data=path.read_bytes();actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
 actual_mode="100755" if path.stat().st_mode&stat.S_IXUSR else "100644"
 assert actual==oid,(name,"bytes");assert actual_mode==mode,(name,"mode")
 assert b"SPDX-License-Identifier: Apache-2.0" in data,(name,"license")
 files.append(dict(path=name,mode=mode,blob=oid,sha256=hashlib.sha256(data).hexdigest()))
index={}
for row in git("ls-files","--stage","-z").split(b"\0"):
 if not row:continue
 meta,name=row.split(b"\t",1);mode,oid,stage=meta.decode().split();assert stage=="0";index[name.decode()]=(mode,oid)
assert index==entries
assert not git("status","--porcelain=v1","--untracked-files=all").strip()
assert not git("diff","--check").strip()
result=dict(head=HEAD,tree=TREE,tracked_files=len(files),all_blobs_modes_and_index_match=True,gitlinks=gitlinks,submodule_status=git("submodule","status").decode(),files=files)
(PACKET/"receipts/integrity.json").write_text(json.dumps(result,indent=2)+"\n")
anchors=[]
for md in [SOURCE/"README.md",SOURCE/"CONTRIBUTING.md",*sorted((SOURCE/"doc").rglob("*.md"))]:
 for lineno,line in enumerate(md.read_text().splitlines(),1):
  for label,link,line1 in re.findall(r"\[([^\]]+)\]\(([^()#]+)#L(\d+)(?:-L\d+)?\)",line):
   path=(md.parent/link).resolve()
   if not path.exists():continue
   target=path.read_text().splitlines()[int(line1)-1]
   anchors.append(dict(page=str(md.relative_to(SOURCE)),line=lineno,label=label,target=str(path.relative_to(SOURCE))+":"+line1,text=target))
(PACKET/"receipts/source-anchors.json").write_text(json.dumps(anchors,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="files"},indent=2));print("Source anchors",len(anchors))
for x in anchors:print(x["label"],x["target"],x["text"])
