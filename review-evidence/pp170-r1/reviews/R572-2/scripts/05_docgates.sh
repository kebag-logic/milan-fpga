#!/bin/sh
# Documentation gates on a pristine copy of the head: make check and the matrix check.
set -u; . "$(dirname "$0")/env.sh"
t="$SCRATCH/docgates"; rm -rf "$t"; git clone -q --no-hardlinks "$SRC" "$t" && git -C "$t" checkout -q --detach "$HEAD_SHA"
( cd "$t" && make check ) > "$RCPT/make-check.log" 2>&1; echo $? > "$RCPT/make-check.rc"
( cd "$t" && python3 scripts/gen_matrix.py --check ) > "$RCPT/gen-matrix-check.log" 2>&1; echo $? > "$RCPT/gen-matrix-check.rc"
