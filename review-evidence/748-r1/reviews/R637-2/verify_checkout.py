#!/usr/bin/env python3
"""Verify tracked worktree bytes, modes, index entries and required registered gitlinks."""
import hashlib, json, os, pathlib, stat, subprocess, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(__file__).resolve().parent
HEAD = "2e83841675e4e1439c413c9ca11b4a123898a60e"
TREE = "4b1bed5825eae73757cb5368c71468c7d1d67d72"
REQUIRED = ["protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack"]
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])
def entries(root):
    expected = {}
    for item in git(root, "ls-tree", "-rz", "HEAD").split(b"\0"):
        if item:
            meta, name = item.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            expected[os.fsdecode(name)] = (mode, kind, oid)
    return expected
def verify(root):
    expected = entries(root)
    index = {}
    for item in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if item:
            meta, name = item.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0", os.fsdecode(name)
            index[os.fsdecode(name)] = (mode, oid)
    assert index == {p:(v[0],v[2]) for p,v in expected.items()}, "index differs"
    count = 0
    links = {}
    for name, (mode, kind, oid) in expected.items():
        if kind == "commit":
            links[name] = oid
            continue
        path = root / name
        st = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == "100755"), name
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, name
        count += 1
    return {"head": git(root, "rev-parse", "HEAD").decode().strip(),
            "tree": git(root, "rev-parse", "HEAD^{tree}").decode().strip(),
            "verified_blobs": count, "index_matches": True, "blob_bytes_and_modes_match": True,
            "gitlinks": links}
result = {"superproject": verify(ROOT), "required_submodules": {}}
assert result["superproject"]["head"] == HEAD
assert result["superproject"]["tree"] == TREE
for name in REQUIRED:
    path = ROOT / name
    assert (path / ".git").is_file(), name
    parent = git(path, "rev-parse", "--show-superproject-working-tree").decode().strip()
    assert pathlib.Path(parent).resolve() == ROOT, name
    checked = verify(path)
    assert checked["head"] == result["superproject"]["gitlinks"][name], name
    checked["registered_submodule"] = True
    result["required_submodules"][name] = checked
result["status"] = git(ROOT, "status", "--porcelain=v1").decode()
assert not result["status"], result["status"]
(OUT / "checkout-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: exact head/tree,", result["superproject"]["verified_blobs"], "superproject blobs and modes, exact index, four registered submodules with pinned bytes; clean status")
