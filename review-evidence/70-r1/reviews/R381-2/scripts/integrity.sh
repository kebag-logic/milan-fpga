#!/usr/bin/env bash
# Verify the review clone is byte-identical to the exact head. Usage: integrity.sh <clone>
set -u; C="$1"; H=e796c68a460fe6946e28cb9da0349a382c868352; T=2bbb410b9af6b0f8513e2693e4726a1c3bde4205
cd "$C" || exit 2; rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree}); echo "HEAD $h"; echo "tree $t"
[ "$h" = "$H" ] && [ "$t" = "$T" ] || { echo "HEAD/tree MISMATCH"; rc=1; }
a=$(git ls-files -s | sha256sum | cut -d' ' -f1); b=$(git ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum | cut -d' ' -f1)
echo "index(mode blob stage path) sha256 $a"; echo "HEAD tree  (mode blob 0 path)  sha256 $b"; [ "$a" = "$b" ] || { echo "INDEX != HEAD"; rc=1; }
p=$(git status --porcelain --ignore-submodules=none | wc -l); echo "porcelain entries $p"; [ "$p" -eq 0 ] || { git status --porcelain; rc=1; }
git diff --quiet HEAD && echo "worktree == HEAD for tracked files" || { echo "WORKTREE DIFF"; rc=1; }
echo "gitlinks at HEAD:"; git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
echo "submodule status:"; git submodule status
[ "$(git -C protocol-processor rev-parse HEAD)" = 16be6768f710e79450aace277abacd6c2c3336e5 ] || rc=1
p2=$(git -C protocol-processor status --porcelain | wc -l); echo "protocol-processor porcelain entries $p2"; [ "$p2" -eq 0 ] || rc=1
echo "integrity rc $rc"; exit $rc
