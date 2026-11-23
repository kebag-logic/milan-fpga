#!/usr/bin/env bash
# Start one campaign detached, pinned to the review's 16 CPUs, with its own log, argv, rc and times.
# Usage: launch.sh <receipt-dir> <workdir> <command...>
# Environment: REVIEW_CPUS (default 0-15), SDK_BIN (the verified pinned RV32 SDK's bin), LITEX_VENV_BIN.
set -euo pipefail
out=$1; shift
work=$1; shift
mkdir -p "$out"
printf '%s\n' "$@" > "$out/argv.txt"
git -C "$work" rev-parse HEAD > "$out/head.txt"
cpus=${REVIEW_CPUS:-0-15}
setsid nohup bash -c '
  out=$1; work=$2; cpus=$3; shift 3
  date -Is > "$out/start.txt"
  cd "$work"
  rc=0
  taskset -c "$cpus" env PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true "$@" > "$out/log.txt" 2>&1 || rc=$?
  date -Is > "$out/end.txt"
  echo "$rc" > "$out/rc"
' _ "$out" "$work" "$cpus" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $out"
