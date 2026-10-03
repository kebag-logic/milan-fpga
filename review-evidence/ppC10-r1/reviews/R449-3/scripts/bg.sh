#!/usr/bin/env bash
# Start one job detached, with its own log and rc file.
# usage: bg.sh <name> <workdir> <command...>
# Writes receipts/<name>.log, receipts/<name>.rc (rc appears only on exit) and
# receipts/<name>.time (wall seconds). PATH is prefixed with the pinned
# Verilator shim; TMPDIR points into scratch.
set -u
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
name=$1 wd=$2; shift 2
rm -f "$P/receipts/$name.rc"
(
  export PATH="$P/scratch/bin:$PATH" TMPDIR="$P/scratch/tmp"
  cd "$wd" || exit 97
  t0=$(date +%s.%N)
  "$@" > "$P/receipts/$name.log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  echo "$t0 $t1" | awk '{printf "%.2f\n", $2-$1}' > "$P/receipts/$name.time"
  echo "$rc" > "$P/receipts/$name.rc"
) < /dev/null > /dev/null 2>&1 &
echo "started $name pid $!"
