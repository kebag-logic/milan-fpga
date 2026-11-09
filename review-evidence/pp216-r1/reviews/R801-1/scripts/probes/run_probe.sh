#!/usr/bin/env bash
# run_probe.sh ARM GROUP : export the reviewed head into a disposable copy, apply ARM
# ("control" = none, "probe216" = add the probe group), build tb/srp_top and run GROUP.
set -u
arm=$1; group=$2
PKT=$(cd "$(dirname "$0")/../.." && pwd)
SRC=${SRC:?set SRC to a clone holding the reviewed head}
HEAD=60094a268c0df46703a3bee08c94118153634fd9
W=$PKT/scratch/probe-$arm-$group
rm -rf "$W"; mkdir -p "$W"
git -C "$SRC" archive "$HEAD" | tar -x -C "$W"
case $arm in
  control) ;;
  probe216) python3 -I "$PKT/scripts/probes/probe_tb.py" "$W" ;;
  *) python3 -I "$PKT/scripts/probes/mutate.py" "$W" "$arm" ;;
esac
cd "$W/tb/srp_top" && make run RUN_ARGS="$group" VERILATOR="${VERILATOR:-verilator}"
