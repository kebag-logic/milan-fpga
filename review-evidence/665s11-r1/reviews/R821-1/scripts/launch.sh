#!/bin/sh
# launch.sh NAME DIR CMD...: run CMD in DIR in its own session, its output in receipts/NAME.log, its exit
# status in receipts/NAME.rc once it ends. wait.sh polls for the rc file in the foreground.
PK=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
. "$PK/scripts/env.sh"
rm -f "$PK/receipts/$name.rc"
cd "$dir" || exit 2
setsid nohup sh -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$PK/receipts/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "launched $name"
