#!/bin/sh
# Verify a review clone still holds the exact reviewed head, bytes, modes,
# index and required submodule gitlinks. Usage: r329_restore_check.sh <clone>
set -u
cd "$1" || exit 2
fail=0
want_head=104c8a54b183cd9215ed1e3a2e1be1634f48d33d
want_tree=c1d413a847312074618f45635750252aea21e197
echo "HEAD $(git rev-parse HEAD)"; [ "$(git rev-parse HEAD)" = "$want_head" ] || fail=1
echo "TREE $(git rev-parse 'HEAD^{tree}')"; [ "$(git rev-parse 'HEAD^{tree}')" = "$want_tree" ] || fail=1
# index == HEAD (blob ids and modes), worktree == index (bytes and modes)
git diff --cached --quiet --ignore-submodules=none && echo "index==HEAD" || { echo "index differs"; fail=1; }
git diff --quiet --ignore-submodules=none && echo "worktree==index" || { echo "worktree differs"; fail=1; }
n=$(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)
echo "status entries (incl. ignored/untracked): $n"; [ "$n" -eq 0 ] || { git status --porcelain=v1 --ignored | head; fail=1; }
# rehash every tracked regular file against its index blob id
bad=$(git ls-files -s | awk '$1 != "160000" {print $2" "$4}' | while read -r id path; do
  [ "$(git hash-object --no-filters -- "$path")" = "$id" ] || echo "$path"; done | wc -l)
echo "tracked blobs rehashed with mismatches: $bad"; [ "$bad" -eq 0 ] || fail=1
for s in protocol-processor:870ff88ad35bbd532244e4c7e6d7661b9f6e1366 \
         gptp-processor:5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d \
         third_party/verilog-axis:48ff7a7e2ef782cf778d47910cf85835c64b1bce; do
  p=${s%%:*}; w=${s#*:}
  g=$(git ls-tree HEAD "$p" | awk '{print $3}'); c=$(git -C "$p" rev-parse HEAD)
  d=$(git -C "$p" status --porcelain --untracked-files=all | wc -l)
  echo "gitlink $p recorded=$g checkout=$c dirty=$d"
  [ "$g" = "$w" ] && [ "$c" = "$w" ] && [ "$d" -eq 0 ] || fail=1
done
echo "RESULT $([ $fail -eq 0 ] && echo OK || echo FAIL)"
exit $fail
