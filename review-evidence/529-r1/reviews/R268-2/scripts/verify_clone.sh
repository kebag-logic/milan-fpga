#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Verify a review clone is exactly the reviewed head: HEAD and tree ids, index
# records equal to the HEAD tree records, every tracked regular file's bytes
# and mode equal to its blob, no untracked or ignored residue, and the three
# required gitlinks at mode 160000, at their pins, with clean worktrees.
# usage: verify_clone.sh <clone> <expected head> <expected tree>
set -u
c=$1; want_head=$2; want_tree=$3
cd "$c" || exit 2
bad=0
say() { echo "$1"; }
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
say "HEAD $h $( [ "$h" = "$want_head" ] && echo OK || { bad=1; echo MISMATCH; })"
say "tree $t $( [ "$t" = "$want_tree" ] && echo OK || { bad=1; echo MISMATCH; })"
if diff <(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}') \
        <(git ls-files -s | awk '{print $1, $2, $4}') >/dev/null; then
  say "index records == HEAD tree records: OK"
else
  say "index records differ from HEAD tree: MISMATCH"; bad=1
fi
n=0; mm=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest##* }
  [ "$type" = blob ] || continue
  n=$((n + 1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)" = "$oid" ] || { mm=$((mm + 1)); echo "  symlink mismatch: $path"; }
    continue
  fi
  if [ ! -f "$path" ] || [ -L "$path" ]; then mm=$((mm + 1)); echo "  missing: $path"; continue; fi
  [ "$(git hash-object --no-filters "$path")" = "$oid" ] || { mm=$((mm + 1)); echo "  bytes differ: $path"; }
  x=100644; [ -x "$path" ] && x=100755
  [ "$x" = "$mode" ] || { mm=$((mm + 1)); echo "  mode differs: $path"; }
done < <(git ls-tree -r --full-tree HEAD)
say "tracked blobs checked: $n, byte/mode mismatches: $mm"
[ "$mm" -eq 0 ] || bad=1
res=$(git status --porcelain --ignored --untracked-files=all --ignore-submodules=none | grep -v '^!! external/$' || true)
if [ -z "$res" ]; then say "untracked/ignored/modified residue: none"; else say "residue:"; echo "$res" | head -20; bad=1; fi
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  rec=$(git ls-tree HEAD "$sm"); mode=${rec%% *}; pin=$(echo "$rec" | awk '{print $3}')
  cur=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=all 2>/dev/null | wc -l)
  ok=OK; { [ "$mode" = 160000 ] && [ "$cur" = "$pin" ] && [ "$dirty" -eq 0 ]; } || { ok=MISMATCH; bad=1; }
  say "gitlink $sm mode=$mode pin=$pin checkout=$cur dirty_entries=$dirty $ok"
done
say "VERDICT $( [ "$bad" -eq 0 ] && echo CLEAN || echo NOT-CLEAN)"
exit "$bad"
