#!/usr/bin/env bash
# Start one named campaign detached, pinned to a CPU set, with its own log, rc
# and wall-time files under $PKT/receipts/<name>.{log,rc,wall}.
# Usage: launch.sh NAME CPUSET WORKDIR -- COMMAND...
set -u
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; cpus=$2; wd=$3; shift 3; [ "$1" = "--" ] && shift
r=$PKT/receipts/$name
rm -f "$r.rc" "$r.log" "$r.wall"
cmd=$(printf '%q ' "$@")
setsid nohup bash -c "cd '$wd' && s=\$(date +%s); taskset -c $cpus bash -c $(printf '%q' "$cmd") >'$r.log' 2>&1; rc=\$?; echo \$rc >'$r.rc'; echo \$(( \$(date +%s) - s )) s >'$r.wall'" </dev/null >/dev/null 2>&1 &
echo "launched $name pid $! on cpus $cpus in $wd"
