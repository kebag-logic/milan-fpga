#!/usr/bin/env bash
# Start one command detached, with its own log and rc file, and return at once.
# usage: launch.sh LOGDIR NAME COMMAND [ARG ...]
# Writes LOGDIR/NAME.log (stdout and stderr), LOGDIR/NAME.time (/usr/bin/time -v) and,
# when the command ends, LOGDIR/NAME.rc. Wait for the rc files with a foreground poll.
set -euo pipefail
dir=$1; name=$2; shift 2
mkdir -p "$dir"
rm -f "$dir/$name.rc"
setsid nohup bash -c '
  dir=$1; name=$2; shift 2
  /usr/bin/time -v -o "$dir/$name.time" "$@" > "$dir/$name.log" 2>&1
  echo $? > "$dir/$name.rc"
' launch "$dir" "$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name"
