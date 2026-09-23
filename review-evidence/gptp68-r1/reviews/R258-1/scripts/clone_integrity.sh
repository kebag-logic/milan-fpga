#!/bin/bash
# Prove the review clone still holds the exact head: HEAD and tree ids, a
# clean status, no assume-unchanged/skip-worktree bits, the index equal to
# the head tree (mode, blob, path), every tracked file's bytes hashing to its
# blob id with its mode, and the gitlink population (none expected here).
set -euo pipefail
. "$(dirname "$0")/env.sh"
cd "$CLONE"
fail=0
[ "$(git rev-parse HEAD)" = "$HEAD_SHA" ] || { echo "HEAD moved"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = 10154fc3f95ccc542a6f5dcd8a58105d302fd1af ] || { echo "tree moved"; fail=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$st" ] && echo "status: clean (incl. ignored and untracked)" || { echo "status: $st"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' || true)
[ -z "$flags" ] && echo "index flags: none hidden" || { echo "index flags: $flags"; fail=1; }
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') \
  && echo "index == HEAD tree (mode blob path)" || fail=1
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest#* }
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  got=$(git hash-object --no-filters "$path")
  fm=100644; [ -x "$path" ] && fm=100755; [ -L "$path" ] && fm=120000
  if [ "$got" != "$blob" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $path"; bad=$((bad+1)); fi
done < <(git ls-tree -r HEAD)
echo "tracked files byte/mode checked: $n mismatches: $bad"
[ "$bad" = 0 ] || fail=1
gl=$(git ls-tree -r HEAD | awk '$1=="160000"'); gi=$(git ls-files -s | awk '$1=="160000"')
echo "gitlinks in HEAD tree: ${gl:-none}; in index: ${gi:-none}"
[ "$gl" = "$gi" ] || fail=1
echo "integrity: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
