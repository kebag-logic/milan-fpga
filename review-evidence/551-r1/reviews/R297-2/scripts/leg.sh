#!/bin/sh
# Build and run the milan_dp obj_crflic leg in a disposable Mdir.
# usage: leg.sh <clone> <label> [DP_SRC] ; env VERILATOR, JOBS, PACKET
# Writes receipts/<label>.build.log, receipts/<label>.run.log, receipts/<label>.rc
set -u
CLONE=$1; LABEL=$2; DPSRC=${3:-}
PACKET=${PACKET:-$REVIEWS/551-r297-2-packet}
JOBS=${JOBS:-8}
MDIR=$PACKET/scratch/obj_$LABEL
R=$PACKET/receipts
mkdir -p "$R"
rm -rf "$MDIR"
cd "$CLONE/tb/verilator/milan_dp" || exit 2
if [ -n "$DPSRC" ]; then
  make -s crflic-build VERILATOR="$VERILATOR" VERILATOR_JOBS="$JOBS" CRFLIC_MDIR="$MDIR" DP_SRC="$DPSRC" \
    > "$R/$LABEL.build.log" 2>&1
else
  make -s crflic-build VERILATOR="$VERILATOR" VERILATOR_JOBS="$JOBS" CRFLIC_MDIR="$MDIR" \
    > "$R/$LABEL.build.log" 2>&1
fi
brc=$?
echo "build_rc=$brc" > "$R/$LABEL.rc"
if [ $brc -ne 0 ] || [ ! -x "$MDIR/Vmilan_dp_crflic" ]; then
  tail -40 "$R/$LABEL.build.log"; exit 3
fi
"$MDIR/Vmilan_dp_crflic" >"$R/$LABEL.run.log" 2>&1
rrc=$?
echo "run_rc=$rrc" >> "$R/$LABEL.rc"
echo "fail_lines=$(grep -c '^\s*\[FAIL\]' "$R/$LABEL.run.log")" >> "$R/$LABEL.rc"
tail -4 "$R/$LABEL.run.log" >> "$R/$LABEL.rc"
cat "$R/$LABEL.rc"
