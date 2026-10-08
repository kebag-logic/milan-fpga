#!/bin/sh
# Usage: static_gates.sh <gates.txt> <tree> <out-dir> [parallel]
# Each line of gates.txt is "name|command"; every command runs in <tree>
# through run_job.sh, <parallel> at a time (default 6).
here=$(cd "$(dirname "$0")" && pwd)
gates=$1; tree=$2; out=$3; par=${4:-6}
grep -v '^#' "$gates" | grep '|' | while IFS='|' read -r name cmd; do
  printf '%s\0%s\0' "$name" "$cmd"
done | xargs -0 -n2 -P "$par" sh -c 'exec "$0" "$1" "$3" "$2" sh -c "$4"' "$here/run_job.sh" "$out" "$tree"
