#!/bin/sh
# Shared settings. Override any of them from the environment.
: "${PKT:=$(cd "$(dirname "$0")/.." && pwd)}"
: "${SRC:=$REVIEWS/r572-2-pp170}"
: "${HEAD_SHA:=89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54}"
: "${VERILATOR:=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
SCRATCH="$PKT/scratch"
RCPT="$PKT/receipts"
export PKT SRC HEAD_SHA VERILATOR SCRATCH RCPT
# Extract a pristine copy of the exact head into $1 (never touches $SRC's tree).
extract() { rm -rf "$1"; mkdir -p "$1"; git -C "$SRC" archive "$HEAD_SHA" | tar -x -C "$1"; }
