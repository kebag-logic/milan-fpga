#!/usr/bin/env python3
"""Independently verify merge resolution, retained inputs, raw blobs and index."""
import hashlib, json, os, pathlib, stat, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
def git(*args, cwd=root):
    return subprocess.check_output(["git", *args], cwd=cwd)
head="8c3e892c2b7130d88d16fb6a26136856975e1ea9"
base="cfadd767a7ad47aaee68de655e1066cc000fb8a0"
prior="2cf985f3206dd519d80142fd2479afe24c3051f6"
assert git("rev-parse","HEAD").decode().strip()==head
assert git("rev-parse","HEAD^{tree}").decode().strip()=="04f38ab729f09b4f1185f7f91416995868308ff8"
assert git("show","-s","--format=%P",head).decode().split()==[prior,base]
merge=subprocess.run(["git","merge-tree","--write-tree",prior,base],cwd=root,capture_output=True)
assert merge.returncode==1
plain=merge.stdout.splitlines()[0].decode()
changed=git("diff","--name-only",plain,head).decode().splitlines()
assert changed==["docs/diagrams/PNG_MANIFEST.json","docs/diagrams/submodule_boundaries.drawio","docs/diagrams/submodule_boundaries.png"],changed
print("plain_merge_tree",plain)
print("resolved_paths",json.dumps(changed))
print("boundary_svg_equals_plain_merge",git("rev-parse",plain+":docs/diagrams/submodule_boundaries.svg")==git("rev-parse",head+":docs/diagrams/submodule_boundaries.svg"))
for suffix in ("drawio","svg","png"):
    name="docs/diagrams/timesync_chain."+suffix
    assert git("rev-parse",prior+":"+name)==git("rev-parse",head+":"+name)
print("timesync_chain_all_three_prior_blobs_retained",True)
manifest=lambda ref:json.loads(git("show",ref+":docs/diagrams/PNG_MANIFEST.json"))
m=manifest(head); old=manifest(prior); dev=manifest(base)
assert m["artifacts"]["docs/diagrams/timesync_chain.png"]==old["artifacts"]["docs/diagrams/timesync_chain.png"]
for key in m["artifacts"]:
    if key not in ("docs/diagrams/timesync_chain.png","docs/diagrams/submodule_boundaries.png"):
        assert m["artifacts"][key]==dev["artifacts"][key]
print("manifest_timesync_retained_and_other_entries_equal_dev",True)
print("manifest_boundary_entry",json.dumps(m["artifacts"]["docs/diagrams/submodule_boundaries.png"],sort_keys=True))
retained=["gptp-processor","tb/verilator/gptp_plane","tb/verilator/milan_dp","tb/verilator/milan_dp_gm_steps","scripts/suite_shards.py","scripts/check_nvm_capture.py","tb/verilator/nvm_capture_cpu"]
assert not git("diff","--raw",prior,head,"--",*retained)
print("prior_input_paths_retained",json.dumps(retained))

def verify(cwd, ref):
    entries=[]; count=0; links=[]
    for record in git("ls-tree","-rz",ref,cwd=cwd).split(b"\0"):
        if not record:continue
        meta,path=record.split(b"\t",1)
        mode,kind,oid=meta.split()
        entries.append((mode,oid,path))
        disk=cwd/os.fsdecode(path)
        if kind==b"commit":
            links.append((os.fsdecode(path),oid.decode()))
            continue
        st=disk.lstat()
        if mode==b"120000":
            assert stat.S_ISLNK(st.st_mode),(path,"kind")
            data=os.fsencode(os.readlink(disk))
        else:
            assert stat.S_ISREG(st.st_mode),(path,"kind")
            assert bool(st.st_mode&0o111)==(mode==b"100755"),(path,"mode")
            data=disk.read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual==oid.decode(),(path,"raw blob differs")
        count+=1
    index=[]
    for row in git("ls-files","--stage","-z",cwd=cwd).split(b"\0"):
        if not row:continue
        meta,path=row.split(b"\t",1); mode,oid,stage=meta.split()
        assert stage==b"0",(path,"index conflict")
        index.append((mode,oid,path))
    assert sorted(index)==sorted(entries),"index differs from head"
    print("verified",str(cwd.relative_to(root)) or ".",ref,"blobs",count,"index_and_modes",True)
    return links
links=verify(root,head)
for name,pin in links:
    print("gitlink",name,pin)
    directory=root/name
    if (directory/".git").exists():
        assert pathlib.Path(git("rev-parse","--show-toplevel",cwd=directory).decode().strip())==directory
        assert git("rev-parse","HEAD",cwd=directory).decode().strip()==pin
        assert git("rev-parse","--show-superproject-working-tree",cwd=directory).decode().strip()==str(root)
        verify(directory,pin)
    else:
        print("uninitialized",name,"gitlink_verified_only")
assert dict(links)["gptp-processor"]=="7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9"
assert dict(links)["third_party/lwSRP"]=="08ee86e812a0eb5e1dc6cd61b494d8baf3491348"
print("PASS raw tracked blobs, modes, index and required gitlinks")
