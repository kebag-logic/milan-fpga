#!/usr/bin/env bash
# Prove the review clone is at the exact head: HEAD/tree ids, no tracked
# modification (content re-hashed, index flags checked), the required
# submodule gitlinks checked out at their pins with no local change.
set -uo pipefail
repo=$1; want_head=$2; want_tree=$3; bad=0
cd "$repo" || exit 2
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$want_head" ] || { echo "HEAD MISMATCH"; bad=1; }
[ "$t" = "$want_tree" ] || { echo "TREE MISMATCH"; bad=1; }
git update-index -q --really-refresh >/dev/null 2>&1
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then echo "tracked changes:"; git status --porcelain --untracked-files=no; bad=1; fi
flags=$(git ls-files -v | grep -v '^H ' | head -5)
[ -z "$flags" ] || { echo "index flags set: $flags"; bad=1; }
# re-hash every tracked regular file against the index blob and mode
mism=$(git ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}' | while read -r mode blob path; do
  got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
  m=$( [ -L "$path" ] && echo 120000 || { [ -x "$path" ] && echo 100755 || echo 100644; } )
  [ "$got" = "$blob" ] && [ "$m" = "$mode" ] || echo "$path"
done | head -5)
[ -z "$mism" ] || { echo "byte/mode mismatch: $mism"; bad=1; }
echo "index blobs == HEAD tree: $(git diff-index --cached --quiet HEAD && echo yes || { echo no; bad=1; })"
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  pin=$(git rev-parse ":$sm"); co=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=no | head -3)
  echo "$sm pin=$pin checkout=$co $( [ "$pin" = "$co" ] && [ -z "$dirty" ] && echo OK || echo BAD)"
  { [ "$pin" = "$co" ] && [ -z "$dirty" ]; } || bad=1
done
echo "verify_clone: $( [ $bad -eq 0 ] && echo CLEAN || echo NOT-CLEAN)"
exit $bad
