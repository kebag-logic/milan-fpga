#!/usr/bin/env bash
# route.sh <head>: the shipping AX7101 1x1 TDM8 route at <head>, one directive (ExtraPostPlacementOpt, SEEDS=eppo),
# under the Vivado slot, never flashing (build-dev.sh stops before any board step; --no-capture opens no console).
set -u
M=<mgmt>
H=$1; S=<scratch>/route-${H:0:8}
CLONE=<worktrees>/build-845a738-${H:0:12}
mkdir -p "$S/out"
SEEDS=eppo BUILD_OUT="$S/out" BUILD_CLONE="$CLONE" bash "$M/vivado-slot.sh" bash "$M/build-dev.sh" "$H" --tag meas845a738h${H:0:6} --no-capture --console /dev/null > "$S/build.log" 2>&1
echo $? > "$S/build.rc"
