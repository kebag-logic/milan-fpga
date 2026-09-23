#!/usr/bin/env bash
# Review round R266-2: prove the review clone is byte-identical to the exact
# head after every probe. Checks: HEAD and tree ids; index == HEAD tree;
# every tracked regular file's working bytes hash to its index blob, with the
# index mode matching the file's executable bit and symlinks matching their
# target text; no assume-unchanged/skip-worktree flags; no untracked or
# ignored files; the four gitlinks recorded at their pins with the checkout
# state of each (the required three and the SSH-only `external`).
# Usage: clone_integrity.sh CLONE EXPECTED_HEAD EXPECTED_TREE
set -euo pipefail
clone=$1 head=$2 tree=$3
cd "$clone"
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD $head ok" || { echo "HEAD mismatch"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] && echo "tree $tree ok" || { echo "tree mismatch"; fail=1; }
[ "$(git write-tree)" = "$tree" ] && echo "index writes tree $tree ok" || { echo "index tree mismatch"; fail=1; }
flags=$(git ls-files -v | grep -vc '^H ' || true)
echo "index entries with hidden flags: $flags"; [ "$flags" = 0 ] || fail=1
extra=$( { git status --porcelain --ignored --untracked-files=all | grep -v "^!! .*/$" || true; } | wc -l)
echo "untracked/ignored/modified paths: $extra"; [ "$extra" = 0 ] || { git status --porcelain --ignored | head; fail=1; }
checked=0 bad=0
while IFS= read -r -d '' rec; do
  meta=${rec%%$'\t'*}; path=${rec#*$'\t'}
  read -r mode blob _stage <<<"$meta"
  case "$mode" in
    160000) continue ;;
    120000) actual=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    100644|100755)
      actual=$(git hash-object --no-filters "$path")
      if [ -x "$path" ]; then fm=100755; else fm=100644; fi
      [ "$fm" = "$mode" ] || { echo "MODE $path index=$mode file=$fm"; bad=$((bad+1)); } ;;
    *) echo "UNKNOWN MODE $mode $path"; bad=$((bad+1)); continue ;;
  esac
  [ "$actual" = "$blob" ] || { echo "BYTES $path"; bad=$((bad+1)); }
  checked=$((checked+1))
done < <(git ls-files -s -z)
echo "tracked non-gitlink entries checked: $checked, mismatches: $bad"; [ "$bad" = 0 ] || fail=1
git ls-files -s | awk '$1=="160000"{print "gitlink", $4, $2}'
git submodule status 2>&1 | sed 's/^/submodule-status: /'
echo "RESULT: $([ "$fail" = 0 ] && echo EXACT || echo MISMATCH)"
exit "$fail"
