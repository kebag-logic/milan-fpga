#!/usr/bin/env python3
"""Verify tracked bytes, executable/symlink modes, exact index and populated gitlinks."""
import hashlib, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
head="8000520cc12ec5d107a2a67f8ba3d6134b87d2b5"
env=dict(os.environ,GIT_NO_REPLACE_OBJECTS="1")
def git(repo,*args):
    return subprocess.check_output(["git","-C",str(repo),*args],env=env)
def audit(repo,rev,label):
    records=git(repo,"ls-tree","-rz",rev).split(b"\0")
    expected=[]; links=[]; n=0
    for entry in records:
        if not entry: continue
        meta,name=entry.split(b"\t",1); mode,kind,oid=meta.split(); rel=os.fsdecode(name)
        expected.append(mode+b" "+oid+b" 0\t"+name)
        f=repo/rel
        if kind==b"commit": links.append((rel,oid.decode()));continue
        st=f.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),(label,rel,"not symlink")
            data=os.fsencode(os.readlink(f))
        else:
            assert stat.S_ISREG(st.st_mode),(label,rel,"not regular")
            assert bool(st.st_mode&0o111)==(mode==b"100755"),(label,rel,"mode")
            data=f.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),(label,rel,"blob")
        n+=1
    assert git(repo,"ls-files","--stage","-z")==b"\0".join(expected)+b"\0",(label,"index differs from tree")
    print(f"{label}: {n} tracked blobs and modes match {rev}; index matches tree")
    return links
assert git(root,"rev-parse","HEAD").decode().strip()==head
assert git(root,"rev-parse","HEAD^{tree}").decode().strip()=="fc876150e72e530d5c4122f04c3ec89700523b2a"
links=audit(root,head,"parent")
for rel,pin in links:
    if rel=="external":
        print("external: uninitialized, not a required validation dependency; gitlink "+pin)
        continue
    sub=root/rel
    assert (sub/".git").is_file(),(rel,"not registered submodule")
    assert git(sub,"rev-parse","HEAD").decode().strip()==pin,(rel,"wrong HEAD")
    audit(sub,pin,rel)
    print(rel+": gitlink "+pin)
print("PASS: exact tracked bytes, modes, index and required submodule pins")
