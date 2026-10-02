#!/bin/sh
# Run one chunk of tb/pp_top/d3_mutants.py (names one per line in CHUNKFILE)
# from an exported head tree, capped at 4 concurrent mutants x 2 build jobs.
# Usage: d3_chunk.sh HEADTREE CHUNKFILE OUTDIR LOG VERILATOR_WRAPPER
set -u
T="$1"; C="$2"; O="$3"; L="$4"; V="$5"
export R431_VJOBS=2
rm -rf "$O"
cd "$T" && timeout 595 python3 tb/pp_top/d3_mutants.py --output "$O" --verilator "$V" \
    --jobs 4 --only $(cat "$C") > "$L" 2>&1
rc=$?
echo "rc=$rc" >> "$L"
exit $rc
