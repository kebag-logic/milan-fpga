#!/usr/bin/env python3
"""Verify a checkout's tracked bytes, modes, index and gitlinks against HEAD.
Usage: checkout_integrity.py <checkout> <expected-head> <expected-tree>"""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root, want_head, want_tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
git = lambda *a, cwd=root: subprocess.check_output(["git", *a], cwd=cwd, env=env)
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
index_tree = git("write-tree").decode().strip()
problems = []
blobs = gitlinks = 0
for entry in filter(None, git("ls-tree", "-rz", "HEAD").split(b"\0")):
    meta, name = entry.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    path = root / os.fsdecode(name)
    if kind == "commit":
        gitlinks += 1
        if (path / ".git").exists():
            got = git("rev-parse", "HEAD", cwd=path).decode().strip()
            if got != oid:
                problems.append(f"gitlink {name.decode()}: {got} != {oid}")
        continue
    info = path.lstat()
    if mode == "120000":
        data = os.fsencode(os.readlink(path)); ok_kind = stat.S_ISLNK(info.st_mode)
    else:
        data = path.read_bytes(); ok_kind = stat.S_ISREG(info.st_mode)
        if bool(info.st_mode & 0o111) != (mode == "100755"):
            problems.append(f"mode {name.decode()}")
    if not ok_kind:
        problems.append(f"kind {name.decode()}")
    if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != oid:
        problems.append(f"bytes {name.decode()}")
    blobs += 1
status = git("status", "--porcelain", "--ignored", "--untracked-files=all").decode()
subs = git("submodule", "status").decode()
result = {"head": head, "tree": tree, "index_tree": index_tree, "head_ok": head == want_head,
          "tree_ok": tree == want_tree == index_tree, "tracked_blobs": blobs, "gitlinks": gitlinks,
          "problems": problems, "status_porcelain_ignored": status.splitlines(),
          "submodule_status": subs.splitlines()}
print(json.dumps(result, indent=1))
sys.exit(0 if result["head_ok"] and result["tree_ok"] and not problems and not status.strip() else 1)
