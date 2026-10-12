#!/usr/bin/env bash
# Start one named campaign detached, with its own log and rc file.
# usage: launch.sh NAME WORKDIR CMD...   (log: receipts/NAME.log, rc: receipts/NAME.rc)
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
mkdir -p "$P/receipts"
rm -f "$P/receipts/$name.rc"
VL=$VALIDATION_TOOLS/pinned-verilator-5.050
setsid nohup bash -c '
  cd "$1" || exit 99; shift
  log=$1; rc=$2; shift 2
  { echo "# cwd: $(pwd)"; echo "# head: $(git rev-parse HEAD 2>/dev/null)"; echo "# cmd: $*";
    echo "# start: $(date -u +%FT%TZ)"; } >"$log"
  PATH='"$VL"':$PATH "$@" >>"$log" 2>&1; r=$?
  echo "# end: $(date -u +%FT%TZ) rc=$r" >>"$log"; echo $r >"$rc"
' _ "$dir" "$P/receipts/$name.log" "$P/receipts/$name.rc" "$@" </dev/null >/dev/null 2>&1 &
echo "launched $name"
