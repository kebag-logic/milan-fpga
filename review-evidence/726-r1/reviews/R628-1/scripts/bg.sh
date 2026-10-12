#!/bin/sh
# Usage: bg.sh <name> <dir> <command...>
# Runs <command> in <dir> detached, logging to receipts/<name>.log and the
# exit status to receipts/<name>.rc. Paths are relative to the packet root.
PKT=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$PKT/receipts/$name.rc"
(
  cd "$dir" || exit 99
  VERILATOR=${VERILATOR:-verilator}
  export VERILATOR
  "$@" > "$PKT/receipts/$name.log" 2>&1
  echo $? > "$PKT/receipts/$name.rc"
) </dev/null >/dev/null 2>&1 &
echo "started $name pid $!"
