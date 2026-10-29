#!/bin/bash
# One gate in a checkout, its output to a log with the head, elapsed seconds and rc last.
# usage: gate.sh CHECKOUT LOG CWD_REL CMD...
set -u
. $MANAGEMENT/2026-09-23/665s3-a697b/scripts/env.sh
C=$1 LOG=$2 REL=$3; shift 3
start=$(date +%s)
{ echo "HEAD $(git -C "$C" rev-parse HEAD)"; echo "\$ (cd $REL) $*"; } > "$LOG"
(cd "$C/$REL" && "$@") >> "$LOG" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$LOG"
echo "tree: $(git -C "$C" status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s) after the gate" >> "$LOG"
echo "rc=$rc" >> "$LOG"
