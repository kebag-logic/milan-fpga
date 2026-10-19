#!/usr/bin/env bash
# Launch one named job detached, with its own log and rc file.
# usage: launch.sh NAME DIR CMD...   (log: receipts/NAME.log, rc: receipts/NAME.rc)
# PKT defaults to this script's packet; VBIN is prepended to PATH (pinned Verilator).
set -u
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
rm -f "$PKT/receipts/$name.rc"
(
  cd "$dir" || exit 97
  export PATH="${VBIN:-$PKT/scratch/bin}:$PATH" TMPDIR="$PKT/scratch/tmp"
  "$@" > "$PKT/receipts/$name.log" 2>&1
  echo $? > "$PKT/receipts/$name.rc"
) </dev/null >/dev/null 2>&1 &
disown
echo "launched $name"
