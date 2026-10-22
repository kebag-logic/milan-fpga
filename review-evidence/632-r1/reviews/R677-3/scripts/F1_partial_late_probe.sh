#!/bin/sh
# Reproduce the partial-late probe on KL_render_queue at the reviewed head.
# usage: F1_partial_late_probe.sh <repo-at-head> <workdir> <verilator>
set -eu
R=$1; W=$2; V=$3; HERE=$(cd "$(dirname "$0")" && pwd)
for v in base probe; do
  mkdir -p "$W/$v/tb/verilator" "$W/$v/tb/common" "$W/$v/hdl/ieee1722/aaf"
  cp -r "$R/tb/verilator/render_queue" "$W/$v/tb/verilator/"
  cp "$R/tb/common/verilator_harness.hpp" "$W/$v/tb/common/"
  cp "$R/hdl/ieee1722/aaf/KL_render_queue.sv" "$W/$v/hdl/ieee1722/aaf/"
done
(cd "$W/probe/tb/verilator/render_queue" && patch -p4 < "$HERE/F1_partial_late_probe.patch")
for v in base probe; do
  (cd "$W/$v/tb/verilator/render_queue" && { make -s run VERILATOR="$V" > "$W/$v.run.log" 2>&1; echo $? > "$W/$v.run.rc"; make -s odd VERILATOR="$V" > "$W/$v.odd.log" 2>&1; echo $? > "$W/$v.odd.rc"; })
done
