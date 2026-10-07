#!/usr/bin/env python3
"""Prove every tracked byte, file mode and index entry equals the assigned tree."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("source", type=Path)
ap.add_argument("packet", type=Path)
args = ap.parse_args()
source, packet = args.source.resolve(), args.packet.resolve()
head = "c4539ff107a6a4c7d2e4a4844182b00a2bf33c82"
tree = "4378652558345d65dd87efd4f092f41f413226c8"
def git(*argv):
    return subprocess.check_output(["git", "-C", str(source), *argv])
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == tree
entries, expected_index, gitlinks = [], [], []
for line in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not line:
        continue
    meta, path_bytes = line.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    relative = os.fsdecode(path_bytes)
    path = source / relative
    expected_index.append(mode.encode() + b" " + oid.encode() + b" 0\t" + path_bytes)
    if kind == "commit":
        gitlinks.append(dict(path=relative, gitlink=oid))
        continue
    raw = os.fsencode(os.readlink(path)) if mode == "120000" else path.read_bytes()
    actual_oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    actual_stat = path.lstat().st_mode
    actual_mode = "120000" if stat.S_ISLNK(actual_stat) else ("100755" if actual_stat & 0o111 else "100644")
    assert actual_mode == mode and actual_oid == oid, relative
    entries.append(dict(path=relative, mode=mode, blob=oid, bytes=len(raw)))
index = [x for x in git("ls-files", "--stage", "-z").split(b"\0") if x]
assert sorted(index) == sorted(expected_index)
assert not git("status", "--porcelain=v1", "--untracked-files=all").strip()
assert not gitlinks, "This assigned processor tree is expected to contain no submodule gitlinks"
dependencies = json.loads((packet / "receipts/source-fetch.json").read_text())
assert dependencies["verified_gitlinks"]["gptp-processor"] == "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d"
assert dependencies["verified_gitlinks"]["third_party/verilog-axis"] == "48ff7a7e2ef782cf778d47910cf85835c64b1bce"
assert dependencies["measurement_processor_override"] == head
resource = {}
for line in Path("/proc/self/cgroup").read_text().splitlines():
    hierarchy, controllers, group = line.split(":", 2)
    if hierarchy == "0":
        for name in ["memory.max", "memory.current", "memory.peak", "memory.events"]:
            file = Path("/sys/fs/cgroup") / group.lstrip("/") / name
            if file.exists():
                resource[name] = file.read_text().strip()
if "memory.max" in resource and resource["memory.max"] != "max":
    assert int(resource["memory.max"]) <= 12 * 1024**3
if "memory.peak" in resource:
    assert int(resource["memory.peak"]) < 12 * 1024**3
result = dict(head=head, tree=tree, tracked_blobs=len(entries), index_entries=len(index),
              raw_blob_bytes_match=True, modes_match=True, index_matches_tree=True, status_empty=True,
              processor_gitlinks=gitlinks, measurement_dependencies=dependencies["verified_gitlinks"],
              measurement_processor_override=head,
              dependency_limit="Dependency pins checked from public parent metadata and fetched source blobs; no parent checkout was edited.",
              resource_observation=resource, entries=entries)
(packet / "receipts/checkout-integrity.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "entries"}, indent=2))
