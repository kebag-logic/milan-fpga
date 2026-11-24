#!/usr/bin/env bash
# Launch one job detached with its own log and rc file.
# Usage: launch.sh NAME CWD CMD...   (logs to $OUT/NAME.log, rc to $OUT/NAME.rc)
set -u
OUT=${OUT:?}
name=$1; cwd=$2; shift 2
rm -f "$OUT/$name.rc"
( cd "$cwd" && setsid nohup bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$OUT/$name" "$@" < /dev/null > /dev/null 2>&1 & )
echo "launched $name"
