#!/usr/bin/env bash
# Launch one reviewer job detached, with its own log and rc file.
# usage: bg.sh NAME WORKDIR COMMAND...
# Writes receipts/NAME.log and receipts/NAME.rc (rc appears only on exit).
set -u
P="$(cd "$(dirname "$0")/.." && pwd)"
name="$1"; dir="$2"; shift 2
mkdir -p "$P/receipts"
rm -f "$P/receipts/$name.rc"
export VERILATOR="${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
export TMPDIR="${TMPDIR:-$P/scratch/tmp}"
mkdir -p "$TMPDIR"
nohup setsid bash -c 'cd "$1" && shift && "$@"; echo $? > "'"$P/receipts/$name.rc"'"' \
  _ "$dir" "$@" > "$P/receipts/$name.log" 2>&1 < /dev/null &
echo "started $name pid $!"
