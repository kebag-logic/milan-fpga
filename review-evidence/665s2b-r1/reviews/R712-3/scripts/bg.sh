#!/bin/sh
# bg.sh NAME CMD...: run CMD detached from the clone root ($CLONE) with the pinned Verilator wrapper
# directory ($PACKET/scratch/bin) first on PATH; output in $PACKET/receipts/NAME.log, exit status in
# $PACKET/receipts/NAME.rc. PACKET defaults to this script's parent directory.
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
: "${CLONE:?set CLONE to the detached clone at the head under review}"
name=$1; shift
cd "$CLONE" || exit 1
export PATH="$PACKET/scratch/bin:$PATH"
rm -f "$PACKET/receipts/$name.rc"
setsid nohup sh -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$PACKET/receipts/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name"
