#!/usr/bin/env python3
"""Verify a clone's tracked files byte-for-byte against its index and HEAD.
Usage: verify_restore.py <repo> <expected head>"""
import os, stat, subprocess, sys
repo, want = sys.argv[1], sys.argv[2]
git = lambda *a, **k: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True, **k).stdout
head = git("rev-parse", "HEAD").strip()
entries = [l.split(None, 3) for l in git("ls-files", "-s").splitlines()]
tree = {l.split("\t")[1]: l.split()[:3] for l in git("ls-tree", "-r", "HEAD").splitlines()}
bad, files = [], []
for mode, blob, _stage, path in entries:
    t = tree.get(path)
    if t is None or t[0] != mode or t[2] != blob:
        bad.append(f"index!=HEAD {path}")
    if mode == "160000":
        sub = git("-C", path, "rev-parse", "HEAD").strip() if os.path.exists(os.path.join(repo, path, ".git")) else "(not checked out)"
        print(f"gitlink {path} {blob} checkout={sub} {'OK' if sub in (blob, '(not checked out)') else 'MISMATCH'}")
        if sub not in (blob, "(not checked out)"):
            bad.append(f"gitlink {path}")
        continue
    full = os.path.join(repo, path)
    st = os.lstat(full)
    real = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & 0o111 else "100644")
    if real != mode:
        bad.append(f"mode {path} {real}!={mode}")
    files.append((path, blob))
hashes = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", "--stdin-paths"],
                        input="\n".join(p for p, _ in files), capture_output=True, text=True, check=True).stdout.split()
for (path, blob), h in zip(files, hashes):
    if h != blob:
        bad.append(f"bytes {path}")
extra = git("status", "--porcelain", "--ignored", "--untracked-files=all").strip()
print(f"head={head} expected={want} {'OK' if head == want else 'MISMATCH'}")
print(f"tracked_files={len(files)} gitlinks={len(entries)-len(files)} mismatches={len(bad)} untracked_or_ignored={'none' if not extra else extra[:200]}")
for b in bad[:20]: print(" ", b)
sys.exit(1 if bad or head != want or extra else 0)
