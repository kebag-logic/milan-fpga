#!/bin/bash
# The 3-seed AX7101 1x1 TDM8 place sweep of sw/litex/sweep.sh, ONE SEED AT A
# TIME, under flock /tmp/milan-vivado.lock (held for the whole sequence).
# Why serial: a seed's Vivado peaks at about 7.8 GB (`Memory (MB): peak` in the
# interrupted seeds' vivado.log) and this session runs under a 12 GiB memory
# cap, so three concurrent seeds do not fit. Nothing else changes: the script
# takes sweep.sh's own functions (setup_env, board_shape, check_shape,
# entity_defs, build_base) by evaluating sweep.sh without its final `main "$@"`
# line, so the shape gate, the per-config entity definition and the exact
# build command line ($BASE, --vivado-max-threads 32) are sweep.sh's, and each
# seed gets the same --place-directive and output directory sweep.sh gives it.
# Usage: sweep_serial.sh <repo> <tag> <logdir> [seed ...]   (seeds: asl eto eppo)
set -euo pipefail
REPO=$1 TAG=$2 LOGS=$3; shift 3
[ $# -gt 0 ] && SEEDS=("$@") || SEEDS=(asl eto eppo)
mkdir -p "$LOGS"
exec 9>/tmp/milan-vivado.lock
echo "waiting for the lock $(date -Is)" >> "$LOGS/sweep-serial.log"
flock 9
echo "lock held $(date -Is) head $(git -C "$REPO" rev-parse HEAD) dirty=$(git -C "$REPO" status --porcelain --untracked-files=no | wc -l)" >> "$LOGS/sweep-serial.log"
cd "$REPO"
eval "$(sed '$d' sw/litex/sweep.sh)"
BOARD=ax7101
setup_env
R=$REPO
board_shape
check_shape >> "$LOGS/sweep-serial.log" 2>&1
entity_defs
build_base
declare -A DIRECTIVE=([asl]=AltSpreadLogic_high [eto]=ExtraTimingOpt [eppo]=ExtraPostPlacementOpt)
cd "$W"
for s in "${SEEDS[@]}"; do
  dir="$W/build_${BOARD}_${s}_${TAG}"
  rm -rf "$dir"
  start=$(date +%s)
  echo "seed $s ${DIRECTIVE[$s]} start $(date -Is)" >> "$LOGS/sweep-serial.log"
  set +e
  $BASE --place-directive "${DIRECTIVE[$s]}" --output-dir "$dir" > "$dir.launch.log" 2>&1 < /dev/null  # shellcheck disable=SC2086
  rc=$?
  set -e
  echo "seed $s rc=$rc seconds=$(( $(date +%s) - start )) end $(date -Is)" >> "$LOGS/sweep-serial.log"
  echo "$rc" > "$LOGS/seed-$s.rc"
done
echo "sweep done $(date -Is)" >> "$LOGS/sweep-serial.log"
