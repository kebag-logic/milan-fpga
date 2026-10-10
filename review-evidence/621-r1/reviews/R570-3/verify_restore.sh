#!/usr/bin/env bash
# Verify a review clone is byte-exact at its head after probes.
# Usage: verify_restore.sh <repo-root> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "TREE $tree"
[ "$head" = "$2" ] || { echo "MISMATCH head"; fail=1; }
[ "$tree" = "$3" ] || { echo "MISMATCH tree"; fail=1; }
check_repo() {  # rehash every tracked regular blob and compare id and mode with the index
  local dir=$1 n=0 bad=0
  while IFS=$'\t' read -r meta path; do
    set -- $meta; mode=$1; id=$2
    [ "$mode" = 160000 ] && continue
    n=$((n + 1))
    if [ "$mode" = 120000 ]; then
      got=$(printf '%s' "$(readlink "$dir/$path")" | git hash-object --stdin)
    else
      got=$(git -C "$dir" hash-object --no-filters -- "$path")
      if [ "$mode" = 100755 ]; then [ -x "$dir/$path" ] || { echo "MODE $dir/$path"; bad=$((bad + 1)); }
      else [ -x "$dir/$path" ] && { echo "MODE $dir/$path"; bad=$((bad + 1)); }; fi
    fi
    [ "$got" = "$id" ] || { echo "BYTES $dir/$path"; bad=$((bad + 1)); }
  done < <(git -C "$dir" ls-files -s | awk '{print $1" "$2"\t"substr($0, index($0, "\t") + 1)}')
  echo "$dir: $n tracked blobs rehashed, $bad differ"
  [ $bad = 0 ] || fail=1
  [ -z "$(git -C "$dir" diff --cached --name-only HEAD)" ] || { echo "INDEX differs from HEAD in $dir"; fail=1; }
  flags=$(git -C "$dir" ls-files -v | grep -c '^[a-zS]' || true)
  echo "$dir: assume-unchanged/skip-worktree entries $flags"; [ "$flags" = 0 ] || fail=1
  st=$(git -C "$dir" status --porcelain --ignored --untracked-files=all)
  [ -z "$st" ] && echo "$dir: status clean (including ignored)" || { echo "$dir: STATUS"; echo "$st" | head; fail=1; }
}
check_repo .
git ls-tree HEAD | awk '$1 == "160000" {print $3" "$4}' | while read -r id path; do
  if [ -e "$path/.git" ]; then
    top=$(git -C "$path" rev-parse --show-toplevel)
    [ "$top" = "$(pwd)/$path" ] || { echo "SUBMODULE TOPLEVEL $path -> $top"; exit 1; }
    got=$(git -C "$path" rev-parse HEAD)
    echo "gitlink $path $id checked-out $got $([ "$got" = "$id" ] && echo EQUAL || echo DIFFER)"
  else
    echo "gitlink $path $id uninitialised"
  fi
done
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
  [ -e "$sub/.git" ] && check_repo "$sub"
done
[ $fail = 0 ] && echo "RESTORE: EXACT" || echo "RESTORE: NOT EXACT"
exit $fail
