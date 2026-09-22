import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(__file__).parent
label = sys.argv[1]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args):
    return subprocess.check_output(["rtk", "proxy", "git", *args], env=env)


head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
raw_index = git("ls-files", "--stage", "-z")
raw_tree = git("ls-tree", "-r", "-z", "HEAD")
index = {}
for entry in raw_index.split(b"\0"):
    if not entry:
        continue
    meta, name = entry.split(b"\t", 1)
    mode, oid, stage = meta.decode().split()
    index.setdefault(os.fsdecode(name), []).append(dict(mode=mode, oid=oid, stage=stage))
entries = []
objects = root / "source-bytes"
objects.mkdir(exist_ok=True)
for entry in raw_tree.split(b"\0"):
    if not entry:
        continue
    meta, name = entry.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    name = os.fsdecode(name)
    p = Path(name)
    for ancestor in p.parents:
        assert not ancestor.is_symlink(), ancestor
    st = p.lstat()
    actual_kind = "symlink" if stat.S_ISLNK(st.st_mode) else "file" if stat.S_ISREG(st.st_mode) else "directory"
    record = dict(path=name, head_mode=mode, head_kind=kind, head_oid=oid,
                  index=index.get(name, []), filesystem_kind=actual_kind,
                  filesystem_mode=oct(st.st_mode), filesystem_permissions=oct(stat.S_IMODE(st.st_mode)))
    if kind == "blob":
        data = os.fsencode(os.readlink(p)) if actual_kind == "symlink" else p.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        disk_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        (objects / sha256).write_bytes(data)
        record.update(size=len(data), sha256=sha256, filesystem_git_blob=disk_blob,
                      matches_head_bytes=disk_blob == oid,
                      matches_head_kind_mode=(actual_kind == "symlink" if mode == "120000" else
                          actual_kind == "file" and bool(st.st_mode & 0o111) == (mode == "100755")))
    entries.append(record)
result = dict(label=label, cwd=str(Path.cwd()), head=head, tree=tree,
              branch=git("branch", "--show-current").decode().strip(),
              status=git("status", "--porcelain=v2", "--branch").decode(),
              dependency_pins=[e for e in entries if e["head_kind"] == "commit"],
              entries=entries)
out = root / ("source-manifest-" + label + ".json")
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + "\n")
(root / ("index-" + label + ".raw")).write_bytes(raw_index)
(root / ("tree-" + label + ".raw")).write_bytes(raw_tree)
(root / ("index-flags-" + label + ".txt")).write_bytes(git("ls-files", "-v"))
print(json.dumps({k: v for k, v in result.items() if k != "entries"}, indent=2))
print("Tracked files:", len(entries))
print("Head byte differences:", [e["path"] for e in entries if e.get("matches_head_bytes") is False])
assert all(e.get("matches_head_kind_mode", True) for e in entries)
assert all(e["index"] == [dict(mode=e["head_mode"], oid=e["head_oid"], stage="0")] for e in entries)
