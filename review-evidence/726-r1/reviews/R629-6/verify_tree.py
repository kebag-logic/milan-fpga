#!/usr/bin/env python3
"""Compare raw tracked bytes, modes, index and registered submodule pins."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve()
def git(tree,*args):
    return subprocess.check_output(["git","-C",str(tree),*args],env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1"))
def verify(tree,expected):
    assert git(tree,"rev-parse","HEAD").decode().strip()==expected
    records=git(tree,"ls-tree","-rz",expected).split(b"\0")
    index=git(tree,"ls-files","--stage","-z")
    expected_index=[]; count=0; sub=[]
    for record in records:
        if not record: continue
        info,name=record.split(b"\t",1)
        mode,kind,oid=info.split()
        expected_index.append(mode+b" "+oid+b" 0\t"+name+b"\0")
        path=tree/os.fsdecode(name)
        if kind==b"commit":
            if name in [b"protocol-processor",b"gptp-processor",b"third_party/verilog-axis"]:
                assert (path/".git").is_file(),path
                sub.append(verify(path,oid.decode()))
            continue
        st=path.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),path
            data=os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode),path
            assert bool(st.st_mode&0o111)==(mode==b"100755"),path
            data=path.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),path
        count+=1
    assert index==b"".join(expected_index),str(tree)+" index differs"
    return {"tree":str(tree.relative_to(root)) or ".","head":expected,"blobs_checked":count,"index_exact":True,"submodules":sub}
print(json.dumps(verify(root,"12f00129349c889e6dbbb7de11529ab38c9d164d"),indent=2))
