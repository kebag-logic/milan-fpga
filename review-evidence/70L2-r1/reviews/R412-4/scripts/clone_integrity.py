#!/usr/bin/env python3
"""clone_integrity.py <clone> <head> <tree>: the review clone is byte-exact.

Checks HEAD and its tree, an empty porcelain status (untracked included),
index == HEAD (paths, modes, blob ids), every tracked regular file's bytes
hash to its blob id, and each initialized submodule's checkout == its gitlink."""
import subprocess, sys
from pathlib import Path

clone, head, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
def git(*a, cwd=clone):
    return subprocess.run(["git", "-C", str(cwd), *a], check=True,
                          capture_output=True, text=True).stdout
ok = True
def check(cond, what):
    global ok
    print(("OK   " if cond else "FAIL ") + what)
    ok &= bool(cond)
check(git("rev-parse", "HEAD").strip() == head, f"HEAD == {head}")
check(git("rev-parse", "HEAD^{tree}").strip() == tree, f"HEAD^{{tree}} == {tree}")
check(git("status", "--porcelain", "--untracked-files=all", "--ignore-submodules=none").strip() == "",
      "porcelain status empty (untracked and submodules included)")
idx = {l.split("\t")[1]: l.split()[0:2] for l in git("ls-files", "-s").splitlines()}
trk = {l.split("\t")[1]: l.split()[0:3:2] for l in git("ls-tree", "-r", "HEAD").splitlines()}
check(idx == trk, f"index == HEAD tree for {len(trk)} entries (mode, object id)")
bad = []
for path, (mode, oid) in trk.items():
    if mode in ("100644", "100755"):
        p = clone / path
        h = subprocess.run(["git", "-C", str(clone), "hash-object", "--no-filters", str(p)],
                           check=True, capture_output=True, text=True).stdout.strip()
        exe = p.stat().st_mode & 0o111 != 0
        if h != oid or exe != (mode == "100755"):
            bad.append(path)
    elif mode == "120000":
        if subprocess.run(["git", "-C", str(clone), "hash-object", "--stdin"],
                          input=str(Path.readlink(clone / path)), capture_output=True,
                          text=True).stdout.strip() != oid:
            bad.append(path)
check(not bad, f"tracked file bytes and exec bits match blobs ({len(bad)} mismatched: {bad[:5]})")
for path, (mode, oid) in trk.items():
    if mode == "160000":
        sub = clone / path
        if (sub / ".git").exists():
            check(git("rev-parse", "HEAD", cwd=sub).strip() == oid and
                  git("status", "--porcelain", cwd=sub).strip() == "",
                  f"submodule {path} checked out clean at gitlink {oid}")
        else:
            print(f"INFO {path}: gitlink {oid}, not initialized (as at round start)")
print("CLONE INTEGRITY", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
