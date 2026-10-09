#!/bin/sh
# launch.sh NAME CPUSET DIR -- CMD...  : run CMD detached in DIR pinned to CPUSET,
# writing OUT/NAME.log, OUT/NAME.rc and OUT/NAME.time (wall seconds).
# OUT defaults to the packet's receipts/runs directory.
name=$1; cpus=$2; dir=$3; shift 3; [ "$1" = "--" ] && shift
OUT=${OUT:-$(cd "$(dirname "$0")/.." && pwd)/receipts/runs}
mkdir -p "$OUT"
rm -f "$OUT/$name.rc" "$OUT/$name.time"
printf '%s\n' "cd $dir && taskset -c $cpus $*" > "$OUT/$name.cmd"
CPUS=$cpus OUTF=$OUT/$name setsid nohup sh -c '
  start=$(date +%s.%N)
  cd "$1" || exit 99
  shift
  taskset -c "$CPUS" "$@"
  rc=$?
  end=$(date +%s.%N)
  echo "$end - $start" | bc > "$OUTF.time"
  echo $rc > "$OUTF.rc"
' sh "$dir" "$@" > "$OUT/$name.log" 2>&1 < /dev/null &
