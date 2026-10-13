#!/usr/bin/env bash
# Per-file three-way composition check for the merge-train candidate.
# Usage: compose_check.sh <repo>
# For every path changed between live dev B and the candidate H:
#   - changed only by the PR source S  -> H must equal S
#   - changed only by the predecessor P -> H must equal P
#   - changed by both                   -> reported BOTH for manual review
# Also proves H's tree is the clean three-way merge of P and S.
set -euo pipefail
repo=${1:?repo}
B=e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c   # live dev (#726, PR #729); the PR source last merged it
S=d40e4e9827be2516f8f34b9d65f0a483fff2194c   # PR #705 source head
P=ac0142539856222b84ef8e5af414d12132a5bebf   # predecessor candidate (B16 PR #725, #730 PR #731)
H=7094848c928c4c04bf5fae51346b0e1e5848a971   # this candidate
cd "$repo"
echo "merge-base(S,P)=$(git merge-base $S $P)"
echo "is-ancestor B of S: $(git merge-base --is-ancestor $B $S && echo yes || echo no)"
echo "tree(B)=$(git rev-parse $B^{tree}) tree(cdb49e7ec)=$(git rev-parse cdb49e7ec^{tree}) (the #726 train candidate on P's first-parent chain)"
echo "parents(H)=$(git rev-parse $H^1) $(git rev-parse $H^2)"
blob() { git rev-parse -q --verify "$1:$2" 2>/dev/null || echo none; }
n=0; both=0; bad=0
while IFS= read -r f; do
  n=$((n+1))
  b=$(blob $B "$f"); s=$(blob $S "$f"); p=$(blob $P "$f"); h=$(blob $H "$f")
  if [ "$s" != "$b" ] && [ "$p" != "$b" ]; then
    both=$((both+1)); echo "BOTH $f base=$b src=$s pred=$p cand=$h"
  elif [ "$s" != "$b" ]; then
    [ "$h" = "$s" ] || { bad=$((bad+1)); echo "MISMATCH-SRC $f"; }
  elif [ "$p" != "$b" ]; then
    [ "$h" = "$p" ] || { bad=$((bad+1)); echo "MISMATCH-PRED $f"; }
  else
    bad=$((bad+1)); echo "NEITHER $f"
  fi
done < <(git diff --name-only $B $H)
echo "paths=$n both=$both mismatches=$bad"
echo "predecessor-only paths (H vs S):"; git diff --name-only $S $H | sed 's/^/  /'
mt=$(git merge-tree --write-tree $P $S | head -1)
echo "merge-tree(P,S)=$mt tree(H)=$(git rev-parse $H^{tree})"
[ "$mt" = "$(git rev-parse $H^{tree})" ] || { echo "MERGE TREE DIFFERS"; bad=$((bad+1)); }
[ "$bad" = 0 ]
