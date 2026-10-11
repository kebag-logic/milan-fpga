#!/usr/bin/env python3
"""R602-6: prove a checkout is exactly a commit. Usage: verify_clone.py REPO COMMIT
Every tracked path of COMMIT's tree: index record (mode, blob, stage 0) equals the
tree, the file on disk hashes to the blob with the same kind and executable bit,
gitlinks are registered submodules checked out at the recorded commit, and each
initialised submodule's own tracked files match its HEAD the same way. HEAD must
equal COMMIT and nothing may be untracked or ignored."""
import os, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(d, *a, inp=None):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, check=True, env=env, input=inp).stdout
bad = []
def check(d, rev, label):
    tree = {}
    for line in git(d, "ls-tree", "-r", "-z", "--full-tree", rev).split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1); mode, kind, sha = meta.split()
            tree[path] = (mode, sha)
    idx = {}
    for line in git(d, "ls-files", "-s", "-z").split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1); mode, sha, stage = meta.split()
            idx.setdefault(path, []).append((mode, sha, stage))
    if set(idx) != set(tree):
        bad.append(f"{label}: index paths differ from tree ({len(set(idx) ^ set(tree))})")
    files, links = [], []
    for p, (mode, sha) in tree.items():
        if idx.get(p) != [(mode, sha, b"0")]:
            bad.append(f"{label}: index record {p!r} {idx.get(p)} != {(mode, sha)}")
        full = os.path.join(d, p.decode())
        if mode == b"160000":
            links.append((p.decode(), sha.decode())); continue
        if mode == b"120000":
            if not os.path.islink(full) or os.readlink(full).encode() != git(d, "cat-file", "blob", sha.decode()):
                bad.append(f"{label}: symlink {p!r}")
            continue
        if os.path.islink(full) or not os.path.isfile(full):
            bad.append(f"{label}: not a regular file {p!r}"); continue
        if bool(os.stat(full).st_mode & 0o111) != (mode == b"100755"):
            bad.append(f"{label}: mode {p!r}")
        files.append((p, sha))
    if files:
        got = git(d, "hash-object", "--no-filters", "--stdin-paths",
                  inp=b"\n".join(os.path.join(d, p.decode()).encode() for p, _ in files) + b"\n").split()
        for (p, sha), h in zip(files, got):
            if h != sha:
                bad.append(f"{label}: bytes {p!r}")
    print(f"{label}: {len(files)} blobs, {len(links)} gitlinks checked at {rev[:12]}")
    return links
head = git(repo, "rev-parse", "HEAD").decode().strip()
if head != commit:
    bad.append(f"HEAD {head} != {commit}")
for path, sha in check(repo, commit, "parent"):
    sub = os.path.join(repo, path)
    if not os.path.exists(os.path.join(sub, ".git")):
        print(f"submodule {path} not initialised (gitlink {sha[:12]})"); continue
    sh = git(sub, "rev-parse", "HEAD").decode().strip()
    if sh != sha:
        bad.append(f"submodule {path} at {sh} != gitlink {sha}"); continue
    check(sub, sha, f"submodule {path}")
    if git(sub, "status", "--porcelain", "--ignored"):
        bad.append(f"submodule {path}: untracked or ignored files")
if git(repo, "status", "--porcelain", "--ignored"):
    bad.append("parent: untracked or ignored files")
for b in bad: print("FAIL", b)
print("verify_clone:", "OK" if not bad else f"{len(bad)} failure(s)")
sys.exit(1 if bad else 0)
