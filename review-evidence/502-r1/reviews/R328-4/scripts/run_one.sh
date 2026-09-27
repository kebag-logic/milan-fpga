#!/bin/sh
# R328-4: run one focused command from the candidate root, bounded to 8 CPUs,
# recording the command, start/end UTC, wall seconds and exit status.
# Usage: run_one.sh <candidate-clone> <receipt-dir> <name> <bin-dir> <cmd...>
set -u
C=$1; OUT=$2; NAME=$3; BIN=$4; shift 4
mkdir -p "$OUT"
PATH="$BIN:$PATH"; export PATH
cd "$C" || exit 2
LOG="$OUT/$NAME.log"
{
  printf '$ %s\n' "$*"
  printf 'start %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'verilator %s\n' "$(verilator --version 2>&1)"
  printf 'head %s tree %s\n' "$(git rev-parse HEAD)" "$(git rev-parse 'HEAD^{tree}')"
} > "$LOG"
t0=$(date +%s)
taskset -c 0-7 "$@" >> "$LOG" 2>&1
rc=$?
t1=$(date +%s)
printf 'end %s wall_s %s rc %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$((t1 - t0))" "$rc" >> "$LOG"
printf '%s\n' "$rc" > "$OUT/$NAME.rc"
