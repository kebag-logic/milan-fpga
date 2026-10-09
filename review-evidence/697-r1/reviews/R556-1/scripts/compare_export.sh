#!/bin/sh
# Usage: compare_export.sh <export-clone> <source-bare-repo> <source-rev> <export-rev>
# Diffs each exported file against its source blob; prints the diff hunks.
set -u
EXP=$1; SRC=$2; SREV=$3; EREV=$4
map='sw/firmware/ctrl/adp/adp.c src/adp.c
sw/firmware/ctrl/adp/adp.h include/adp.h
sw/firmware/ctrl/acmp/acmp.c src/acmp.c
sw/firmware/ctrl/acmp/acmp.h include/acmp.h
sw/firmware/ctrl/maap/maap.c src/maap.c
sw/firmware/ctrl/maap/maap.h include/maap.h
sw/firmware/ctrl/wire/wire.h include/wire.h
sw/firmware/ctrl/test/test_adp.cpp tests/test_adp.cpp
sw/firmware/ctrl/test/test_adp_reentry.cpp tests/test_adp_reentry.cpp
sw/firmware/ctrl/test/test_acmp.cpp tests/test_acmp.cpp
sw/firmware/ctrl/test/acmp_fake.hpp tests/acmp_fake.hpp
sw/firmware/ctrl/test/test_maap.cpp tests/test_maap.cpp
sw/firmware/ctrl/test/test_maap_debug.cpp tests/test_maap_debug.cpp'
T=$(mktemp -d)
echo "$map" | while read -r o n; do
  git -C "$SRC" show "$SREV:$o" > "$T/o" 2>/dev/null || { echo "MISSING-SOURCE $o"; continue; }
  git -C "$EXP" show "$EREV:$n" > "$T/n"
  so=$(sha256sum < "$T/o" | cut -c1-16); sn=$(sha256sum < "$T/n" | cut -c1-16)
  nd=$(diff "$T/o" "$T/n" | grep -c '^[<>]')
  echo "== $o -> $n src=$so exp=$sn changed_lines=$nd"
  diff "$T/o" "$T/n" | head -${MAXDIFF:-12}
done
rm -rf "$T"
