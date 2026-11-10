#!/bin/sh
# Usage: compare_sides.sh <repo> <out-dir>
# Compares each merge side's patch against the same patch on its original base,
# ignoring index lines and hunk-header line offsets.
set -u
repo=$1; out=$(cd "$2" && pwd)
norm() { sed -E -e '/^index [0-9a-f]+\.\.[0-9a-f]+/d' -e 's/^@@ -[0-9,]+ \+[0-9,]+ @@/@@/'; }
cd "$repo" || exit 2
git diff 45f03e04 14492f87 | norm > "$out/n219_main"; git diff 044cb25f fd2d8d2 | norm > "$out/n219_base"
git diff fd2d8d2 14492f87 | norm > "$out/n218_pr";  git diff 044cb25f 45f03e04 | norm > "$out/n218_base"
r=0
echo "== PR219 side: diff(45f03e04,14492f87) vs diff(044cb25f,fd2d8d2)"; diff "$out/n219_base" "$out/n219_main" && echo IDENTICAL || r=1
echo "== PR218 side: diff(fd2d8d2,14492f87) vs diff(044cb25f,45f03e04)"; diff "$out/n218_base" "$out/n218_pr" && echo IDENTICAL || r=1
echo "== commits on the PR side of the merge (first parent ^1) since base"; git log --format="%H %s" 044cb25f..14492f87^1
exit $r
