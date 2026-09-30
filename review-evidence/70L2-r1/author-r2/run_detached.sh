#!/bin/bash
# Start one long command detached, so it outlives a single foreground call:
# run_detached.sh <logfile> <command...>. Writes <logfile> (stdout+stderr) and
# <logfile>.rc when the command ends; poll for the .rc file in the foreground.
set -u
LOG=$1; shift
rm -f "$LOG.rc"
setsid nohup bash -c '"$@" > "$0" 2>&1; echo $? > "$0.rc"' "$LOG" "$@" < /dev/null > /dev/null 2>&1 &
echo "started pid $! -> $LOG"
