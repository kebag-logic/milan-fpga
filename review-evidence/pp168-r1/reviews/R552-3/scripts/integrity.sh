#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Usage: integrity.sh <clone> <expected-head> <expected-tree>
# Read-only: prints head/tree, worktree and index state, re-hashes every
# tracked file's bytes and mode against the index, and lists gitlinks.
set -u
c=$1; h=$2; t=$3; rc=0
cd "$c" || exit 2
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "head $head"; echo "tree $tree"
[ "$head" = "$h" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = "$t" ] || { echo "TREE MISMATCH"; rc=1; }
st=$(git status --porcelain --ignored=no)
[ -z "$st" ] && echo "worktree clean" || { echo "worktree dirty:"; echo "$st"; rc=1; }
git diff --cached --quiet HEAD && echo "index equals HEAD" || { echo "INDEX DIFFERS"; rc=1; }
itree=$(git write-tree); echo "index tree $itree"
[ "$itree" = "$t" ] || { echo "INDEX TREE MISMATCH"; rc=1; }
# per-file byte and mode check against the index
python3 -I - "$c" <<'EOF' || rc=1
import os, stat, subprocess, sys
c = sys.argv[1]
out = subprocess.run(["git", "-C", c, "ls-files", "-s", "-z"], check=True,
                     capture_output=True).stdout.split(b"\0")
n = bad = links = 0
for rec in out:
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, sha, _ = meta.split()
    p = os.path.join(c.encode(), path)
    if mode == b"160000":
        links += 1
        continue
    n += 1
    st = os.lstat(p)
    if mode == b"120000":
        ok_mode = stat.S_ISLNK(st.st_mode)
    else:
        ok_mode = stat.S_ISREG(st.st_mode) and (
            bool(st.st_mode & 0o111) == (mode == b"100755"))
    got = subprocess.run(["git", "-C", c, "hash-object", "--no-filters", p],
                         check=True, capture_output=True).stdout.strip()
    if got != sha or not ok_mode:
        bad += 1
        print("MISMATCH", path.decode(), mode.decode(), sha.decode(), got.decode())
print(f"tracked files {n}, byte/mode mismatches {bad}, gitlinks {links}")
sys.exit(1 if bad else 0)
EOF
exit $rc
