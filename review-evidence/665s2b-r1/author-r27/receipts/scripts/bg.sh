#!/bin/bash
# Run a command in a checkout, detached, its output to LOG and its rc to LOG.rc. usage: bg.sh CHECKOUT LOG cmd...
C=$1 LOG=$2; shift 2
. <scratch>/scripts/env.sh
export MAKEFLAGS="${MAKEFLAGS:--j8 --no-print-directory}" PYTHONUNBUFFERED=1 TMPDIR=${TMPDIR:-<scratch>/tmp}
cd "$C" || exit 3
start=$(date +%s)
"$@" > "$LOG" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$LOG"
echo $rc > "$LOG.rc"
