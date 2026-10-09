# Verify that a review clone holds the exact head: HEAD, every tracked blob's bytes and
# mode, the index against the tree, gitlinks, and an empty status.
# Usage: python3 -I verify_clone.py <clone> <commit>
import hashlib
import os
import stat
import subprocess
import sys

clone, commit = sys.argv[1], sys.argv[2]


def git(*args):
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True).stdout


problems = []
head = git("rev-parse", "HEAD").decode().strip()
if head != commit:
    problems.append(f"HEAD {head} != {commit}")
entries = files = links = 0
for line in git("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
    if not line:
        continue
    meta, path = line.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    path = path.decode()
    entries += 1
    full = os.path.join(clone, path)
    if kind == "commit":
        links += 1
        if git("ls-files", "-s", "--", path).decode().split()[1] != oid:
            problems.append(f"gitlink index {path}")
        continue
    files += 1
    st = os.lstat(full)
    if mode == "120000":
        data = os.readlink(full).encode()
        ok_mode = stat.S_ISLNK(st.st_mode)
    else:
        with open(full, "rb") as handle:
            data = handle.read()
        ok_mode = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o100) == (mode == "100755")
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if blob != oid:
        problems.append(f"bytes {path}")
    if not ok_mode:
        problems.append(f"mode {path}")
tree = git("rev-parse", f"{commit}^{{tree}}").decode().strip()
index_tree = git("write-tree").decode().strip()
if index_tree != tree:
    problems.append(f"index tree {index_tree} != {tree}")
status = git("status", "--porcelain", "--untracked-files=all").decode()
if status.strip():
    problems.append("status not empty: " + status.strip().replace("\n", "; "))
print(f"HEAD {head}; tree {tree}; {entries} entries ({files} files, {links} gitlinks); index tree {index_tree}")
print(git("submodule", "status").decode().rstrip())
print("PROBLEMS: " + "; ".join(problems) if problems else "INTEGRITY OK: bytes, modes, index, gitlinks and status exact")
sys.exit(1 if problems else 0)
