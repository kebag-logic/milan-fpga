#!/usr/bin/env python3
"""Compare every tracked object, index entry, file kind/mode and required gitlink."""
import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("repo",type=Path);p.add_argument("output",type=Path);a=p.parse_args()
root=a.repo.resolve()
def git(repo,*args):
    return subprocess.check_output(["git","--no-replace-objects","-C",str(repo),*args])
def check(repo):
    tree=git(repo,"ls-tree","-rz","--full-tree","HEAD")
    entries={}
    for record in tree.split(b"\0"):
        if not record: continue
        meta,path=record.split(b"\t",1);mode,kind,oid=meta.split();entries[path]=(mode,kind,oid)
    idx=git(repo,"ls-files","--stage","-z");actual={}
    for record in idx.split(b"\0"):
        if not record: continue
        meta,path=record.split(b"\t",1);mode,oid,stage=meta.split()
        assert stage==b"0" and path not in actual, (repo,path,stage)
        actual[path]=(mode,oid)
    assert actual=={path:(m,o) for path,(m,k,o) in entries.items()}, repo
    rows=[]
    for name,(mode,kind,oid) in entries.items():
        if kind==b"commit": continue
        path=repo/os.fsdecode(name)
        parent=path.parent
        while parent!=repo:
            assert parent.is_dir() and not parent.is_symlink(),parent
            parent=parent.parent
        st=path.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),path
            data=os.fsencode(os.readlink(path))
        else:
            assert mode in (b"100644",b"100755") and stat.S_ISREG(st.st_mode),path
            assert bool(st.st_mode & 0o111)==(mode==b"100755"),path
            data=path.read_bytes()
        calculated=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert calculated==oid.decode(),path
        rows.append({"path":os.fsdecode(name),"mode":mode.decode(),"blob":calculated,"sha256":hashlib.sha256(data).hexdigest()})
    index_path=Path(os.fsdecode(git(repo,"rev-parse","--path-format=absolute","--git-path","index").strip()))
    status=git(repo,"status","--porcelain=v1","--untracked-files=no").decode()
    assert not status,(repo,status)
    return {"head":git(repo,"rev-parse","HEAD").decode().strip(),"tree":git(repo,"rev-parse","HEAD^{tree}").decode().strip(),"count":len(rows),"files":rows,"index_sha256":hashlib.sha256(index_path.read_bytes()).hexdigest(),"index_records_sha256":hashlib.sha256(idx).hexdigest(),"status":status}
result={"root":check(root),"submodules":{}}
for name in ("third_party/verilog-axis","protocol-processor","gptp-processor"):
    path=root/name
    assert path.is_dir() and not path.is_symlink(),path
    assert (path/".git").is_file() and (path/".git").read_text().startswith("gitdir:"),path
    assert Path(os.fsdecode(git(path,"rev-parse","--show-superproject-working-tree").strip())).resolve()==root,path
    pin=git(root,"ls-tree","HEAD","--",name).split()[2].decode()
    row=check(path);assert row["head"]==pin,(name,row["head"],pin)
    row["gitlink"]=pin; result["submodules"][name]=row
assert result["root"]["head"]=="4671e582cfa4bba4809b9e3a354ce5b6eb967f99"
assert result["root"]["tree"]=="afc8eadb3e9f6611dfb62347580b49dc721d25c0"
a.output.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"root":result["root"]["count"],"submodules":{k:v["count"] for k,v in result["submodules"].items()},"result":"PASS"}))
