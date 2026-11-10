#!/usr/bin/env bash
# Reproduce the R802-3 checks on a clean clone of the processor repository.
# Usage: reproduce.sh <clone-dir> <out-dir>
# Read-only against the clone except for the gate's own ignored helper
# directory (.venv-wavedrom), which it removes at the end.
set -u
C=${1:?clone dir}; O=${2:?out dir}
HEAD_EXP=03862f75c89e5c1d84baa4735eff1c1c6f796e25
TREE_EXP=dec0f2f79439b89af8686f87bd1db6653a0585fd
mkdir -p "$O"
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD_EXP" ] || { echo "wrong head"; exit 2; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$TREE_EXP" ] || { echo "wrong tree"; exit 2; }

# 1. the delta is docs-only (empty output expected)
git --no-pager diff --stat 84f6d6a..HEAD -- . ':(exclude)docs' > "$O/nondocs-diff-stat.txt"
git --no-pager diff --stat 84f6d6a..HEAD > "$O/full-diff-stat.txt"
git --no-pager diff --check 044cb25f HEAD > "$O/diff-check.txt"; echo "rc=$?" >> "$O/diff-check.txt"

# 2. the docs gates
make check > "$O/make-check.log" 2>&1; echo "rc=$?" > "$O/make-check.rc"
python3 scripts/gen_matrix.py --check > "$O/gen-matrix-check.log" 2>&1; echo "rc=$?" > "$O/gen-matrix-check.rc"

# 3. the RTL fact GAP-19 rests on: link_up_i reaches three instances only
grep -n "link_up_i" hdl/srp/KL_srp_top.sv > "$O/srp-top-link-up.txt"
grep -n "la_msrp_pend_r\|la_mvrp_pend_r\|need_draw_r\[" hdl/srp/KL_srp_top.sv > "$O/srp-top-leaveall-drivers.txt"

# 4. restore and verify exact head
rm -rf -- ./.venv-wavedrom
{ git status --porcelain --ignored; echo "write-tree $(git write-tree)"; } > "$O/restore-check.txt"
cat "$O"/*.rc
