#!/bin/sh
# Run one campaign driver from a git-archive extraction of the head.
# Usage: campaign.sh REPO SCRATCH OUT VERILATOR DRIVER JOBS [extra args]
set -u
REPO=$1 S=$2 OUT=$3 V=$4 DRV=$5 J=$6; shift 6
HEAD=79571006b803a4ab4af65358f0d87bc3af73180e
name=$(basename "$DRV" .py)
T="$S/camp-$name"; rm -rf "$T"; mkdir -p "$T/tree" "$T/tmp" "$OUT/$name"
git -C "$REPO" archive $HEAD | tar -x -C "$T/tree"
cd "$T/tree"
TMPDIR="$T/tmp" python3 "$DRV" --output "$OUT/$name" --verilator "$V" --jobs "$J" "$@" > "$OUT/$name.driver.log" 2>&1
echo $? > "$OUT/$name.rc"
