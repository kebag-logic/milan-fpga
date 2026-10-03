#!/usr/bin/env bash
# R449-3: verify the isolated review clone still holds the exact head bytes.
# usage: integrity.sh <clone>
set -u
c=$1; cd "$c" || exit 2
rc=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "tree $tree"
[ "$head" = 39298e03aa53d5f82c7485b8d12d2b69a47b0d55 ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = 7f3b4639ee70ad34c567f4df4cc9fec4c8172780 ] || { echo "TREE MISMATCH"; rc=1; }
git symbolic-ref -q HEAD >/dev/null && { echo "NOT DETACHED"; rc=1; } || echo "detached: yes"
st=$(git status --porcelain --ignored)
if [ -z "$st" ]; then echo "status --porcelain --ignored: empty"; else echo "status not empty:"; echo "$st"; rc=1; fi
if diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null; then
  echo "index == ls-tree -r HEAD (mode, blob, path)"; else echo "INDEX DIFFERS FROM HEAD"; rc=1; fi
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  n=$((n + 1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $blob"; continue; fi
  got=$(git hash-object --no-filters -- "$path")
  [ "$got" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=$((bad + 1)); }
  case "$mode" in
    100755) [ -x "$path" ] || { echo "MODE MISMATCH $path (want exec)"; bad=$((bad + 1)); } ;;
    100644) [ ! -x "$path" ] || { echo "MODE MISMATCH $path (want non-exec)"; bad=$((bad + 1)); } ;;
    120000) [ -L "$path" ] || { echo "MODE MISMATCH $path (want symlink)"; bad=$((bad + 1)); } ;;
  esac
done < <(git ls-files -s)
echo "tracked entries re-hashed: $n, mismatches: $bad"
echo "gitlinks (160000 entries): $(git ls-files -s | awk '$1==160000' | wc -l)"
[ "$bad" -eq 0 ] || rc=1
echo "integrity rc=$rc"
exit $rc
