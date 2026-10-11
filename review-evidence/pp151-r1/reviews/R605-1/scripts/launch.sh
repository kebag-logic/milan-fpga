#!/usr/bin/env bash
# Start one named job detached, with its own log, rc and seconds files.
# usage: launch.sh <name> <toolchain-dir> <cwd> <command...>
# The toolchain dir is put first on PATH (sv2v, yosys, verilator symlinks).
set -u
K=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; tc=$2; cwd=$3; shift 3
log=$K/receipts/$name.log
mkdir -p "$K/receipts"
rm -f "$K/receipts/$name.rc" "$K/receipts/$name.secs"
printf '%s\n' "$*" > "$K/receipts/$name.cmd"
nohup bash -c '
  start=$(date +%s)
  cd "$3" || exit 99
  PATH="$2:$PATH" "${@:5}" > "$4" 2>&1
  rc=$?
  echo $rc > "${4%.log}.rc"
  echo $(( $(date +%s) - start )) > "${4%.log}.secs"
' _ "$name" "$tc" "$cwd" "$log" "$@" > /dev/null 2>&1 &
echo "started $name pid $!"
