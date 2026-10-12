#!/usr/bin/env python3
"""Prove raw tracked bytes, entry kinds, modes, index, and submodule pins."""
import hashlib, json, os, pathlib, stat, subprocess
ROOT = pathlib.Path.cwd()
HEAD = "42678ae2f77fbbef056f7fb99859e0193181e6d7"
TREE = "1508b29c3603a36349665938939fa00c871cbd7e"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)
def verify(root, revision):
    entries = git(root, "ls-tree", "-rz", "--full-tree", revision).split(b"\0")
    expected_index = []
    links = {}
    count = 0
    for entry in filter(None, entries):
        meta, name = entry.split(b"\t", 1)
        mode, kind, oid = meta.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + name)
        path = root / os.fsdecode(name)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        actual_mode = path.lstat().st_mode
        if mode == b"120000":
            assert stat.S_ISLNK(actual_mode), str(path)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(actual_mode), str(path)
            assert bool(actual_mode & 0o111) == (mode == b"100755"), str(path)
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid.decode(), str(path)
        count += 1
    assert git(root, "ls-files", "--stage", "-z") == b"\0".join(expected_index) + b"\0", "index mismatch"
    print(json.dumps({"path": str(root.relative_to(ROOT)) or ".", "revision": revision, "verified_blobs": count, "gitlinks": links}))
    return links
assert git(ROOT, "rev-parse", "HEAD").decode().strip() == HEAD
assert git(ROOT, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
links = verify(ROOT, HEAD)
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/lwSRP"):
    sub = ROOT / name
    assert (sub / ".git").is_file() and not sub.is_symlink(), name
    assert git(sub, "rev-parse", "HEAD").decode().strip() == links[name], name
    assert pathlib.Path(git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()) == ROOT, name
    verify(sub, links[name])
print("PASS tracked bytes, modes, index and required gitlinks; external remains uninitialized and unused")
