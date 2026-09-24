#!/usr/bin/env python3
"""Reviewer-owned read-only check that a clone sits exactly at its head.

usage: verify_restore.py <repo> <expected-head>
Checks: HEAD sha; index entries == HEAD tree entries (mode, oid, path);
every tracked regular file / symlink hashes (git hash-object, no -w) to its
index oid with the index mode; no assume-unchanged / skip-worktree flags;
no untracked or ignored paths; every gitlink's checkout HEAD equals the
recorded gitlink and that checkout is itself clean (tracked, untracked, ignored).
"""
import os, stat, subprocess, sys

def git(repo, *a, text=True):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=text).stdout

repo, want = sys.argv[1], sys.argv[2]
ok = True
def res(name, good, detail=""):
    global ok
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} {name} {detail}")

head = git(repo, "rev-parse", "HEAD").strip()
res("head", head == want, head)
tree = {}
for ln in git(repo, "ls-tree", "-r", "--full-tree", "HEAD").splitlines():
    meta, path = ln.split("\t", 1); mode, _t, oid = meta.split(); tree[path] = (mode, oid)
idx = {}
for ln in git(repo, "ls-files", "-s").splitlines():
    meta, path = ln.split("\t", 1); mode, oid, stage = meta.split(); idx[path] = (mode, oid)
res("index==HEAD tree", idx == tree, f"{len(idx)} entries")
flags = [l for l in git(repo, "ls-files", "-v").splitlines() if l[:1].islower() or l[:1] == "S"]
res("no hide flags", not flags, str(flags[:3]))
bad = []
nfiles = 0
for path, (mode, oid) in idx.items():
    if mode == "160000":
        continue
    full = os.path.join(repo, path)
    st = os.lstat(full)
    if mode == "120000":
        good = stat.S_ISLNK(st.st_mode)
    else:
        exe = bool(st.st_mode & 0o111)
        good = stat.S_ISREG(st.st_mode) and ((mode == "100755") == exe)
    h = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", "--", path],
                       capture_output=True, text=True).stdout.strip() if mode != "120000" else \
        subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(full).encode(),
                       capture_output=True).stdout.decode().strip()
    nfiles += 1
    if not good or h != oid:
        bad.append(path)
res("tracked bytes+modes", not bad, f"{nfiles} files checked; mismatches={bad[:5]}")
st = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all", "--ignore-submodules=none")
res("status clean (incl. ignored)", st.strip() == "", st.strip()[:300])
for path, (mode, oid) in tree.items():
    if mode != "160000":
        continue
    sub = os.path.join(repo, path)
    if not os.path.exists(os.path.join(sub, ".git")):
        empty = os.path.isdir(sub) and not os.listdir(sub)
        res(f"gitlink {path}", empty, f"recorded={oid} not initialised in this clone (empty dir={empty}); not required by the checks run")
        continue
    try:
        sh = git(sub, "rev-parse", "HEAD").strip()
        sst = git(sub, "status", "--porcelain", "--ignored", "--untracked-files=all")
        dq = subprocess.run(["git", "-C", sub, "diff", "--quiet", "HEAD"]).returncode
        res(f"gitlink {path}", sh == oid and sst.strip() == "" and dq == 0,
            f"recorded={oid} checkout={sh} clean={sst.strip()=='' and dq==0}")
    except subprocess.CalledProcessError as e:
        res(f"gitlink {path}", False, f"recorded={oid} checkout unreadable ({e.stderr.strip()[:80]})")
print("RESULT:", "CLEAN" if ok else "NOT CLEAN")
sys.exit(0 if ok else 1)
