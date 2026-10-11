#!/bin/sh
# Usage: verify_merge.sh <clone>
# Recomputes the plain merge of PR #80's pre-merge head and main, and
# compares it with the published merge commit. Prints only raw git output.
set -eu
C=${1:?clone}
HEAD_C=49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c
PRE=a70e38804cb16435c089d024c58e8c3fb4d39ff6
MAIN=155de13789ac85bab7a14bea0ae86d1c376b490a
BASE=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
g() { git -C "$C" --no-pager "$@"; }
echo "== identity"
g rev-parse "$HEAD_C^{tree}" "$HEAD_C^1" "$HEAD_C^2"
echo "== merge-base (expect $BASE)"
g merge-base "$PRE" "$MAIN"
echo "== plain merge (merge-tree, conflicts expected)"
T=$(g merge-tree --write-tree --name-only "$PRE" "$MAIN" | head -1) || true
g merge-tree --write-tree --name-only "$PRE" "$MAIN" || true
echo "== files differing: plain merge tree vs published head"
g diff --name-status "$T" "$HEAD_C"
echo "== published head vs plain merge (full)"
g diff "$T" "$HEAD_C"
echo "== parser RTL, parser tests, every hdl/ and tb/ path: pre-merge head vs published head (expect empty)"
g diff --stat "$PRE" "$HEAD_C" -- hdl tb bench scripts
echo "== tree ids of hdl tb bench scripts at pre and head"
for p in hdl tb bench scripts; do echo "$p $(g rev-parse "$PRE:$p") $(g rev-parse "$HEAD_C:$p")"; done
echo "== published head vs main (the PR's net change)"
g diff --stat "$MAIN" "$HEAD_C"
echo "== README.md and docs/MANAGER.md: head vs main"
g diff "$MAIN" "$HEAD_C" -- README.md docs/MANAGER.md
echo "== main-side changes vs pre-merge head equal main vs base on every main-touched path?"
for f in $(g diff --name-only "$BASE" "$MAIN"); do
  a=$(g rev-parse "$MAIN:$f" 2>/dev/null || echo none)
  b=$(g rev-parse "$HEAD_C:$f" 2>/dev/null || echo none)
  [ "$a" = "$b" ] && s=same-as-main || s=DIFFERS-from-main
  echo "$f $s"
done
echo "== branch-touched paths: head vs pre-merge head"
for f in $(g diff --name-only "$BASE" "$PRE"); do
  a=$(g rev-parse "$PRE:$f" 2>/dev/null || echo none)
  b=$(g rev-parse "$HEAD_C:$f" 2>/dev/null || echo none)
  [ "$a" = "$b" ] && s=same-as-pre || s=DIFFERS-from-pre
  echo "$f $s"
done
