#!/bin/bash
# Run one command in a directory with the lane's environment, its output to a log with the head, elapsed and rc last.
# usage: bg.sh DIR LOG CMD...
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683l/scripts/env.sh
D=$1 LOG=$2; shift 2
start=$(date +%s)
{ echo "HEAD $(git -C "$D" rev-parse HEAD) DIRTY $(git -C "$D" status --porcelain --untracked-files=no | wc -l)"; echo "\$ $*"; } > "$LOG"
(cd "$D" && "$@") >> "$LOG" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$LOG"
echo "tree: $(git -C "$D" status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s) after" >> "$LOG"
echo "rc=$rc" >> "$LOG"
