#!/bin/sh
# Fabric T-SRP-DAFRESH edge probe on KL_acmp_talker (processor gitlink of milan-fpga dev).
# usage: fabric_edge_probe.sh <processor checkout> <work dir> <verilator>
# stock: unmodified suite; edge15000: expiry at exactly ping+15000 must close (suite passes);
# edge14999: expiry at ping+14999 must NOT close (D2 close check fails).
set -u
SRC=$1; WORK=$2; VER=$3
for v in stock edge15000 edge14999; do
  rm -rf "$WORK/$v"; mkdir -p "$WORK/$v"
  cp -r "$SRC/hdl" "$SRC/tb" "$WORK/$v/"
  f="$WORK/$v/tb/acmp_talker/sim_main.cpp"
  case $v in
    edge15000) sed -i 's/d->now_ms_i = t2 + T_DAFRESH + 1; /d->now_ms_i = t2 + T_DAFRESH;     /' "$f" ;;
    edge14999) sed -i 's/d->now_ms_i = t2 + T_DAFRESH + 1; /d->now_ms_i = t2 + T_DAFRESH - 1; /' "$f" ;;
  esac
  grep -n "d->now_ms_i = t2 + T_DAFRESH" "$f"
  (cd "$WORK/$v/tb/acmp_talker" && make VERILATOR="$VER" run > ../../run.log 2>&1; echo $? > ../../run.rc)
  echo "$v rc=$(cat "$WORK/$v/run.rc")"; grep -E "D2|PASS|FAIL|checks" "$WORK/$v/run.log" | tail -6
done
