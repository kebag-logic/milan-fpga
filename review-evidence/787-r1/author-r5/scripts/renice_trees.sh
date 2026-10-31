#!/usr/bin/env bash
# #787 round 5: set nice +10 on the given process trees (every descendant, to any depth) and on every process of the
# lane's Vivado scopes, so the LiteX aggregate re-run's members are not starved on the unit's 16 CPUs. Children
# and threads created later inherit the value. Scheduling only; no gate input changes.
# usage: renice_trees.sh <root-pid>...
set -u
todo="$*"; all=""
while [ -n "$todo" ]; do
  next=""
  for p in $todo; do all+=" $p"; next+=" $(pgrep -d ' ' -P "$p")"; done
  todo=$(echo $next)
done
for p in $(ps -eo pid=); do
  case "$(cat /proc/$p/cgroup 2>/dev/null)" in *milan-787-a700f-viv-*) all+=" $p";; esac
done
n=0
# every thread of each process: setpriority on a pid reaches only the thread with that id
for p in $all; do for t in $(ls /proc/$p/task 2>/dev/null); do renice --priority 10 -p "$t" > /dev/null 2>&1 && n=$((n+1)); done; done
echo "nice +10 on $n thread(s)"
