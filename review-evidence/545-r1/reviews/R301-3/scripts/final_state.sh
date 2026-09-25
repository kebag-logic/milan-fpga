#!/usr/bin/env bash
# Verifies the clone is at the exact reviewed head with pristine tracked bytes,
# modes and index, no untracked or ignored residue, and submodule checkouts at
# their gitlinks with clean trees.
set -u
H=b376f6113b388929fe82e883d400e5361319b966; T=659205c787ef36b51185790d0579dfbcd6705682
rc=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "head OK $H" || { echo "head MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree OK $T" || { echo "tree MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree OK" || { echo "index tree MISMATCH"; rc=1; }
git diff --quiet && git diff --cached --quiet && echo "worktree/index vs HEAD: no diff (bytes and modes)" || { echo "DIFF present"; rc=1; }
st=$(git status --porcelain --ignored); [ -z "$st" ] && echo "status --ignored: empty" || { echo "residue:"; echo "$st"; rc=1; }
for sm in external gptp-processor protocol-processor third_party/verilog-axis; do
  gl=$(git rev-parse ":$sm")
  if [ -e "$sm/.git" ]; then
    h=$(git -C "$sm" rev-parse HEAD); s=$(git -C "$sm" status --porcelain --ignored | wc -l)
    [ "$h" = "$gl" ] && [ "$s" = 0 ] && echo "submodule $sm OK $gl clean" || { echo "submodule $sm head=$h gitlink=$gl residue=$s"; rc=1; }
  else echo "submodule $sm gitlink=$gl (not initialized)"; fi
done
exit $rc
