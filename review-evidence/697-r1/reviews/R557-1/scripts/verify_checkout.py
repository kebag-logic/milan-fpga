#!/usr/bin/env python3
"""Verify every tracked byte, mode, index entry, and gitlink against exact HEAD."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
a = p.parse_args()
root = a.repository.resolve()
def git(*args):
    return subprocess.check_output(["git", *args], cwd=root)
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
assert head == "b9b9c20a9a44650e176db0c72ad7c752bee20dc4"
assert tree == "f0706be728e592ba936d0cd3556f131d98782970"
entries = {}
gitlinks = []
for record in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not record: continue
    meta, name = record.split(b"\t",1)
    mode, kind, oid = meta.decode().split()
    name = name.decode()
    if kind == "commit":
        gitlinks.append({"path": name, "oid": oid})
    entries[name] = (mode, oid)
index = {}
for record in git("ls-files", "-sz").split(b"\0"):
    if not record: continue
    meta,name = record.split(b"\t",1)
    mode,oid,stage = meta.decode().split()
    assert stage == "0"
    index[name.decode()] = (mode,oid)
assert index == entries
files=[]
for name,(mode,oid) in entries.items():
    if mode == "160000": continue
    path = root/name
    data = path.read_bytes()
    actual = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    actual_mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
    assert actual == oid and actual_mode == mode, name
    files.append({"path":name,"mode":mode,"blob":oid})
status=git("status","--porcelain=v1","--untracked-files=all").decode()
assert status == "", status
print(json.dumps({"head":head,"tree":tree,"tracked_files":len(files),"index_matches_head":True,"worktree_bytes_and_modes_match_head":True,"gitlinks":gitlinks,"clean_status":True,"files":files},indent=2))
