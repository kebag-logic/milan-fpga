#!/usr/bin/env bash
# Usage: [CWD=dir] bg.sh <name> <cmd...> : run detached inside $CWD (default .)
# writing $RUNS/<name>.log and $RUNS/<name>.rc
set -u
RUNS=${RUNS:?}; name=$1; shift
mkdir -p "$RUNS"
nohup bash -c 'cd "$1" || exit 99; n=$2; shift 2; "$@" > "$n.log" 2>&1; echo $? > "$n.rc"' _ "${CWD:-.}" "$RUNS/$name" "$@" > /dev/null 2>&1 &
echo "started $name pid $!"
