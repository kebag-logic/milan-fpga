#!/usr/bin/env bash
# Per-file three-way composition check for the merge-train candidate.
# Usage: compose_check.sh <repo>
# For every path changed between the merge base B and the candidate H:
#   - changed only by the PR source S  -> H must equal S
#   - changed only by the predecessor P -> H must equal P
#   - changed by both                   -> reported BOTH for manual review
set -euo pipefail
repo=${1:?repo}
B=d5858bbee328cf8d2c39a99ec14203f5d0ddd123   # merge base (dev before #727)
S=97e713168470bfae2685521fa557dc462b782b32   # PR #705 source head
P=ada26e56ac42ee5de311aef84cb86c8435b97cee   # predecessor candidate
H=6758fe0216955c96f37b52d7129509586c9c0a8c   # this candidate
cd "$repo"
echo "merge-base(S,P)=$(git merge-base $S $P)"
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
echo "tree(H)=$(git rev-parse $H^{tree})"
[ "$bad" = 0 ]
