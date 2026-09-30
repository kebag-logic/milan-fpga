#!/usr/bin/env bash
# Build a scratch copy of the head with the reviewer probes and run DL and HZ.
# Usage: run-probes.sh <clone> <head-sha> <packet-dir>
set -u
CLONE=$1; HEAD=$2; PKT=$3
EXP=$PKT/scratch/probe
rm -rf "$EXP"; mkdir -p "$EXP" "$PKT/receipts"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP"
sed -i 's/--build -j 0/--build -j 8/' "$EXP/tb/pp_top/Makefile"
python3 "$PKT/scripts/probe_patch.py" "$EXP/tb/pp_top/sim_main.cpp"
export PATH="$PKT/scratch/bin:$PATH"
make -C "$EXP/tb/pp_top" gsi-build > "$PKT/receipts/30-probe-build.log" 2>&1 || { echo build failed; tail -30 "$PKT/receipts/30-probe-build.log"; exit 1; }
(cd "$EXP/tb/pp_top" && ./obj_dir/Vpp_top_sim --deadline-only) > "$PKT/receipts/31-probe-deadline.log" 2>&1; echo "deadline rc=$?"
(cd "$EXP/tb/pp_top" && ./obj_dir/Vpp_top_sim --hazards-only) > "$PKT/receipts/32-probe-hazards.log" 2>&1; echo "hazards rc=$?"
