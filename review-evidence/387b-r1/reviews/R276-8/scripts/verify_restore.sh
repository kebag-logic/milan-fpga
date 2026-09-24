#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head: HEAD, tree,
# index == HEAD (paths, modes, blob ids), worktree bytes hash to the index
# blobs, no untracked or ignored files, and required submodule gitlinks.
# Usage: verify_restore.sh <clone> <head> <tree>
set -u
cd "$1" || exit 2
H=$2 T=$3 bad=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD $H OK" || { echo "HEAD MISMATCH"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree $T OK" || { echo "tree MISMATCH"; bad=1; }
[ "$(git write-tree)" = "$T" ] && echo "index writes tree $T OK" || { echo "index tree MISMATCH"; bad=1; }
git diff --quiet && git diff --cached --quiet && echo "worktree/index vs HEAD: no diff" || { echo "DIFF present"; bad=1; }
n=0; m=0
while IFS= read -r -d '' ent; do
  meta=${ent%%$'\t'*}; path=${ent#*$'\t'}
  set -- $meta; mode=$1 oid=$2
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters "$path"); fi
  if [ "$got" != "$oid" ]; then echo "BLOB MISMATCH $path"; bad=1; m=$((m+1)); fi
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE MISMATCH $path"; bad=1; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE MISMATCH $path"; bad=1; fi
done < <(git ls-files -s -z)
echo "tracked non-gitlink entries hashed: $n, mismatches: $m"
u=$(git status --porcelain --ignored | wc -l); echo "untracked+ignored entries: $u"; [ "$u" = 0 ] || bad=1
git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
git submodule status | sed 's/^/submodule: /'
for s in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git rev-parse HEAD:$s); got=$(git -C $s rev-parse HEAD)
  [ "$want" = "$got" ] && echo "gitlink $s $want checked out OK" || { echo "GITLINK MISMATCH $s"; bad=1; }
  [ -z "$(git -C $s status --porcelain)" ] && echo "  $s clean" || { echo "  $s DIRTY"; bad=1; }
done
echo "verify_restore: $([ $bad = 0 ] && echo PASS || echo FAIL)"
exit $bad
