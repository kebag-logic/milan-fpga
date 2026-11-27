#!/bin/bash
# spot_runs.sh <repo> <cgreen-prefix> <work> <receipts>
# Concurrent spot checks: unit builds (default, end-station with and without the
# scale options, one-port alone; both profiles where named), the end-station
# reversals, and the MRP/timer differential in both profiles.
set -u
repo=$1; cg=$2; work=$3; out=$4
mkdir -p "$work" "$out"
export LD_LIBRARY_PATH="$cg/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
ES="-DLWSRP_ONE_PORT_MAP=1 -DLWSRP_LEAN_VALIDATE=1 -DLWSRP_RAPID_REPLACE=1 -DLWSRP_LEAN_COPY=1 -DLWSRP_LEAN_TX=1"
unit() { # label milan scale cflags
  local l=$1 b="$work/unit-$1"
  {
    cmake -S "$repo" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$cg" -DLWSRP_MILAN="$2" -DLWSRP_SCALE="$3" \
      -DCMAKE_C_FLAGS="$4" && cmake --build "$b" --parallel 2 && ctest --test-dir "$b" --output-on-failure && "$b/unit_tests"
  } > "$out/unit-$l.log" 2>&1
  echo "rc=$?" >> "$out/unit-$l.log"
}
unit default-OFF OFF OFF "" &
unit default-ON ON OFF "" &
unit es-scale-OFF OFF ON "$ES" &
unit es-scale-ON ON ON "$ES" &
unit es-noscale-OFF OFF OFF "$ES" &
unit oneport-OFF OFF OFF "-DLWSRP_ONE_PORT_MAP=1" &
unit leantx-ON ON OFF "-DLWSRP_LEAN_TX=1" &
( cd "$repo" && python3 -I tests/check_reversals.py --work-dir "$work/rev-es-OFF" --prefix "$cg" --scale ON --end-station ON > "$out/rev-es-scale-OFF.log" 2>&1; echo "rc=$?" >> "$out/rev-es-scale-OFF.log"; cp "$work/rev-es-OFF/summary.json" "$out/rev-es-scale-OFF.summary.json" 2>/dev/null ) &
( cd "$repo" && python3 -I tests/check_reversals.py --work-dir "$work/rev-es-ON" --prefix "$cg" --milan ON --end-station ON > "$out/rev-es-noscale-ON.log" 2>&1; echo "rc=$?" >> "$out/rev-es-noscale-ON.log"; cp "$work/rev-es-ON/summary.json" "$out/rev-es-noscale-ON.summary.json" 2>/dev/null ) &
( cd "$repo" && python3 -I tests/check_differential.py --work-dir "$work/diff-OFF" > "$out/diff-OFF.log" 2>&1; echo "rc=$?" >> "$out/diff-OFF.log" ) &
( cd "$repo" && python3 -I tests/check_differential.py --work-dir "$work/diff-ON" --milan ON > "$out/diff-ON.log" 2>&1; echo "rc=$?" >> "$out/diff-ON.log" ) &
wait
echo "spot runs finished"
