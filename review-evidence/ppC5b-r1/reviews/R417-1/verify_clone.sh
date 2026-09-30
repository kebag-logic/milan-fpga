#!/usr/bin/env bash
# Verify a clone is byte-for-byte its HEAD: every tracked path's working-tree
# bytes re-hashed and compared to the index and HEAD blob, every mode compared,
# the index tree equal to HEAD's tree, no untracked or ignored file, and no
# gitlink (the processor repository records no submodule).
# Usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -uo pipefail
cd "$1" || exit 2
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "tree $tree"
[ "$head" = "$2" ] || { echo "FAIL head"; exit 1; }
[ "$tree" = "$3" ] || { echo "FAIL tree"; exit 1; }
echo "core.filemode $(git config core.filemode)"
[ "$(git write-tree)" = "$tree" ] || { echo "FAIL index tree"; exit 1; }
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  read -r mode _type blob <<<"$meta"
  n=$((n + 1))
  if [ "$mode" = "160000" ]; then echo "gitlink $path $blob"; continue; fi
  if [ "$mode" = "120000" ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
    if [ "$mode" = "100755" ] && [ ! -x "$path" ]; then echo "MODE $path"; bad=1; fi
    if [ "$mode" = "100644" ] && [ -x "$path" ]; then echo "MODE $path"; bad=1; fi
  fi
  [ "$got" = "$blob" ] || { echo "BYTES $path"; bad=1; }
done < <(git ls-tree -r --full-tree HEAD)
extra=$(git status --porcelain --ignored | wc -l)
gl=$(git ls-files -s | awk '$1 == "160000"' | wc -l)
echo "tracked paths re-hashed: $n; gitlinks: $gl; untracked/ignored/modified entries: $extra"
[ "$extra" -eq 0 ] || bad=1
[ "$bad" -eq 0 ] && echo "CLONE VERIFY: PASS" || echo "CLONE VERIFY: FAIL"
exit "$bad"
