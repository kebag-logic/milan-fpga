#!/bin/sh
# Verify a checkout is byte-exact at its expected head: index tree, index
# flags, every tracked blob's bytes and mode, and the required gitlinks.
# Usage: verify_restore.sh <checkout> <expected-head> <expected-tree>
set -eu
repo=$1 head=$2 tree=$3
cd "$repo"
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] || { echo "HEAD tree differs"; fail=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "index tree differs"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' || true)
[ -z "$flags" ] || { echo "index flags present:"; echo "$flags"; fail=1; }
[ -z "$(git ls-files --stage | awk '$3 != 0')" ] || { echo "unmerged entries"; fail=1; }
# Every tracked regular file and symlink: bytes and mode against HEAD.
bad=$(git ls-tree -r -z HEAD | python3 -I -c '
import os, sys, subprocess, stat
bad = 0
for rec in sys.stdin.buffer.read().split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, kind, oid = meta.split()
    if kind != b"blob":
        continue
    p = os.fsdecode(path)
    st = os.lstat(p)
    if mode == b"120000":
        ok = stat.S_ISLNK(st.st_mode)
        got = subprocess.run(["git", "hash-object", "--stdin"], input=os.fsencode(os.readlink(p)),
                             capture_output=True).stdout.strip() if ok else b""
    else:
        ok = stat.S_ISREG(st.st_mode) and (bool(st.st_mode & 0o100) == (mode == b"100755"))
        got = subprocess.run(["git", "hash-object", "--no-filters", p], capture_output=True).stdout.strip()
    if not ok or got != oid:
        bad += 1
        print("MISMATCH", p, file=sys.stderr)
print(bad)
')
[ "$bad" = 0 ] || { echo "$bad tracked blob(s) differ"; fail=1; }
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sub" | awk '{print $3}')
  got=$(git -C "$sub" rev-parse HEAD)
  [ "$want" = "$got" ] || { echo "gitlink $sub: want $want got $got"; fail=1; }
  [ -z "$(git -C "$sub" status --porcelain --ignored)" ] || { echo "submodule $sub not clean"; fail=1; }
  echo "gitlink $sub $want checkout $got"
done
[ -z "$(git status --porcelain --ignored)" ] || { echo "worktree not clean"; fail=1; }
echo "tracked blobs differing: $bad"
[ $fail = 0 ] && echo "RESTORE: EXACT" || echo "RESTORE: DIFFERENT"
exit $fail
