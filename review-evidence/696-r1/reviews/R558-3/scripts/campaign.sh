#!/bin/sh
# Usage: campaign.sh <clone> <label> <makeflags-or-empty> <outdir>
# Runs the maap suite default target (harness + mutant campaign) with the pinned
# simulator; each label gets its own MDIR so concurrent runs never share output.
set -u
export VERILATOR_JOBS=8 TMPDIR=$4/../scratch/tmp-$2
CLONE=$1; LABEL=$2; MF=$3; OUT=$4
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
LOG=$OUT/campaign-$LABEL.log; RC=$OUT/campaign-$LABEL.rc
MD=$OUT/../scratch/obj-$LABEL
rm -rf "$MD" "$TMPDIR"; mkdir -p "$TMPDIR"
{
  echo "label=$LABEL MAKEFLAGS='$MF' head=$(git -C "$CLONE" rev-parse HEAD) date=$(date -u +%FT%TZ)"
  "$V" --version
  if [ -n "$MF" ]; then
    env MAKEFLAGS="$MF" VERILATOR="$V" make -C "$CLONE/tb/verilator/maap" VERILATOR="$V" VERILATOR_JOBS=8 MDIR="$MD"
  else
    env -u MAKEFLAGS VERILATOR="$V" make -C "$CLONE/tb/verilator/maap" VERILATOR="$V" VERILATOR_JOBS=8 MDIR="$MD"
  fi
  echo "rc=$?"
} > "$LOG" 2>&1
tail -1 "$LOG" | sed 's/rc=//' > "$RC"
