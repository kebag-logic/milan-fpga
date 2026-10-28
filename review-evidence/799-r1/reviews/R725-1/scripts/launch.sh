#!/bin/sh
# Start one gate detached, with its own log and rc file.
# Usage: launch.sh <name> <workdir> <command...>
# Writes <packet>/receipts/<name>.log and <name>.rc (the command's own rc).
set -eu
R=$REVIEWS/799-r725-1-packet/receipts
name=$1; dir=$2; shift 2
rm -f "$R/$name.rc"
(
  cd "$dir"
  export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
  export TMPDIR=$REVIEWS/799-r725-1-packet/scratch/tmp
  export PYTHONHASHSEED=0
  mkdir -p "$TMPDIR"
  echo "# $name in $dir at $(git rev-parse HEAD 2>/dev/null) started $(date -Is)"
  echo "# command: $*"
  rc=0; sh -c "$*" || rc=$?
  echo "# finished $(date -Is) rc=$rc"
  echo "$rc" > "$R/$name.rc"
) > "$R/$name.log" 2>&1 < /dev/null &
echo "launched $name pid $!"
