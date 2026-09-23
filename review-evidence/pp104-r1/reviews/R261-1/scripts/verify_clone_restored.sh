#!/bin/sh
# Verify the review clone still holds the exact published head, byte for byte.
# Usage: verify_clone_restored.sh <clone> <expected-head> <expected-tree>
set -u
C=$1; HEAD_EXP=$2; TREE_EXP=$3
cd "$C" || exit 2
fail=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $h $( [ "$h" = "$HEAD_EXP" ] && echo OK || { fail=1; echo MISMATCH; } )"
echo "tree $t $( [ "$t" = "$TREE_EXP" ] && echo OK || { fail=1; echo MISMATCH; } )"
echo "detached: $(git symbolic-ref -q HEAD >/dev/null && echo NO || echo yes)"
if git diff-index --cached --quiet HEAD --; then echo "index == HEAD tree: OK"; else echo "index == HEAD tree: MISMATCH"; fail=1; fi
if git diff-files --quiet; then echo "worktree tracked bytes/modes == index: OK"; else echo "worktree tracked bytes/modes == index: MISMATCH"; fail=1; fi
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -c1-64)
tree=$(git ls-tree -r HEAD | awk '{split($0,a,"\t"); split(a[1],b," "); print b[1], b[3], a[2]}' | sha256sum | cut -c1-64)
echo "ls-files -s digest $idx vs ls-tree -r digest $tree: $( [ "$idx" = "$tree" ] && echo OK || { fail=1; echo MISMATCH; } )"
n=$(git ls-files | wc -l); echo "tracked entries: $n"
# re-hash every tracked regular file from disk and compare with the HEAD blob id
bad=$(git ls-tree -r HEAD | awk '$1 != "160000" {split($0,a,"\t"); print $3 "\t" a[2]}' | while IFS="$(printf '\t')" read -r blob path; do
    [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || echo "$path"; done)
if [ -z "$bad" ]; then echo "every tracked blob re-hashed from disk == HEAD: OK"; else echo "blob mismatch: $bad"; fail=1; fi
links=$(git ls-files -s | awk '$1 == "160000"')
echo "gitlinks in this repository: ${links:-none}"
st=$(git status --porcelain --ignored --untracked-files=all)
echo "status (incl. ignored/untracked): ${st:-clean}"
[ -z "$st" ] || fail=1
echo "CLONE RESTORED: $( [ $fail -eq 0 ] && echo PASS || echo FAIL)"
exit $fail
