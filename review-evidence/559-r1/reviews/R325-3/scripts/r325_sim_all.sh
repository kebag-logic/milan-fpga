#!/bin/sh
# [R325] R325-3: run the sim step of r325_head_probe.sh for the four 50 MHz arms
# in parallel (4 jobs), each writing its own log and rc file.
set -u
P=$1; S=$2
export LITEX_PY SDK_BIN VL_BIN
for a in "endstation_ax7101_8x8 on" "endstation_ax7101_8x8 off" "endstation_ax7101_1x1_tdm8 on" "endstation_ax7101_1x1_tdm8 off"; do
  set -- $a
  ( "$P/scripts/r325_head_probe.sh" "$S/clone-src" "$S" "$1" 50000000 "$2" 16 sim > "$S/sim-$1-50-$2.log" 2>&1; echo "rc=$?" > "$S/sim-$1-50-$2.rc" ) &
done
wait
echo done > "$S/sim-all.done"
