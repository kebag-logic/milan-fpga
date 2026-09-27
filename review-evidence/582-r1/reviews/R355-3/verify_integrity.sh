#!/usr/bin/env bash
# Verify that the review clone is at the exact head with pristine tracked
# bytes, modes, index and submodule gitlinks after all gates and probes.
# Usage: verify_integrity.sh <clone>
set -u
cd "$1" || exit 2
head=1304205cfc9fa4c9e69a32130fb366895c5f883b
tree=28c36c12cf459020de252185dbdb14ea508724d2
fail=0
check() { if "$@"; then echo "ok   $*"; else echo "FAIL $*"; fail=1; fi; }
check test "$(git rev-parse HEAD)" = "$head"
check test "$(git rev-parse 'HEAD^{tree}')" = "$tree"
check test "$(git write-tree)" = "$tree"
check git diff --quiet HEAD --
check git diff --cached --quiet HEAD --
check test -z "$(git status --porcelain --ignored)"
# Index entries (mode, blob, path) equal the head tree, including gitlinks.
check test "$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum)" = \
           "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum)"
# Worktree bytes of every tracked regular file equal the head blobs.
mism=$(git ls-tree -r HEAD | awk '$2 == "blob" {print $3" "$4}' |
    while read -r blob path; do
        [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || echo "$path"
    done | wc -l)
check test "$mism" -eq 0
# Required submodule gitlinks are checked out at the recorded pins.
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
    pin=$(git ls-tree HEAD "$sub" | awk '{print $3}')
    check test "$(git -C "$sub" rev-parse HEAD)" = "$pin"
    check test -z "$(git -C "$sub" status --porcelain)"
done
git submodule status 2>/dev/null
echo "integrity: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
exit $fail
