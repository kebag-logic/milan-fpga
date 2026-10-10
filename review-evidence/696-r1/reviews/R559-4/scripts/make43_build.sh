#!/bin/sh
# Usage: make43_build.sh <clone> <make-binary-dir> <scratchdir> <outdir>
# (1) head: the suite's own integration-build target, invoked exactly as
#     mutants.py invokes it (make -j8 -s -C <suite> integration-build ...), under
#     inherited MAKEFLAGS=w, with the given make first on PATH.
# (2) remedy probe: a disposable copy of integration.mk whose two captures also
#     clear MAKEFLAGS (the pp_shadow / milan_dp_mclk / milan_dp_render pattern),
#     built from a -j8 recursive parent under MAKEFLAGS=w, then run.
set -u
C=$1; MB=$2; S=$3; OUT=$4; M=$C/tb/verilator/maap
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH="$MB:$PATH"; mkdir -p "$S"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
rm -rf "$S/obj-head43"
(cd / && env MAKEFLAGS=w make -j8 -s -C "$M" integration-build DP_MDIR="$S/obj-head43" \
   MAAP_RTL="$C/hdl/ieee1722/maap/KL_maap.sv" VERILATOR="$V" VERILATOR_JOBS=8) > "$OUT/make43-head-integration.log" 2>&1
echo "head integration-build rc=$?"
grep -E 'non-files|jobserver' "$OUT/make43-head-integration.log" | head -3
sed 's/\$(shell \$(MAKE) -s --no-print-directory/$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory/' "$M/integration.mk" > "$S/remedy.mk"
printf 'all:\n\t+$(MAKE) -s -C %s -f %s build DP_MDIR=%s MAAP_RTL=%s VERILATOR=%s VERILATOR_JOBS=8\n' \
  "$M" "$S/remedy.mk" "$S/obj-remedy43" "$C/hdl/ieee1722/maap/KL_maap.sv" "$V" > "$S/remedy-parent.mk"
rm -rf "$S/obj-remedy43"
(cd / && env MAKEFLAGS=w make -j8 -s -f "$S/remedy-parent.mk") > "$OUT/make43-remedy-integration.log" 2>&1
b=$?; echo "remedy build rc=$b"
if [ $b -eq 0 ]; then (cd "$S/obj-remedy43" && ./maap_integration) > "$OUT/make43-remedy-run.log" 2>&1; echo "remedy run rc=$?"; tail -1 "$OUT/make43-remedy-run.log"; fi
