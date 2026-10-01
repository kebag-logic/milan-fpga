#!/bin/sh
# R417-2: re-derive the merge of main d5f73bac into the lane head 54c1e2b and
# compare it with the published merge a4ba9f7; then hold each side's own paths
# to that side. Usage: check_merge.sh <clone>
set -u
cd "$1"
MAIN=d5f73bac158276a9fcf549185bad5c65c0498dae
echo "git merge-tree --write-tree 54c1e2b $MAIN:"
T=$(git merge-tree --write-tree --name-only 54c1e2b $MAIN | head -1)
git merge-tree --write-tree --name-only 54c1e2b $MAIN | sed -n '2,/^$/p'
echo "files where the published merge differs from the automatic merge result:"
git diff --name-only "$T" a4ba9f7
for f in tb/pp_top/Makefile tb/pp_top/sim_main.cpp tb/pp_top/README.md; do
  echo "== $f: lines the resolution removes or adds besides the conflict markers"
  git diff "$T" a4ba9f7 -- "$f" | grep '^[-+]' | grep -v '^+++\|^---' \
    | grep -v '^-<<<<<<<\|^-=======\|^->>>>>>>' | cut -c1-110
done
for p in hdl/maap tb/maap tb/rx_validator tb/adp_engine tb/srp_top .github; do
  git diff --quiet $MAIN HEAD -- "$p" && r=equal || r=DIFFERS
  echo "$p at HEAD vs main $MAIN: $r"
done
for p in hdl/aecp hdl/top tb/ucpu; do
  git diff --quiet 54c1e2b a4ba9f7 -- "$p" && r=equal || r=DIFFERS
  echo "$p at merge a4ba9f7 vs lane 54c1e2b: $r"
done
echo "merge parents: $(git rev-parse a4ba9f7^1 a4ba9f7^2 | tr '\n' ' ')"
