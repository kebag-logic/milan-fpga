#!/bin/sh
# Usage: run_job.sh <out-dir> <name> <cwd> <command> [args...]
# Runs one command in <cwd>, writing <out-dir>/<name>.log, <name>.rc and
# <name>.cmd (argv, cwd, start/end UTC and wall seconds). The pinned
# Verilator directory, when VERILATOR_DIR is set, is prepended to PATH.
out=$1; name=$2; cwd=$3; shift 3
mkdir -p "$out"
[ -n "$VERILATOR_DIR" ] && PATH="$VERILATOR_DIR:$PATH" && export PATH
start=$(date -u +%s)
{
  echo "argv: $*"
  echo "cwd: $cwd"
  echo "start_utc: $(date -u -d @"$start" +%Y-%m-%dT%H:%M:%SZ)"
} > "$out/$name.cmd"
( cd "$cwd" && "$@" ) > "$out/$name.log" 2>&1
rc=$?
end=$(date -u +%s)
echo "end_utc: $(date -u -d @"$end" +%Y-%m-%dT%H:%M:%SZ)" >> "$out/$name.cmd"
echo "wall_seconds: $((end - start))" >> "$out/$name.cmd"
echo "$rc" > "$out/$name.rc"
