#!/usr/bin/env bash
# Launch one gate detached: bg.sh NAME DIR CMD...
# Writes receipts/NAME.log (stdout+stderr, unpiped into the gate itself),
# receipts/NAME.rc (the gate's own exit status) and receipts/NAME.time
# (peak RSS and wall time). Uses the pinned simulator first on PATH.
set -u
PKT="$(cd "$(dirname "$0")/.." && pwd)"
name=$1; dir=$2; shift 2
R="$PKT/receipts"
mkdir -p "$R" "$PKT/scratch/tmp"
rm -f "$R/$name.rc"
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH"
export TMPDIR="$PKT/scratch/tmp"
setsid nohup bash -c '
  cd "$1" || { echo 127 > "$2.rc"; exit; }
  shift 2
  /usr/bin/time -v -o "$0.time" "$@" > "$0.log" 2>&1
  echo $? > "$0.rc"
' "$R/$name" "$dir" "$R/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name pid $!"
