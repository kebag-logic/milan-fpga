#!/bin/sh
# Start one named job detached, with its own log and rc file under receipts/.
# Usage: launch.sh NAME WORKDIR CMD...
# Environment expected: PKT (packet root), VERILATOR, CTRL_RV32_CC, TMPDIR.
set -eu
name=$1; dir=$2; shift 2
log="$PKT/receipts/$name.log"; rc="$PKT/receipts/$name.rc"
rm -f "$rc"
cd "$dir"
setsid nohup sh -c 'start=$(date +%s); "$@"; r=$?; end=$(date +%s); echo "rc=$r seconds=$((end-start))" >> "$0.log"; echo $r > "$0.rc"' \
  "$PKT/receipts/$name" "$@" > "$log" 2>&1 < /dev/null &
echo "launched $name pid $!"
