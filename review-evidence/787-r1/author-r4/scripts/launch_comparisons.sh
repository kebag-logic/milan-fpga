#!/usr/bin/env bash
# #787 round 4: wait until the shipping run has written its synthesis checkpoint and moved on to opt_design, record
# the checkpoint's SHA-256, then start the two comparison directives from it, each through launch.sh.
# usage: launch_comparisons.sh <w1>
set -u
w1=$1; g=$w1/ax7101/gateware; here=$(cd "$(dirname "$0")" && pwd)
until [ -s "$g/alinx_ax7101_synth.dcp" ] && grep -q "^Command: opt_design" "$g/baseline.log" 2>/dev/null; do
  [ -e "$g/baseline.log.rc" ] && { echo "shipping run ended before opt_design: $(cat "$g/baseline.log.rc")"; exit 2; }
  sleep 30
done
echo "== SYNTH-DCP $(date -u +%FT%TZ)"
sha256sum "$g/alinx_ax7101_synth.dcp" | tee "$w1/synth-dcp.sha256"
for d in AltSpreadLogic_high ExtraTimingOpt; do
  bash "$here/launch.sh" "$d" "$w1/ax7101-$d" baseline_implementation.tcl
done
