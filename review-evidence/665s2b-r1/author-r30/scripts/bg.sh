#!/bin/bash
# Run a command in a checkout, its output to LOG and its rc to LOG.rc. usage: bg.sh CHECKOUT LOG cmd...
C=$1 LOG=$2; shift 2
. /data-2/milan/tmp/665s2b-a683zo/scripts/env.sh
export MAKEFLAGS="${MAKEFLAGS:--j8 --no-print-directory}" PYTHONUNBUFFERED=1 TMPDIR=${TMPDIR:-/data-2/milan/tmp/665s2b-a683zo/tmp}
cd "$C" || exit 3
start=$(date +%s)
"$@" > "$LOG" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$LOG"
echo $rc > "$LOG.rc"
