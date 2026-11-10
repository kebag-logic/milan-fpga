#!/bin/bash
# The head's tests/test_acmp_wide.cpp built against main's src/acmp.c at 33 sinks, without and with sanitizer recovery.
# usage: wide_on_main.sh <packet> <head tree> <main tree> <scratch work dir>
P=$1 H=$2 M=$3 W=$4; . "$P/scripts/env.sh" "$P"
GT=$(pkg-config --cflags gmock gtest); GL=$(pkg-config --libs gmock gtest)
rm -rf "$W"; mkdir -p "$W"; g++ -std=c++20 $GT -c "$H/tests/main.cpp" -o "$W/main.o"
for mode in norecover recover; do
  F="-fsanitize=shift,undefined"; [ $mode = norecover ] && F="$F -fno-sanitize-recover=shift,undefined"
  gcc -std=c11 -O0 -g $F -DACMP_MAX_SINKS=33u -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$M/include" -c "$M/src/acmp.c" -o "$W/a-$mode.o"
  g++ -std=c++20 -O0 -g $F -DACMP_MAX_SINKS=33u $GT -I"$M/include" -I"$H/tests" -c "$H/tests/test_acmp_wide.cpp" -o "$W/t-$mode.o"
  g++ "$W/a-$mode.o" "$W/t-$mode.o" "$W/main.o" $F $GL -o "$W/wide-$mode"
  "$W/wide-$mode" > "$W/$mode.log" 2>&1; echo "== $mode rc=$?"
  grep -E "runtime error|^\[  FAILED  \]|W[012] " "$W/$mode.log" | sed "s|$M/||" | sort -u | head -12
done
