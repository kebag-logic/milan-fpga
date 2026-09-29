#!/bin/bash
# Compile-probe sim_ax1x1gptp.cpp:55-81 (clock constants, #error, static_assert)
# at several MILAN_CLK_HZ_TB values. usage: harness_clock_guard.sh <clone> <workdir>
C=$1; W=$2
sed -n 55,81p "$C/tb/verilator/milan_dp/sim_ax1x1gptp.cpp" > "$W/clock_guard_excerpt.inc"
for d in "" -DMILAN_CLK_HZ_TB=50000000 -DMILAN_CLK_HZ_TB=100000000 -DMILAN_CLK_HZ_TB=50000001 -DMILAN_CLK_HZ_TB=62500000; do
  printf '#include <cstdint>\n#include "%s"\n}\nint main(){return (int)(kPeriodNs + kAafPeriod + kDelayBoundNs) & 0;}\n' "$W/clock_guard_excerpt.inc" > "$W/cg.cpp"
  out=$(g++ -std=c++17 -fsyntax-only $d "$W/cg.cpp" 2>&1); rc=$?
  echo "=== g++ ${d:-<no define>}: rc=$rc $(echo "$out" | grep -E 'error' | head -1 | sed 's|.*error: ||')"
done
