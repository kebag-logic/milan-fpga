#!/usr/bin/env bash
# pause_tree.sh STOP|CONT <root-pid>: send SIGSTOP (parents first) or SIGCONT (children first) to <root-pid> and
# every descendant, found through /proc whatever their session. Used to keep two of this lane's own gate chains
# from building at once (memory); it stops nothing for good, and the gates it pauses keep no host-time deadline.
set -u
sig=$1; root=$2
tree() { echo "$1"; for c in $(cat /proc/"$1"/task/*/children 2>/dev/null); do tree "$c"; done; }
pids=$(tree "$root")
if [ "$sig" = STOP ]; then for p in $pids; do kill -STOP "$p" 2>/dev/null; done
else for p in $(echo "$pids" | tac); do kill -CONT "$p" 2>/dev/null; done; fi
echo "$(date +%T) $sig $(echo $pids | wc -w) processes under $root"
