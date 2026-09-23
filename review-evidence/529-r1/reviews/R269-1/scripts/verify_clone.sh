#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Verify that the review clone still holds the exact published head: HEAD, tree,
# index records, tracked blob bytes and modes, no untracked or ignored residue,
# and the three required submodule gitlinks checked out clean at their pins.
#
# usage: verify_clone.sh <clone> <expected head> <expected tree>
set -uo pipefail
clone=$1; want_head=$2; want_tree=$3
cd "$clone" || exit 2
rc=0
say() { printf '%s\n' "$*"; }
chk() { if [ "$2" = "$3" ]; then say "OK   $1: $2"; else say "FAIL $1: got $2 want $3"; rc=1; fi; }
chk HEAD "$(git rev-parse HEAD)" "$want_head"
chk tree "$(git rev-parse 'HEAD^{tree}')" "$want_tree"
# index == HEAD tree, record for record (mode, object, stage 0, path)
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
tre=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
chk "index records == HEAD tree records (sha256)" "$idx" "$tre"
# every tracked regular file / symlink hashes to its recorded blob, with its mode
bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
    if [ -x "$path" ]; then fm=100755; else fm=100644; fi
    [ "$fm" = "$mode" ] || { say "FAIL mode $path $fm != $mode"; bad=$((bad+1)); }
  fi
  [ "$got" = "$oid" ] || { say "FAIL bytes $path"; bad=$((bad+1)); }
done < <(git ls-tree -r HEAD)
chk "tracked blob byte/mode mismatches" "$bad" 0
chk "untracked or ignored residue (git status --ignored)" \
    "$(git status --porcelain --ignored --ignore-submodules=none | wc -l)" 0
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  pin=$(git ls-tree HEAD "$sm" | awk '{print $1, $3}')
  co=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  chk "gitlink $sm (mode, pin)" "$pin" "160000 $co"
  chk "submodule $sm worktree clean" \
      "$(git -C "$sm" status --porcelain --ignored | wc -l)" 0
done
say "verify_clone exit $rc"
exit $rc
