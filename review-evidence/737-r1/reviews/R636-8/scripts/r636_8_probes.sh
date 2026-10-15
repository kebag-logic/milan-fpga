#!/usr/bin/env bash
# R636-8 delta probes for PR #739 (fe2e2a54..30f7b0ef). Read-only on the clone.
# Usage: r636_8_probes.sh <clone-at-30f7b0ef> <scratch-dir> <receipts-dir>
set -u
C=$1; S=$2; R=$3; mkdir -p "$S" "$R"
OLD=fe2e2a543474dd9a932383052bb6fe14bfbbb1fe; NEW=30f7b0ef9d7ab073dccd9bda1130a630aef633b1
DEV=65617779018f41d7e55d1b1ac189ef882bff6367; BASE=fa7347fc59173f90e4feec2df207692e6e6e72ec
MB=f62602531d415d6c1cae1374a3cc2938faf54049; ACT=4f411281417e88660bea1c1a1749aa71ae0bd60f
g() { git -C "$C" "$@"; }
{ g diff --raw $OLD $NEW; g diff $OLD $NEW; } > "$R/p1-delta.txt"
# Each head judged with its own .gitattributes (--attr-source), never the checkout's.
for H in $OLD $NEW; do for B in $DEV $BASE $MB; do
  g --attr-source=$H diff --check $B $H > /dev/null; echo "head=$H base=$B rc=$?"; done; done > "$R/p2-diff-check-rc.txt"
g --attr-source=$OLD diff --check $DEV $OLD | grep -E '^[^+].*:[0-9]+: ' | cut -d: -f1 | sort | uniq -c > "$R/p3-flagged-paths.txt"
g ls-tree -r --name-only $NEW > "$S/paths"
diff <(g --attr-source=$OLD check-attr --stdin whitespace < "$S/paths") \
     <(g --attr-source=$NEW check-attr --stdin whitespace < "$S/paths") > "$R/p4-attr-change.txt"
printf '%s\n' ci/act/new.patch ci/act/sub/x.patch ci/act/x.diff ci/act/x.go ci/x.patch x/ci/act/y.patch CI/act/y.patch ci/act/y.PATCH \
  | g --attr-source=$NEW -c core.ignorecase=false check-attr --stdin whitespace > "$R/p5-glob.txt"
for r in $OLD $NEW; do g cat-file blob $r:ci/act/fail-fast.patch | sha256sum; done > "$R/p6-patch-sha.txt"
curl -sSfL -o "$S/act.tar.gz" https://github.com/nektos/act/archive/$ACT.tar.gz && sha256sum "$S/act.tar.gz" >> "$R/p6-patch-sha.txt"
mkdir -p "$S/x" && tar -xzf "$S/act.tar.gz" -C "$S/x" --no-same-owner --no-same-permissions
g cat-file blob $NEW:ci/act/fail-fast.patch > "$S/fail-fast.patch"
( cd "$S/x/act-$ACT" && patch --dry-run --batch --fuzz=0 -p1 -i "$S/fail-fast.patch"; echo "dry-run rc=$?" ) > "$R/p7-dry-run.txt" 2>&1
cat "$R"/p2-diff-check-rc.txt "$R"/p3-flagged-paths.txt "$R"/p4-attr-change.txt "$R"/p6-patch-sha.txt "$R"/p7-dry-run.txt
