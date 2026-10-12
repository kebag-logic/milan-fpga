#!/bin/sh
# The three focused suites R558-12 ran at the exact head, concurrently.
# Usage: run_suites.sh <checkout> <out dir> <verilator>
# Each suite writes <out>/<name>.log and <out>/<name>.rc. Build outputs land in
# the suites' ignored obj_* directories (MAAP's in <out>/obj_maap); remove them
# afterwards and confirm `git status --short --ignored` matches its prior state.
TREE=$1; OUT=$2; V=$3
mkdir -p "$OUT"
( cd "$TREE/tb/verilator/maap" && make all VERILATOR="$V" VERILATOR_JOBS=4 MDIR="$OUT/obj_maap" \
    > "$OUT/maap_all.log" 2>&1; echo $? > "$OUT/maap_all.rc" ) &
( cd "$TREE/tb/verilator/csr" && make -j6 run VERILATOR="$V" \
    > "$OUT/csr_run.log" 2>&1; echo $? > "$OUT/csr_run.rc" ) &
( cd "$TREE/tb/verilator/milan_dp" && make -j6 run VERILATOR="$V" VERILATOR_JOBS=2 \
    > "$OUT/milan_dp_run.log" 2>&1; echo $? > "$OUT/milan_dp_run.rc" ) &
wait
