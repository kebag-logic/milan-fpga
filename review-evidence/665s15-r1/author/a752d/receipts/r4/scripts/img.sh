#!/bin/bash
# Link one size-fixture image. usage: img.sh TREE CONFIG_STEM N_IF OUTDIR [extra args]
set -u
T=$1 C=$2 N=$3 O=$4; shift 4
source $SCRATCH/scripts/env.sh
R=$SCRATCH/fw
L=""; [ "$C" = endstation_ax7101_8x8 ] && [ "$N" = 2 ] && L="--ledgered-point 8x8-two-interfaces"
rm -rf "$O"
cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$C.yaml --interfaces $N --with-aecp --layout split --output "$O" $L --libc $R/runtime/libc.a --compiler-runtime $R/runtime/libcompiler_rt.a "$@" > "$O.log" 2>&1
rc=$?
echo "$C if$N rc=$rc $( [ -f "$O/ctrl_app.elf" ] && sha256sum "$O/ctrl_app.elf" | cut -c1-16 )"
exit $rc
