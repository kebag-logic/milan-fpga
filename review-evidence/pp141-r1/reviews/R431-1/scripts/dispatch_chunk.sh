#!/bin/sh
# Run one chunk of tb/pp_top/aecp_dispatch_mutants.py arms (names one per line
# in CHUNKFILE) from an exported head tree, builds capped at 8 jobs.
# Usage: dispatch_chunk.sh HEADTREE CHUNKFILE OUTDIR LOG VERILATOR_WRAPPER
set -u
T="$1"; C="$2"; O="$3"; L="$4"; V="$5"
export R431_VJOBS=8
rm -rf "$O"
cd "$T/tb/pp_top" && timeout 590 python3 aecp_dispatch_mutants.py --output "$O" --verilator "$V" \
    --only "$(paste -sd, "$C")" > "$L" 2>&1
rc=$?
echo "rc=$rc" >> "$L"
exit $rc
