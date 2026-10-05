#!/bin/sh
# C11 merge check: the RTL and bench files C11 changes, preprocessed with comments
# stripped, at e3c9f0b5 (lane before merge) vs 7957100 (head), and at 054d01c7 vs 21c6f709.
# Usage: c11_comment_only.sh REPO SCRATCH VERILATOR
set -u
R=$1 S=$2 V=$3
mkdir -p "$S/c11"
git -C "$R" diff --name-only 054d01c79e59c3f80454ad9cdefd8e914b540bb4 21c6f709 -- hdl tb | while read f; do
  for pair in "e3c9f0b 79571006b803a4ab4af65358f0d87bc3af73180e" "054d01c79e59c3f80454ad9cdefd8e914b540bb4 21c6f709"; do
    set -- $pair
    for r in $1 $2; do git -C "$R" show "$r:$f" > "$S/c11/$(echo $r|cut -c1-7)-$(basename $f)"; done
    a="$S/c11/$(echo $1|cut -c1-7)-$(basename $f)"; b="$S/c11/$(echo $2|cut -c1-7)-$(basename $f)"
    case $f in
      *.sv) "$V" -E -P "$a" > "$a.pp" 2>/dev/null; "$V" -E -P "$b" > "$b.pp" 2>/dev/null ;;
      *) gcc -fpreprocessed -dD -E -P -x c++ "$a" > "$a.pp" 2>/dev/null; gcc -fpreprocessed -dD -E -P -x c++ "$b" > "$b.pp" 2>/dev/null ;;
    esac
    if cmp -s "$a.pp" "$b.pp"; then res=IDENTICAL; else res=DIFFERS; fi
    echo "$f $(echo $1|cut -c1-7)..$(echo $2|cut -c1-7): comment-stripped $res; lines $(wc -l < $a) -> $(wc -l < $b); pp-bytes $(wc -c < $a.pp)"
  done
done
