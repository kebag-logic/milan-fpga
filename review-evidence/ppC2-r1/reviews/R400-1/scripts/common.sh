#!/usr/bin/env bash
# Shared settings for the R400-1 probes. Override via environment:
#   CLONE    the detached review clone at the exact head
#   PACKET   this packet directory
#   VERILATOR  a Verilator 5.050 executable
set -euo pipefail
HEAD_SHA=b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745
HEAD_TREE=7916d0854d52eecb28b03ac5e665d05355b7be08
BASE_SHA=c951a9ff0cb5851fb159d33e966e5a2a9a188fe3
CLONE=${CLONE:-$REVIEWS/r400-1-ppC2}
PACKET=${PACKET:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator}
SCRATCH=$PACKET/scratch
RECEIPTS=$PACKET/receipts
# at most 8 parallel jobs: pin to 8 CPUs so Verilator's -j 0 sees 8
CPUSET=${CPUSET:-0-7}
export VERILATOR
mkdir -p "$SCRATCH" "$RECEIPTS"

# export a pristine copy of a commit into $1 (never touches the clone's worktree)
export_tree() {
  local dest=$1 rev=${2:-$HEAD_SHA}
  rm -rf "$dest"; mkdir -p "$dest"
  git -C "$CLONE" archive "$rev" | tar -x -C "$dest"
}

# run a make target, tee to a receipt, record rc; never aborts the caller
run_target() {
  local tree=$1 suite=$2 target=$3 log=$4
  set +e
  ( cd "$tree/tb/$suite" && taskset -c "$CPUSET" make VERILATOR="$VERILATOR" "$target" ) >"$log" 2>&1
  local rc=$?
  set -e
  echo "rc=$rc" >>"$log"
  echo "$suite/$target rc=$rc tally: $(grep -E '[0-9]+ checks' "$log" | tail -1)"
  return 0
}
