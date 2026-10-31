#!/bin/sh
# Usage: delta_checks.sh <clone>  -- read-only checks of the R732-5 delta.
set -u
cd "$1" || exit 2
H=86a349d5399d8abc40b819d09806fc8245682609 OLD=cbc7c6043ebf84d5bcd74652dc0a7131b7d54271 DEV=8adf5c990bad73e80852e9c1df95163792a0deb2
fail=0; chk() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1: got [$2] want [$3]"; fail=1; fi; }
chk tree-identity "$(git rev-parse $OLD^{tree})" "$(git rev-parse $H^{tree})"
chk parents "$(git rev-parse $H^1 $H^2 | tr '\n' ' ')" "$OLD $DEV "
chk one-merge-base "$(git merge-base --all $DEV $H | tr '\n' ' ')" "$DEV "
chk old-had-two-bases "$(git merge-base --all $DEV $OLD | wc -l | tr -d ' ')" 2
chk merge-is-auto-merge "$(git merge-tree --write-tree $OLD $DEV)" "$(git rev-parse $H^{tree})"
chk dev-candidate-tree "$(git merge-tree --write-tree $DEV $H)" "$(git rev-parse $H^{tree})"
chk new-commits "$(git rev-list $OLD..$H | wc -l | tr -d ' ')" 2
chk message-lines "$(git log -1 --format=%B $H | grep -c .)" 1
chk no-trailers "$(git log -1 --format=%B $H | grep -ciE '^[A-Za-z-]+: ')" 0
chk gitlinks "$(git ls-tree -r $OLD | awk '$1=="160000"' | sha256sum)" "$(git ls-tree -r $H | awk '$1=="160000"' | sha256sum)"
git diff --check $DEV $H >/dev/null; chk diff-check-vs-dev "$?" 0
exit $fail
