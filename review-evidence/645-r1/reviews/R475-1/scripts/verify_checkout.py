#!/usr/bin/env python3
"""Verify raw worktree blobs, modes, index entries and required gitlinks."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
R=Path(os.environ.get("REVIEW_REPO",str(Path.cwd()))).resolve()
HEAD="4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f"
TREE="1cb3772cf102a9296b4fea2db7096315c3c76360"
def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args])
def audit(root,expected):
    assert git(root,"rev-parse","--show-toplevel").decode().strip()==str(root)
    head=git(root,"rev-parse","HEAD").decode().strip()
    assert head==expected,(str(root),head,expected)
    rows=git(root,"ls-tree","-rz","HEAD").split(b"\0")
    ix={}
    for row in git(root,"ls-files","--stage","-z").split(b"\0"):
        if not row:continue
        meta,path=row.split(b"\t",1); mode,oid,stage=meta.split()
        assert stage==b"0"
        ix[path]=(mode,oid)
    failures=[]; checked=0; links={}
    for row in rows:
        if not row:continue
        meta,name=row.split(b"\t",1); mode,kind,oid=meta.split()
        if ix.pop(name,None)!=(mode,oid): failures.append([os.fsdecode(name),"index"])
        f=root/os.fsdecode(name)
        if kind==b"commit": links[os.fsdecode(name)]=oid.decode();continue
        try:
            s=f.lstat()
            if mode==b"120000":
                if not stat.S_ISLNK(s.st_mode): raise ValueError("not symlink")
                data=os.fsencode(os.readlink(f)); actual_mode=b"120000"
            else:
                if not stat.S_ISREG(s.st_mode):raise ValueError("not regular")
                data=f.read_bytes(); actual_mode=b"100755" if s.st_mode&0o111 else b"100644"
            h=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest().encode()
            if h!=oid or actual_mode!=mode:failures.append([os.fsdecode(name),"raw blob or mode"])
            checked+=1
        except (OSError,ValueError) as e:failures.append([os.fsdecode(name),str(e)])
    failures.extend([[os.fsdecode(name),"extra index entry"] for name in ix])
    return {"head":head,"tree":git(root,"rev-parse","HEAD^{tree}").decode().strip(),"tracked_blob_modes_checked":checked,"failures":failures,"gitlinks":links,"status":git(root,"status","--porcelain=v1").decode()}
result={"root":audit(R,HEAD)}
assert result["root"]["tree"]==TREE
for name in ["protocol-processor","gptp-processor","third_party/verilog-axis"]:
    result[name]=audit((R/name).resolve(),result["root"]["gitlinks"][name])
result["external"]="Not initialized; recorded gitlink only, not a required validation input."
result["pass"]=all(not v["failures"] and not v["status"] for v in result.values() if isinstance(v,dict))
out=P/"receipts"/(sys.argv[1] if len(sys.argv)>1 else "checkout-final.json")
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["pass"] else 1)
