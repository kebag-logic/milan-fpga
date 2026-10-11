#!/bin/sh
# verify_clean.sh REPO HEAD_SHA TREE_SHA
# Verifies that REPO is at HEAD_SHA/TREE_SHA, that the index equals HEAD, that
# every tracked file's bytes and mode equal its index entry, that there are no
# untracked, unignored files, and that each initialised submodule sits at its
# gitlink with a clean worktree.
REPO=$1; HEAD_SHA=$2; TREE_SHA=$3
cd "$REPO" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$HEAD_SHA" ] || { echo "HEAD mismatch"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$TREE_SHA" ] || { echo "tree mismatch"; fail=1; }
git update-index -q --really-refresh >/dev/null 2>&1
git diff-index --cached --quiet HEAD -- || { echo "index differs from HEAD"; fail=1; }
git diff-files --quiet || { echo "worktree differs from index (bytes or mode)"; fail=1; }
n=0; bad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else got=$(git hash-object "$path"); fi
  [ "$got" = "$blob" ] || echo "BLOB MISMATCH $path"
done > /tmp/verify_clean.$$ 2>&1
if [ -s /tmp/verify_clean.$$ ]; then cat /tmp/verify_clean.$$; fail=1; fi
rm -f /tmp/verify_clean.$$
echo "tracked files hashed: $(git ls-files -s | grep -vc '^160000')"
u=$(git ls-files --others --exclude-standard | head -5)
[ -z "$u" ] || { echo "untracked: $u"; fail=1; }
git submodule status
for sm in $(git config -f .gitmodules --get-regexp path | awk '{print $2}'); do
  [ -e "$sm/.git" ] || { echo "$sm: not initialised"; continue; }
  want=$(git rev-parse "HEAD:$sm"); got=$(git -C "$sm" rev-parse HEAD)
  [ "$want" = "$got" ] || { echo "$sm: gitlink $want but checked out $got"; fail=1; }
  [ -z "$(git -C "$sm" status --porcelain)" ] || { echo "$sm: dirty"; git -C "$sm" status --porcelain | head; fail=1; }
done
echo "verify_clean: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
