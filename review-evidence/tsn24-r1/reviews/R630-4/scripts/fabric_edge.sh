#!/bin/sh
# SPDX-License-Identifier: MIT
# Reviewer probe: run the fabric talker bench (protocol-processor tb/acmp_talker)
# unchanged, then with its freshness-lapse check moved to the exact 15000 ms edge
# (must still pass: stale at 15000) and to 14999 ms (must fail D2: still fresh).
# usage: fabric_edge.sh <protocol-processor checkout> <work dir> <verilator>
set -u
PP=$1; WORK=$2; VERILATOR=$3
mkdir -p "$WORK"
for variant in unchanged edge-15000 edge-14999; do
  d="$WORK/$variant"
  rm -rf "$d"; mkdir -p "$d"
  cp -r "$PP/hdl" "$d/hdl"; mkdir -p "$d/tb"; cp -r "$PP/tb/acmp_talker" "$d/tb/acmp_talker"; cp -r "$PP/tb/common" "$d/tb/common"
  f="$d/tb/acmp_talker/sim_main.cpp"
  case $variant in
    edge-15000) sed -i 's|d->now_ms_i = t2 + T_DAFRESH + 1;           // window of B4 has lapsed|d->now_ms_i = t2 + T_DAFRESH;|' "$f";;
    edge-14999) sed -i 's|d->now_ms_i = t2 + T_DAFRESH + 1;           // window of B4 has lapsed|d->now_ms_i = t2 + T_DAFRESH - 1;|' "$f";;
  esac
  changed=$(grep -c 'd->now_ms_i = t2 + T_DAFRESH' "$f")
  (cd "$d/tb/acmp_talker" && make VERILATOR="$VERILATOR" run > "$d/run.log" 2>&1)
  rc=$?
  echo "$variant rc=$rc edge_lines=$changed $(grep -E 'D2|PASS|FAIL|checks' "$d/run.log" | tail -3 | tr '\n' ' ')"
done
