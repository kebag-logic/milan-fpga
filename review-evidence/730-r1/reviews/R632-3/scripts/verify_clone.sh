#!/usr/bin/env bash
# Prove the review clone still holds the exact head: HEAD, tree, a clean index
# and work tree, every tracked blob's bytes and mode, and the submodule gitlinks.
# Usage: verify_clone.sh CLONE HEAD TREE
set -u
C=$1; H=$2; T=$3; rc=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD $H OK" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree $T OK" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$T" ] && echo "index writes tree $T OK" || { echo "INDEX MISMATCH"; rc=1; }
s=$(git status --porcelain=v1 --untracked-files=all --ignore-submodules=none); [ -z "$s" ] && echo "status clean OK" || { echo "STATUS DIRTY: $s"; rc=1; }
git diff --quiet HEAD -- && echo "tracked bytes/modes match HEAD OK" || { echo "TRACKED DIFF"; rc=1; }
git ls-files -s | awk '$1=="160000"' | while read -r mode sha stage path; do echo "gitlink $path $sha"; done
git ls-tree -r HEAD | awk '$2=="commit"{print "head-gitlink " $4 " " $3}'
echo "act_ci.py blob $(git rev-parse HEAD:scripts/act_ci.py) sha256 $(sha256sum scripts/act_ci.py | cut -d' ' -f1)"
exit $rc
