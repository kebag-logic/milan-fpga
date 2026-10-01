#!/usr/bin/env bash
# R426-3: compare every Markdown table of the B6 page across commits.
# Usage: table_identity.sh <repo> <commit>...   Tables are runs of lines starting with '|'.
set -u
repo=$1; shift
page=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
for c in "$@"; do
  git -C "$repo" show "$c:$page" > "/tmp/r426-3-tbl-src-$c"
  awk '/^\|/{if(!t){n++;t=1} print n": "$0; next} {t=0}' "/tmp/r426-3-tbl-src-$c" > "/tmp/r426-3-tbl-$c"
  printf '%s tables=%s lines=%s bytes=%s sha256=%s\n' "$c" \
    "$(tail -1 "/tmp/r426-3-tbl-$c" | cut -d: -f1)" "$(wc -l < "/tmp/r426-3-tbl-$c")" \
    "$(cut -d' ' -f2- "/tmp/r426-3-tbl-$c" | wc -c)" "$(sha256sum < "/tmp/r426-3-tbl-$c" | cut -d' ' -f1)"
done
first=$1; rc=0
for c in "$@"; do
  if diff -q "/tmp/r426-3-tbl-$first" "/tmp/r426-3-tbl-$c" >/dev/null; then echo "$c: identical to $first"
  else echo "$c: DIFFERS from $first"; diff "/tmp/r426-3-tbl-$first" "/tmp/r426-3-tbl-$c"; rc=1; fi
done
rm -f /tmp/r426-3-tbl-*
echo "RESULT rc=$rc"; exit $rc
