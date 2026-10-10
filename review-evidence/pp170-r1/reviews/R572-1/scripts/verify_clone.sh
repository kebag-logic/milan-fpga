#!/usr/bin/env bash
# Usage: verify_clone.sh <clone> : prove exact-head bytes, modes, index; no gitlinks expected
set -euo pipefail
cd "$1"
H=c3864686c0b254bd2d7b7f733078ec302fb9be62; T=305218ec054c05ed7e023594e71642049fc790e9
echo "HEAD $(git rev-parse HEAD) $( [ "$(git rev-parse HEAD)" = $H ] && echo OK || echo MISMATCH)"
echo "tree $(git rev-parse HEAD^{tree}) $( [ "$(git rev-parse HEAD^{tree})" = $T ] && echo OK || echo MISMATCH)"
echo "index tree $(git write-tree) $( [ "$(git write-tree)" = $T ] && echo OK || echo MISMATCH)"
git update-index -q --really-refresh >/dev/null || true
git diff --quiet && echo "worktree vs index: clean" || echo "worktree vs index: DIFFERENT"
git diff --cached --quiet && echo "index vs HEAD: clean" || echo "index vs HEAD: DIFFERENT"
bad=0; n=0
while read -r mode type sha path; do
  n=$((n+1))
  [ "$type" = blob ] || continue
  [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || { echo "BYTES $path"; bad=$((bad+1)); }
  m=$(stat -c %a -- "$path"); want=$([ "$mode" = 100755 ] && echo 755 || echo 644)
  [ "$mode" = 120000 ] || [ "$m" = "$want" ] || [ "$mode" = 100644 -a "$m" = 664 ] || { echo "MODE $path $m vs $mode"; bad=$((bad+1)); }
done < <(git ls-tree -r HEAD | tr '\t' ' ')
echo "tracked entries $n, byte/mode mismatches $bad"
echo "gitlinks: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l) (none required by this repository)"
echo "untracked/ignored: $(git status --porcelain=v1 --ignored | wc -l)"
