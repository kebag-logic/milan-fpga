#!/usr/bin/env bash
# Verify the review clone is byte-identical to the exact head: HEAD, index
# tree, every tracked entry's blob and mode, no untracked/ignored/modified
# entry, and each initialised submodule at its gitlink and clean.
# Usage: verify_restore.sh <repo> <expected-head> <expected-tree>
set -u
repo=$1; want_head=$2; want_tree=$3; bad=0
cd "$repo" || exit 2
note() { echo "$*"; }
[ "$(git rev-parse HEAD)" = "$want_head" ] && note "HEAD ok $want_head" || { note "HEAD MISMATCH"; bad=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$want_tree" ] && note "HEAD tree ok" || { note "HEAD tree MISMATCH"; bad=1; }
[ "$(git write-tree)" = "$want_tree" ] && note "index tree ok" || { note "index tree MISMATCH"; bad=1; }
n=0; m=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path")
       fsmode=$([ -x "$path" ] && echo 100755 || echo 100644)
       [ "$fsmode" = "$mode" ] || { note "MODE $path"; m=$((m+1)); }
  fi
  [ "$got" = "$blob" ] || { note "BLOB $path"; m=$((m+1)); }
done < <(git ls-files -s | awk '{print $1" "$2" "$3"\t"$4}')
note "tracked entries checked: $n, mismatches: $m"; [ $m -eq 0 ] || bad=1
st=$(git status --porcelain --ignored=matching --untracked-files=all | grep -v '^!! external/$\|^!! third_party/lwSRP/$')
[ -z "$st" ] && note "superproject status: clean (no untracked/ignored/modified)" || { note "STATUS:"; echo "$st"; bad=1; }
git submodule status | while read -r line; do echo "submodule: $line"; done
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}')
  got=$(git -C "$sm" rev-parse HEAD)
  s=$(git -C "$sm" status --porcelain --ignored=matching --untracked-files=all)
  if [ "$want" = "$got" ] && [ -z "$s" ]; then note "$sm at gitlink $want, clean"
  else note "$sm MISMATCH want=$want got=$got dirty=$(echo -n "$s" | wc -l)"; bad=1; fi
done > "${TMPDIR:-/tmp}/vr_sub.$$"; cat "${TMPDIR:-/tmp}/vr_sub.$$"
grep -q MISMATCH "${TMPDIR:-/tmp}/vr_sub.$$" && bad=1; rm -f "${TMPDIR:-/tmp}/vr_sub.$$"
[ $bad -eq 0 ] && echo "RESULT: RESTORED" || echo "RESULT: NOT RESTORED"
exit $bad
