#!/bin/sh
# Verify that the review clone's tracked state is exactly the reviewed head:
# HEAD commit and tree, index entries (mode, blob, stage 0) equal to the HEAD
# tree, every tracked worktree file hashing to its index blob with the index
# mode, and the required submodule gitlinks checked out at their pins.
# Usage: verify_clone_integrity.sh <repo> <expected-head> <expected-tree>
set -u
cd "$1"
fail=0
say() { echo "$*"; }
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
[ "$h" = "$2" ] && say "OK head $h" || { say "BAD head $h"; fail=1; }
[ "$t" = "$3" ] && say "OK tree $t" || { say "BAD tree $t"; fail=1; }
# index == HEAD tree (mode, object, path), all stage 0
git ls-files -s | awk '{print $1, $2, $4; if ($3 != 0) bad=1} END {exit bad}' > /tmp/idx.$$ \
  && say "OK all index entries stage 0" || { say "BAD unmerged index entries"; fail=1; }
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' > /tmp/tree.$$
cmp -s /tmp/idx.$$ /tmp/tree.$$ && say "OK index equals HEAD tree ($(wc -l < /tmp/tree.$$) entries)" \
  || { say "BAD index differs from HEAD tree"; fail=1; }
# worktree bytes and modes equal index for every non-gitlink entry
n=0; bad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$blob" ] || echo "MISMATCH $path"
  else
    [ -f "$path" ] && [ ! -L "$path" ] && [ "$(git hash-object --no-filters "$path")" = "$blob" ] || { echo "MISMATCH $path"; continue; }
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || echo "MODE $path"; else [ -x "$path" ] && echo "MODE $path"; fi
  fi
done > /tmp/wt.$$
[ -s /tmp/wt.$$ ] && { say "BAD worktree:"; cat /tmp/wt.$$; fail=1; } || say "OK every tracked file hashes to its blob with its mode"
# hidden-change flags
git ls-files -v | grep -E '^[a-z]|^S ' > /tmp/flags.$$ && { say "BAD assume-unchanged/skip-worktree flags"; head /tmp/flags.$$; fail=1; } || say "OK no assume-unchanged or skip-worktree flags"
# submodule gitlinks
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  pin=$(git ls-tree HEAD "$sm" | awk '{print $3}')
  cur=$(git -C "$sm" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=no 2>/dev/null | wc -l)
  [ "$pin" = "$cur" ] && [ "$dirty" = 0 ] && say "OK $sm at $pin, clean" || { say "BAD $sm pin=$pin cur=$cur dirty=$dirty"; fail=1; }
done
say "submodule status:"; git submodule status
rm -f /tmp/idx.$$ /tmp/tree.$$ /tmp/wt.$$ /tmp/flags.$$
[ $fail = 0 ] && say "RESULT PASS" || say "RESULT FAIL"
exit $fail
