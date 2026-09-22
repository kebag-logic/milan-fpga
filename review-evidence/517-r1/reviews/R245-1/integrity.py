#!/usr/bin/env python3
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(); output=Path(sys.argv[2]); env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(repo,*args):return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def verify(repo,rev):
    raw=git(repo,"ls-tree","-rz",rev); rows=[]; expected=[]
    for rec in raw.split(b"\0"):
        if not rec:continue
        meta,path=rec.split(b"\t",1);mode,kind,oid=meta.decode().split();p=repo/os.fsdecode(path)
        expected.append(mode.encode()+b" "+oid.encode()+b" 0\t"+path)
        if kind=="commit":continue
        s=p.lstat(); assert (stat.S_ISLNK(s.st_mode) if mode=="120000" else stat.S_ISREG(s.st_mode)),str(p)
        data=os.fsencode(os.readlink(p)) if mode=="120000" else p.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid,(str(p),oid,actual)
        if mode!="120000":assert bool(s.st_mode & 0o111)==(mode=="100755"),str(p)
        rows.append({"path":os.fsdecode(path),"mode":mode,"blob":actual,"size":len(data)})
    index=git(repo,"ls-files","--stage","-z");assert sorted(index.split(b"\0")[:-1])==sorted(expected),"index differs"
    flags=git(repo,"ls-files","-v","-z").split(b"\0")
    assert all(not x or x[:1]==b"H" for x in flags),"hidden index flag"
    return {"head":git(repo,"rev-parse","HEAD").decode().strip(),"tree":git(repo,"rev-parse",rev+"^{tree}").decode().strip(),"files":rows,"index_matches":True,"flags_normal":True}
head="5874895eb817ed41c0f8be4eb427ad3315c29844";assert git(root,"rev-parse","HEAD").decode().strip()==head
result={"root":verify(root,head),"submodules":{}}
for name in ("third_party/verilog-axis","protocol-processor","gptp-processor"):
    mode,kind,pin=git(root,"ls-tree",head,name).decode().split()[:3];assert mode=="160000" and kind=="commit"
    sub=root/name;assert not sub.is_symlink();assert git(sub,"rev-parse","HEAD").decode().strip()==pin
    assert Path(git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()).resolve()==root
    result["submodules"][name]=verify(sub,pin)
result["status"]=git(root,"status","--short").decode();output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"head":head,"tree":result["root"]["tree"],"tracked_files":len(result["root"]["files"]),"submodules":{k:{"pin":v["head"],"files":len(v["files"])} for k,v in result["submodules"].items()},"status":result["status"]},indent=2))
