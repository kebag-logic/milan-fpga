#!/usr/bin/env bash
# Verify a checkout equals an exact commit: HEAD, tree, index, every tracked
# blob's bytes and mode, required gitlinks, and no untracked/ignored residue.
# Usage: integrity.sh <checkout> <head-sha> <tree-sha>
set -u
cd "$1" || exit 2
head=$2 tree=$3 rc=0
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD ok $head" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && echo "tree ok $tree" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$tree" ] && echo "index tree ok" || { echo "INDEX MISMATCH"; rc=1; }
git update-index -q --really-refresh
if git diff --quiet HEAD -- && git diff --cached --quiet; then echo "worktree/index clean vs HEAD"; else echo "DIFF PRESENT"; git diff --stat HEAD; rc=1; fi
# Byte-level: hash every tracked regular file and compare with HEAD's blob and mode.
bad=$(git ls-tree -r HEAD | python3 -I -c '
import os, subprocess, sys
bad = 0; n = 0
for line in sys.stdin:
    meta, path = line.rstrip("\n").split("\t", 1)
    mode, kind, sha = meta.split()
    if kind != "blob":
        continue
    n += 1
    if mode == "120000":
        ok = os.path.islink(path) and subprocess.run(["git","hash-object","--stdin"],input=os.readlink(path).encode(),capture_output=True).stdout.decode().strip()==sha
    else:
        got = subprocess.run(["git","hash-object",path],capture_output=True,text=True).stdout.strip()
        ex = os.access(path, os.X_OK)
        ok = got == sha and ex == (mode == "100755")
    if not ok:
        bad += 1; print("BLOB/MODE MISMATCH", path, file=sys.stderr)
print(f"{n} {bad}")
')
echo "tracked blobs checked/bad: $bad"; [ "${bad#* }" = 0 ] || rc=1
git ls-tree HEAD third_party/tsn-c-stack third_party/lwSRP third_party/verilog-axis protocol-processor gptp-processor external
git submodule status
for s in third_party/tsn-c-stack third_party/lwSRP third_party/verilog-axis protocol-processor gptp-processor; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}'); got=$(git -C "$s" rev-parse HEAD 2>/dev/null)
  if [ "$want" = "$got" ] && [ -z "$(git -C "$s" status --porcelain 2>/dev/null)" ]; then echo "gitlink ok $s $want (clean)"; else echo "GITLINK MISMATCH $s want=$want got=$got"; rc=1; fi
done
u=$(git status --porcelain --ignored | wc -l); echo "untracked/ignored entries: $u"; [ "$u" = 0 ] || { git status --porcelain --ignored; rc=1; }
echo "integrity rc=$rc"; exit $rc
