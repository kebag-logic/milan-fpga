#!/usr/bin/env bash
# The MAKEFLAGS=w reproduction at the lane's head (#617 R394-3 F1):
#  1. R394-3's own script (read-only, from its packet): mutants.build('dp') with no
#     MAKEFLAGS and with MAKEFLAGS=w, and the nested DP_SRCS it sees;
#  2. the hosted chain: GNU make 4.3 on PATH, `make -C <dir>` running a recipe that
#     calls mutants.build('dp') with the MAKEFLAGS it inherited (w).
# Exit 0 only if all three builds produce the harness.
set -uo pipefail
S=$LANES/617-capture-frame-atomic/tb/verilator/capture_coherence
W=$VALIDATION_STORAGE/617-a434-work/gates/mfwork
rm -rf "$W"
mkdir -p "$W"
export PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$PATH
echo "## R394-3 scripts/r394_mf_repro.py (GNU make $(make --version | head -1 | awk '{print $3}'))"
out1=$(python3 $REVIEWS/617-r394-3-packet/scripts/r394_mf_repro.py "$S" "$W/r394" 2>&1)
echo "$out1"
echo "## hosted chain: GNU make 4.3, make -C <dir> -> recipe -> mutants.build('dp')"
out2=$(env PATH=$VALIDATION_STORAGE/617-a434-work/tools/make43/bin:$PATH \
       make -C $VALIDATION_STORAGE/617-a434-work/mfdrv SUITE="$S" WORK="$W/make43" 2>&1)
echo "$out2"
built1=$(grep -c "mutants.build('dp') -> built" <<< "$out1")
built2=$(grep -c "mutants.build('dp') -> built" <<< "$out2")
echo "## built: R394-3 script $built1 of 2, make 4.3 chain $built2 of 1"
[ "$built1" = 2 ] && [ "$built2" = 1 ]
