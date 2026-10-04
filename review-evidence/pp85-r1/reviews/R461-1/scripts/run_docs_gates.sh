#!/bin/sh
# make check and gen_matrix --check on a local clone of HEAD in scratch (the review clone is not written).
. "$(dirname "$0")/env.sh"
set -u
d="$SCRATCH/docs-gates"; rm -rf "$d"
git clone -q --no-hardlinks "$CLONE" "$d" && git -C "$d" checkout -q --detach "$HEAD_SHA"
git -C "$d" rev-parse HEAD > "$RCPT/docs-gates.log"
(cd "$d" && make check) >> "$RCPT/docs-gates.log" 2>&1; rc1=$?
echo "make check rc=$rc1" >> "$RCPT/docs-gates.log"
(cd "$d" && python3 scripts/gen_matrix.py --check) >> "$RCPT/docs-gates.log" 2>&1; rc2=$?
echo "gen_matrix --check rc=$rc2" >> "$RCPT/docs-gates.log"
echo "$rc1 $rc2" > "$RCPT/docs-gates.rc"
