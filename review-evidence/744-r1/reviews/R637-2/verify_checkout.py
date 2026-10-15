"""Verify tracked bytes, executable modes, index, and required submodule pins."""
import hashlib, json, os, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(cwd,*args): return subprocess.check_output(["git",*args],cwd=cwd)
def entries(cwd):
    out={}
    for row in git(cwd,"ls-tree","-rz","HEAD").split(b"\0"):
        if row:
            meta,path=row.split(b"\t",1); mode,kind,oid=meta.split()
            out[os.fsdecode(path)]=(mode.decode(),kind.decode(),oid.decode())
    return out
def verify(cwd):
    expected=entries(cwd); index={}
    for row in git(cwd,"ls-files","--stage","-z").split(b"\0"):
        if row:
            meta,path=row.split(b"\t",1); mode,oid,stage=meta.split(); assert stage==b"0"
            index[os.fsdecode(path)]=(mode.decode(),oid.decode())
    assert index=={p:(m,h) for p,(m,k,h) in expected.items()},"index differs from HEAD"
    count=0
    for name,(mode,kind,oid) in expected.items():
        if kind!="blob": continue
        path=cwd/name
        if mode=="120000":
            assert path.is_symlink(),name; data=os.fsencode(os.readlink(path))
        else:
            assert path.is_file() and not path.is_symlink(),name
            actual="100755" if path.stat().st_mode & 0o111 else "100644"
            assert actual==mode,(name,actual,mode)
            data=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid,(name,actual,oid)
        count+=1
    return count,expected
count,top=verify(root)
head=git(root,"rev-parse","HEAD").decode().strip(); tree=git(root,"rev-parse","HEAD^{tree}").decode().strip()
assert head=="43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e"
assert tree=="9c0a8e43b66f420cd9a581460a81f62184bb05dc"
result={"head":head,"tree":tree,"tracked_blobs_verified":count,"index":"exact HEAD","submodules":{}}
for name in ["third_party/verilog-axis","protocol-processor","gptp-processor","third_party/tsn-c-stack"]:
    sub=root/name
    assert not sub.is_symlink() and (sub/".git").is_file(),name
    actual=git(sub,"rev-parse","HEAD").decode().strip()
    assert top[name]==("160000","commit",actual),name
    n,_=verify(sub)
    result["submodules"][name]={"head":actual,"tracked_blobs_verified":n,"index":"exact gitlink"}
result["result"]="PASS"
print(json.dumps(result,indent=2))
