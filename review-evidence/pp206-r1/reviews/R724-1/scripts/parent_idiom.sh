#!/usr/bin/env bash
# Reviewer-run parent idiom gates for issue #206 at one processor gitlink.
# usage: parent_idiom.sh <parent worktree> <processor commit> <out dir>
# The worktree is milan-fpga dev 97aab1d0 with the #202 source-stream-ID
# wiring patch (sha256 ff5068d2...1275) applied and staged; protocol-processor
# and gptp-processor are populated, initialised clones. This script moves the
# protocol-processor clone and the staged gitlink to <processor commit>, then
# runs each gate and records its own exit status.
set -u
wt=$1; rev=$2; out=$3
mkdir -p "$out"
cd "$wt" || exit 2
git -C protocol-processor checkout -q --detach "$rev" || exit 2
git update-index --cacheinfo "160000,$rev,protocol-processor" || exit 2
{
  echo "parent HEAD $(git rev-parse HEAD)"
  echo "staged diff sha256 $(git diff --cached -- . ':!protocol-processor' | sha256sum | cut -c1-64)"
  git ls-files -s protocol-processor gptp-processor
  git submodule status -- protocol-processor gptp-processor
} > "$out/STATE.txt" 2>&1
i=0
for cmd in "python3 scripts/check_py_idiom.py" \
           "python3 scripts/check_py_idiom.py --selftest" \
           "python3 scripts/check_py_idiom.py --list" \
           "python3 scripts/check_cpp_idiom.py" \
           "python3 scripts/check_cpp_idiom.py --selftest"; do
  i=$((i + 1))
  echo "$cmd" > "$out/$i.cmd"
  $cmd > "$out/$i.log" 2>&1
  echo $? > "$out/$i.rc"
  echo "$i rc=$(cat "$out/$i.rc") $cmd: $(grep -E 'long function|FAIL|PASS|OK|ratchet' "$out/$i.log" | head -2 | tr '\n' ' ')"
done
