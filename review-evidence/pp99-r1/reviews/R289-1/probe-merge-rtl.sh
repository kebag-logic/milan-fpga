#!/usr/bin/env bash
# Verify the PR's own delta touches no RTL/testbench/synthesis file, the top's
# parameter header is byte-identical to the base, and the merge commit equals a
# clean replay of its two parents. Runs the replay in a disposable clone.
# Usage: probe-merge-rtl.sh <clone-dir> <scratch-dir>
set -u
c="$1"; s="$2"; base=008edbbf486598ae237414273d75e385cf0e1a56; main=60152f3ff068b81333326b5081b5303253ba7fe7
cd "$c"
echo "== PR-own delta (merged main..HEAD), name-status"; git diff --name-status $main HEAD
echo "== PR-own delta under hdl/ tb/ syn/ (expect empty)"; git diff --stat $main HEAD -- hdl tb syn; echo "(end)"
echo "== 52659df vs base under hdl/ tb/ syn/ (expect empty)"; git diff --stat $base 52659df -- hdl tb syn; echo "(end)"
hdr() { git show "$1:hdl/top/protocol_processor_top.sv" | sed -n '/^module protocol_processor_top/,/^) (/p' | sha256sum; }
echo "== top parameter header sha256: base $(hdr $base)"; echo "   main $(hdr $main)"; echo "   head $(hdr HEAD)"
echo "== top file blob: main $(git rev-parse $main:hdl/top/protocol_processor_top.sv) head $(git rev-parse HEAD:hdl/top/protocol_processor_top.sv)"
echo "== workflow delta (merged main..HEAD)"; git diff $main HEAD -- .github
r="$s/replay"; rm -rf "$r"; git clone -q --no-checkout "$c" "$r"
cd "$r"; git -c user.name=replay -c user.email=replay@invalid checkout -q --detach 52659df
git -c user.name=replay -c user.email=replay@invalid merge -q --no-edit $main >/dev/null 2>&1; echo "replay merge rc=$?"
echo "replayed tree $(git rev-parse 'HEAD^{tree}')  recorded merge tree $(git -C "$c" rev-parse '9cfe2d3^{tree}')"
echo "== recorded merge vs replay (expect empty)"; git diff --stat HEAD 9cfe2d381951467f48d64b75a041bd464ca57e12; echo "(end)"
echo "== 663d50d vs merge (expect checker docstrings only)"; git -C "$c" diff --stat 9cfe2d3 663d50d
