#!/usr/bin/env bash
# bg.sh <out-dir> <name> <cwd> <cmd...>: run <cmd> detached (setsid, no nohup: the sweep driver's
# cancellation self-test needs SIGHUP's default action) with the lane environment, writing
# <out-dir>/<name>.log, then <name>.rc holding "<rc> <seconds>s".
set -u
out=$1; name=$2; cwd=$3; shift 3
mkdir -p "$out"
here=$(cd "$(dirname "$0")" && pwd)
rm -f "$out/$name.rc"
setsid bash -c '
  source "$1/env.sh"; out=$2; name=$3; cd "$4" || exit 2; shift 4
  s=$(date +%s); "$@" > "$out/$name.log" 2>&1; rc=$?
  echo "$rc $(( $(date +%s) - s ))s" > "$out/$name.rc"' bg "$here" "$out" "$name" "$cwd" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name pid $!"
