#!/bin/sh
# R602-2 probe runner: copy a disposable exact-head TEMPLATE tree, plant
# probe LABEL (plant.py), and run the shipping writer gate on one shape.
# Usage: run_probe.sh TEMPLATE WORKROOT LABEL CONFIG JOBS LOGDIR
# Writes LOGDIR/LABEL.log and LOGDIR/LABEL.rc (the gate's exit status;
# 1 = caught, 0 = the gate stayed green on the plant, 2 = harness error,
# 3 = the plant did not apply).
set -u
tmpl=$1; root=$2; label=$3; cfg=$4; jobs=$5; logs=$6
here=$(cd "$(dirname "$0")" && pwd)
tree="$root/probe_$label"
rm -rf "$tree"
cp -a "$tmpl" "$tree"
if ! python3 -I "$here/plant.py" "$tree" "$label" > "$logs/$label.log" 2>&1; then
	echo 3 > "$logs/$label.rc"
	exit 0
fi
cd "$tree" || exit 2
python3 -u sw/firmware/nvm_hosttest/test_nvm_firmware.py --config "$cfg" --jobs "$jobs" \
	>> "$logs/$label.log" 2>&1
echo $? > "$logs/$label.rc"
