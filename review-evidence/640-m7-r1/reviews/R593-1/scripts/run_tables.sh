#!/bin/sh
# Run the gptp_tables lockstep once in a disposable copy of the reviewed tree.
#   run_tables.sh <clone> <scratch-dir> <label> [probe-name]
# Copies the clone's working tree (no .git) to <scratch-dir>/<label>, applies
# the optional reviewer probe, runs `make run` and writes
# <packet>/receipts/tables-<label>.log and .rc
set -u
CLONE=$1; SCR=$2; LABEL=$3; PROBE=${4:-}
PKT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$PKT/receipts"
mkdir -p "$OUT" "$SCR"
TREE="$SCR/$LABEL"
rm -rf "$TREE"
rsync -a --exclude=.git --exclude=obj_dir "$CLONE/" "$TREE/"
LOG="$OUT/tables-$LABEL.log"
(
  echo "label=$LABEL probe=${PROBE:-none} verilator=$(verilator --version)"
  if [ -n "$PROBE" ]; then
    python3 -I "$PKT/scripts/probe_mutants.py" "$TREE" "$PROBE" || { echo "probe apply failed"; exit 3; }
  fi
  make -C "$TREE/tb/verilator/gptp_tables" -s run
) > "$LOG" 2>&1
echo $? > "$OUT/tables-$LABEL.rc"
