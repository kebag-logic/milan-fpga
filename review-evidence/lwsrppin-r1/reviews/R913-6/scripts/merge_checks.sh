#!/bin/sh
# Reproduce the R913-6 sync-merge checks from a clean clone at 2b98e219 (run from the clone root).
set -eu
H=2b98e219a5e2b0681f76be90083fc05e47a8f6c0; PRP=67838b37; UPP=e608f8d8; UB=2509db68
test "$(git rev-parse HEAD)" = "$H"
echo "== path sets"; git diff --name-status $PRP $H > /tmp/r913_d; git diff --name-status $UB $UPP > /tmp/r913_u; cmp /tmp/r913_d /tmp/r913_u && echo SAME-PATHSET
echo "== blob table (both-side paths differ from both parents by construction)"
for f in $(cut -f2 /tmp/r913_u); do
  a=$(git rev-parse -q --verify $PRP:$f || echo NONE); b=$(git rev-parse -q --verify $UB:$f || echo NONE)
  c=$(git rev-parse -q --verify $H:$f || echo NONE); d=$(git rev-parse -q --verify $UPP:$f || echo NONE)
  if [ "$a" = "$b" ] && [ "$c" = "$d" ]; then :; else echo "NOT-PURE-UPSTREAM $f"; fi
done
echo "== SUBMODULES.md three-way merge"
t=$(mktemp -d); git show $PRP:docs/reference/SUBMODULES.md > $t/o; git show $UB:docs/reference/SUBMODULES.md > $t/b; git show $UPP:docs/reference/SUBMODULES.md > $t/u
git merge-file -p $t/o $t/b $t/u > $t/m && cmp $t/m docs/reference/SUBMODULES.md && echo "merge-file clean and equal to head"
echo "== generator re-run"
sha256sum docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png docs/diagrams/PNG_MANIFEST.json > $t/before
python3 docs/diagrams/submodule_boundaries.gen.py
sha256sum docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png docs/diagrams/PNG_MANIFEST.json > $t/after
cmp $t/before $t/after && echo GENERATOR-BYTE-IDENTICAL
git status --porcelain | wc -l
