#!/usr/bin/env python3
"""Read-only merge and tracked-byte audit. Run from the exact-head clone."""
import hashlib, os, pathlib, stat, subprocess
HEAD = "8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d"
TREE = "9c57147d7f2535836e260540372cac0cae7d7049"
BASE = "c6bd08c6f52632c6d33d834ce842ac3cf63f29cc"
PREV = "ce10328c3d89d81509e47836fa4a48b22ecdbc20"
def git(*args):
    return subprocess.check_output(["git", *args])
def audit(root):
    entries = git("-C", str(root), "ls-tree", "-rz", "HEAD").split(b"\0")
    n = 0
    for record in filter(None, entries):
        info, name = record.split(b"\t", 1)
        mode, kind, oid = info.decode().split()
        if kind == "commit": continue
        path = root / os.fsdecode(name)
        data = os.fsencode(os.readlink(path)) if mode == "120000" else path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, (name, "bytes", actual, oid)
        actual_mode = "120000" if path.is_symlink() else "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
        assert actual_mode == mode, (name, "mode", actual_mode, mode)
        n += 1
    assert not git("-C",str(root),"diff","--cached","--raw","HEAD")
    assert not git("-C",str(root),"ls-files","-u")
    print(f"PASS tracked blobs, modes and index: {root.name}, {n} blobs")
assert git("rev-parse","HEAD").decode().strip() == HEAD
assert git("rev-parse","HEAD^{tree}").decode().strip() == TREE
assert git("show","-s","--format=%P","HEAD").decode().strip().split() == [PREV, BASE]
print("Head", HEAD, "tree", TREE)
auto = subprocess.run(["git","merge-tree","--write-tree",PREV,BASE],capture_output=True)
assert auto.returncode == 1, auto.stdout
atree = auto.stdout.splitlines()[0].decode()
changed = git("diff","--name-only",atree,TREE).decode().splitlines()
assert changed == ["docs/ARCHITECTURE_HW_SW_SPLIT.md"], changed
path = changed[0]
a = git("show",f"{atree}:{path}").decode()
kept = []
for line in a.splitlines(keepends=True):
    if line.startswith(("<<<<<<< ", "=======", ">>>>>>> ")): continue
    kept.append(line)
assert ''.join(kept).encode() == git("show",f"{HEAD}:{path}")
print("PASS exact automatic merge except marker removal retaining both architecture sentences")
print(git("diff","--stat",BASE,HEAD).decode())
for path in ["sw/litex/ctrl_memory.py", "sw/litex/test_ctrl_memory.py", "sw/firmware/ctrl/plat/ctrl_split.ld", "sw/firmware/ctrl/plat/ctrl_split_start.S", "sw/firmware/ctrl/test/ctrl_srp_image.py", "syn/ooc/ctrl_memory_ooc.py"]:
    assert git("rev-parse",f"{PREV}:{path}") == git("rev-parse",f"{HEAD}:{path}")
    print("PASS unchanged from previous reviewed head:",path)
audit(pathlib.Path.cwd())
for path in ["protocol-processor","gptp-processor","third_party/verilog-axis","third_party/lwSRP"]:
    pin = git("rev-parse",f"HEAD:{path}").decode().strip()
    assert (pathlib.Path(path)/".git").is_file()
    assert git("-C",path,"rev-parse","HEAD").decode().strip() == pin
    audit(pathlib.Path(path))
    print("PASS required submodule gitlink",path,pin)
print("RESULT: PASS")
