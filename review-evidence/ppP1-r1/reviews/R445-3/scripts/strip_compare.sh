#!/bin/sh
# Usage: strip_compare.sh <repo> <base-rev> <head-rev> <path> <workdir>
# Compares the comment-stripped, whitespace-collapsed token stream of <path> at two revisions
# (g++ -fpreprocessed: comments removed, no macro expansion), then runs a one-token control
# (a "+ 0" on a code line of the head copy) that must be caught.
set -eu
repo=$1 base=$2 head=$3 path=$4 wd=$5
mkdir -p "$wd"
git -C "$repo" show "$base:$path" > "$wd/base.cpp"
git -C "$repo" show "$head:$path" > "$wd/head.cpp"
strip() { g++ -fpreprocessed -dD -E -P -x c++ "$1" 2>/dev/null | tr -s ' \n\t' ' '; }
strip "$wd/base.cpp" > "$wd/base.tok"; strip "$wd/head.cpp" > "$wd/head.tok"
sha256sum "$wd/base.tok" "$wd/head.tok" | sed "s|$wd/||"
if cmp -s "$wd/base.tok" "$wd/head.tok"; then echo "STRIPPED: IDENTICAL"; else echo "STRIPPED: DIFFERENT"; fi
sed 's/const uint64_t m0 = h.nvm_marks;/const uint64_t m0 = h.nvm_marks + 0;/' "$wd/head.cpp" > "$wd/ctl.cpp"
cmp -s "$wd/head.cpp" "$wd/ctl.cpp" && { echo "CONTROL: NOT PLANTED"; exit 1; }
strip "$wd/ctl.cpp" > "$wd/ctl.tok"
if cmp -s "$wd/head.tok" "$wd/ctl.tok"; then echo "CONTROL: MISSED"; exit 1; else echo "CONTROL: CAUGHT"; fi
