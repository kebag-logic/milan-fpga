#!/bin/sh
# usage: bg.sh <name> <workdir> <command...>
# Runs one job detached; writes <packet>/receipts/<name>.log and <name>.rc.
# PACKET defaults to this script's parent directory; VERILATOR must name the
# pinned 5.050 wrapper; a bin directory holding a `verilator` link to it is
# prepended to PATH when PIN_BIN is set.
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
: "${VERILATOR:?set VERILATOR to the pinned Verilator 5.050 wrapper}"
export VERILATOR PYTHONDONTWRITEBYTECODE=1
[ -n "$PIN_BIN" ] && export PATH="$PIN_BIN:$PATH"
cd "$dir" || exit 2
rm -f "$PACKET/receipts/$name.rc"
setsid sh -c '/usr/bin/time -v "$@" > "$0.log" 2>&1; echo $? > "$0.rc"' \
  "$PACKET/receipts/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name"
