#!/bin/sh
# R417-2 probe: run tb/pp_top section AX in the bench's own line build at the
# documented ceiling, DESC_LINE_BYTES_P = 1008 (the suite runs it at 584 only).
# OV1/OV5 then read a 1008-byte whole-line AUDIO_MAP (cdl 1024, frame 1050)
# and RB requires the top elaborated 1008, no response byte past 16 + 1008,
# and the largest response reaching byte 1024.
# Usage: probe_line1008.sh <head-export> <scratch-dir> <verilator>
set -u
SRC=$1; WORK=$2; VL=$3
rm -rf "$WORK"; mkdir -p "$WORK"
cp -a "$SRC/hdl" "$SRC/tb" "$WORK/"
cd "$WORK/tb/pp_top" && rm -rf obj_dir obj_vid obj_line
make VERILATOR="$VL" LINE_FIXTURE=1008 aecp-line
echo "rc=$?"
