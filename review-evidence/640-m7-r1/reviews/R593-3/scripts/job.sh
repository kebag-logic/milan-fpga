#!/bin/sh
# Run one review job detached, with its own log and rc file.
# Usage: job.sh <receipts-dir> <name> <workdir> <command...>
# Writes <receipts-dir>/<name>.log and, when the command ends, <name>.rc.
set -u
out=$1; name=$2; dir=$3; shift 3
rm -f "$out/$name.rc"
(
  cd "$dir" || { echo 97 > "$out/$name.rc"; exit 0; }
  {
    echo "# job $name"
    echo "# dir $dir"
    echo "# cmd $*"
    echo "# start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } > "$out/$name.log"
  "$@" >> "$out/$name.log" 2>&1
  rc=$?
  echo "# end $(date -u +%Y-%m-%dT%H:%M:%SZ) rc=$rc" >> "$out/$name.log"
  echo "$rc" > "$out/$name.rc"
) < /dev/null > /dev/null 2>&1 &
