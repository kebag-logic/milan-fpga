#!/usr/bin/env bash
# Run one command detached with its own log and rc file.
# Usage: run_bg.sh NAME WORKDIR CMD...   (logs to $RUNS/NAME.log, rc to $RUNS/NAME.rc)
# Expects RUNS (output directory) and PATH (pinned verilator first) in the environment.
set -u
name=$1; wd=$2; shift 2
: "${RUNS:?RUNS must name the output directory}"
rm -f "$RUNS/$name.rc"
(
  cd "$wd" || exit 97
  start=$(date +%s)
  "$@" >"$RUNS/$name.log" 2>&1
  rc=$?
  echo "$rc $(( $(date +%s) - start ))" >"$RUNS/$name.rc"
) </dev/null >/dev/null 2>&1 &
disown
echo "started $name pid $!"
