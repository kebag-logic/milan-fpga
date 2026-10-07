#!/usr/bin/env python3
"""Verify actual tracked bytes, types, modes, index, and required gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys
root=pathlib.Path(sys.argv[1]).resolve()
expected=sys.argv[2]
env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}
def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def audit(repo,pin):
    assert git(repo,"rev-parse","HEAD").decode().strip()==pin
    assert git(repo,"write-tree").strip()==git(repo,"rev-parse",pin+"^{tree}").strip(), "index tree mismatch"
    index={}
    for line in git(repo,"ls-files","--stage","-z").split(b"\0"):
        if not line:continue
        meta,name=line.split(b"\t",1);mode,oid,stage=meta.split()
        assert stage==b"0"
        index[name]=(mode,oid)
    records=[];links={}
    for line in git(repo,"ls-tree","-r","-z",pin).split(b"\0"):
        if not line:continue
        meta,name=line.split(b"\t",1);mode,kind,oid=meta.split()
        assert index.pop(name)==(mode,oid)
        file=repo/os.fsdecode(name)
        if kind==b"commit":links[os.fsdecode(name)]=oid.decode();continue
        info=file.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(info.st_mode)
            data=os.fsencode(os.readlink(file))
        else:
            assert stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & 0o111)==(mode==b"100755"), "mode mismatch: "+str(file)
            data=file.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(), "blob mismatch: "+str(file)
        records.append([os.fsdecode(name),mode.decode(),actual])
    assert not index,"extra index entries"
    return {"head":pin,"tree":git(repo,"rev-parse",pin+"^{tree}").decode().strip(),"verified_blobs":len(records),"blob_mode_census_sha256":hashlib.sha256(json.dumps(records).encode()).hexdigest(),"gitlinks":links}
result={"parent":audit(root,expected),"submodules":{}}
for name in ("third_party/verilog-axis","protocol-processor","gptp-processor"):
    path=root/name
    assert (path/".git").is_file(),"unregistered submodule"
    result["submodules"][name]=audit(path,result["parent"]["gitlinks"][name])
print(json.dumps(result,indent=2))
print("Tracked blob bytes, modes, index, and required submodule gitlinks: PASS")
