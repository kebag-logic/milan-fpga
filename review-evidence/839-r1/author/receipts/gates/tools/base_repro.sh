#!/usr/bin/env bash
# base_repro.sh <head sha>: the head's bootsa leg built against the BASE milan_datapath.sv (dev 604899c0), so the
# defect is shown by the same leg that grades the fix. Build through the Makefile's own recipe into a scratch Mdir.
set -u
H=$1; B=604899c08ff1cd1830e1dd08b733109ef852400c
S=$VALIDATION_STORAGE/839-a731; W=$S/gates/lane-wt-${H:0:8}; G=$S/gates/lane-logs-${H:0:8}; M=$S/gates/base-repro
T=$MANAGEMENT/2026-09-23/839-a731/receipts/gates/tools
[ -d "$W" ] || "$T/clone_at.sh" "$H" "$W" || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
mkdir -p "$M" "$G"
git show "$B:hdl/milan/milan_datapath.sv" > "$M/milan_datapath_base.sv"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/gates/tmp PYTHONHASHSEED=0 \
  TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory"
if [ "${2:-}" != run-only ]; then
  { echo "# head $H leg, base $B milan_datapath.sv (sha256 $(sha256sum < "$M/milan_datapath_base.sv" | cut -d' ' -f1))"
    make -C tb/verilator/milan_dp bootsa-build BOOTSA_MDIR="$M/obj" DP_SRC="$M/milan_datapath_base.sv"; } > "$G/base_repro_build.log" 2>&1
  echo $? > "$G/base_repro_build.rc"
fi
# run from the suite's directory, as the Makefile does: the ROM images are relative $readmemh files there
{ echo "# head $H leg, base $B milan_datapath.sv: expected to FAIL by the defect's checks"
  cd tb/verilator/milan_dp && "$M/obj/Vmilan_dp_bootsa" "$M/obj/aemi.bin"; } > "$G/base_repro_run.log" 2>&1
echo $? > "$G/base_repro_run.rc"
git status --porcelain > "$G/tree-after-base-repro.txt"
echo "build rc=$(cat "$G/base_repro_build.rc") run rc=$(cat "$G/base_repro_run.rc")"
