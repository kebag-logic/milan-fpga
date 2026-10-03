#!/usr/bin/env bash
# Compare a C++ file's comment-stripped token stream at two commits, plus a one-token control.
# usage: strip_compare.sh <repo> <base> <head> <path> <outdir>
set -u
repo=$1 base=$2 head=$3 f=$4 out=$5
mkdir -p "$out"
strip() { g++ -fpreprocessed -dD -E -P -x c++ - 2>/dev/null | tr -s ' \t\n' ' '; }
git -C "$repo" show "$base:$f" | strip > "$out/base.stripped"
git -C "$repo" show "$head:$f" | strip > "$out/head.stripped"
sha256sum "$out/base.stripped" "$out/head.stripped"
if cmp -s "$out/base.stripped" "$out/head.stripped"; then echo "STRIPPED IDENTICAL"; else echo "STRIPPED DIFFER"; fi
# control: change one token on the edited banner's following code line, must differ
git -C "$repo" show "$head:$f" | sed '0,/const uint64_t one = row(0, 3, 3);/s//const uint64_t one = row(0, 3, 4);/' | strip > "$out/control.stripped"
if cmp -s "$out/base.stripped" "$out/control.stripped"; then echo "CONTROL NOT CAUGHT"; else echo "CONTROL CAUGHT"; fi
