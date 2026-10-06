#!/bin/sh
# bg.sh NAME CMD...: run CMD detached (own session) in the review clone, log to receipts/NAME.log, rc to receipts/NAME.rc
P=$REVIEWS/665ft-r506-2-packet
name=$1; shift
export TMPDIR=$P/scratch/tmp P name
rm -f "$P/receipts/$name.rc"
setsid sh -c 'cd "${RUN_DIR:-$REVIEWS/r506-2-665ft}" && "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc"' sh "$@" </dev/null >/dev/null 2>&1 &
