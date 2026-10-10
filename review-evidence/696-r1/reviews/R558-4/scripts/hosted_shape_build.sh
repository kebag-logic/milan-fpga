#!/bin/sh
# Usage: hosted_shape_build.sh <clone> <make-binary-dir> <scratchdir> <outdir> <verilator-jobs>
# The exact-head integration-build under the hosted failure shape (inherited w and an
# advertised but unavailable jobserver), then the built datapath harness is run.
set -u
C=$1; MB=$2; S=$3; OUT=$4; J=$5; M=$C/tb/verilator/maap
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator; export PATH="$MB:$PATH"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
rm -rf "$S/obj-hs"; mkdir -p "$S"
(cd / && env MAKEFLAGS='w -j8 --jobserver-auth=97,98' make -s -C "$M" integration-build DP_MDIR="$S/obj-hs" \
   MAAP_RTL="$C/hdl/ieee1722/maap/KL_maap.sv" VERILATOR="$V" VERILATOR_JOBS=$J) > "$OUT/hosted-shape-build.log" 2>&1
b=$?; echo "build rc=$b"; grep -E 'jobserver unavailable|non-files|empty|derivation' "$OUT/hosted-shape-build.log" | sort | uniq -c
[ $b -eq 0 ] && { (cd "$S/obj-hs" && ./maap_integration) > "$OUT/hosted-shape-run.log" 2>&1; echo "run rc=$?"; tail -1 "$OUT/hosted-shape-run.log"; }
