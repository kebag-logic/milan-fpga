#!/usr/bin/env python3
"""Verify tracked disk bytes/modes and the entire stage-zero index against the pin."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
head = "2139f3dc10161b456dfbd51d2f73a63f9164e041"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=env)
assert git("rev-parse", "HEAD").decode().strip() == head
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
assert tree == "b7d98916ed833c26c7f7d713964b16c10c36daa3"
entries = {}
blobs = []
gitlinks = []
for row in git("ls-tree", "-rz", "--full-tree", head).split(b"\0"):
    if not row:
        continue
    metadata, raw_path = row.split(b"\t", 1)
    mode, kind, oid = metadata.decode().split()
    path = raw_path.decode()
    entries[path] = (mode, oid)
    f = repo / path
    if kind == "commit":
        actual = subprocess.check_output(["git", "-C", str(f), "rev-parse", "HEAD"], env=env).decode().strip()
        assert actual == oid, path
        gitlinks.append({"path": path, "pin": oid, "actual": actual})
        continue
    assert kind == "blob", (path, kind)
    st = f.lstat()
    if mode == "120000":
        assert stat.S_ISLNK(st.st_mode), path
        data = os.readlink(f).encode()
    else:
        assert stat.S_ISREG(st.st_mode), path
        assert bool(st.st_mode & stat.S_IXUSR) == (mode == "100755"), path
        data = f.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == oid, path
    blobs.append({"path": path, "mode": mode, "blob": oid, "bytes": len(data), "verified": True})
index = {}
for row in git("ls-files", "--stage", "-z").split(b"\0"):
    if not row:
        continue
    metadata, raw_path = row.split(b"\t", 1)
    mode, oid, stage = metadata.decode().split()
    path = raw_path.decode()
    assert stage == "0" and path not in index, (path, stage)
    index[path] = (mode, oid)
assert entries == index
status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
assert status == "", status
ignored = git("ls-files", "--others", "--ignored", "--exclude-standard").decode().splitlines()
assert ignored == [], ignored
assert len(blobs) == 556
memory = {}
for line in Path("/proc/self/cgroup").read_text().splitlines():
    if line.startswith("0::"):
        cg = Path("/sys/fs/cgroup") / line[3:].lstrip("/")
        for name in ["memory.max", "memory.peak", "memory.events"]:
            if (cg / name).exists():
                memory[name] = (cg / name).read_text().strip()
result = {"head": head, "tree": tree, "tracked_blobs": len(blobs), "all_disk_bytes_and_modes_match": True, "all_index_records_match": True, "source_gitlinks": gitlinks, "status": status, "ignored_files": ignored, "memory": memory, "blobs": blobs}
(packet / "receipts/final-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "blobs"}, indent=2))
