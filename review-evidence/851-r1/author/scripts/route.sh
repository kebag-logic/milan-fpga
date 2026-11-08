#!/usr/bin/env bash
# route.sh <head>: the shipping AX7101 1x1 TDM8 route at <head>, one directive (ExtraPostPlacementOpt, SEEDS=eppo), under
# the Vivado slot. build-dev.sh stops before any board step and --no-capture opens no console: nothing is flashed.
# Waits until no other route (milan_soc.py) runs on the host, so this lane never routes beside another route.
set -u
M=$HOME/milan-fpga-management/2026-09-23; here=$(cd "$(dirname "$0")" && pwd)
H=$1; S=$VALIDATION_STORAGE/scratch/851-a744/route-${H:0:8}
CLONE=$VALIDATION_STORAGE/worktrees/build-851a744-${H:0:12}
mkdir -p "$S/out"
[ -d "$CLONE" ] || bash "$here/make_clone.sh" "$CLONE" "$H" > "$S/clone.log" 2>&1 || { echo 3 > "$S/build.rc"; exit 3; }
# build-dev.sh fetches origin in a reused clone; its submodules point at the lane, so no recursion
git -C "$CLONE" config fetch.recurseSubmodules false
while pgrep -f 'milan_soc.py' > /dev/null; do sleep 30; done
echo "queue released $(date -Iseconds)" > "$S/queue.log"
SEEDS=eppo BUILD_OUT="$S/out" BUILD_CLONE="$CLONE" bash "$M/vivado-slot.sh" bash "$M/build-dev.sh" "$H" \
  --tag meas851a744h${H:0:6} --no-capture --console /dev/null > "$S/build.log" 2>&1
echo $? > "$S/build.rc"
