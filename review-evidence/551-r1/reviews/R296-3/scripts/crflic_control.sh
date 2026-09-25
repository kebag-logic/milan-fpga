#!/bin/sh
# R296-3: rebuild the obj_crflic leg at the head with the processor at a given
# commit, in a disposable tree, and run it once. Never writes the source clone.
# Usage: crflic_control.sh <source clone> <scratch dir> <processor commit> <log>
# Env: VERILATOR (pinned 5.050 wrapper), VERILATOR_JOBS (default 4).
set -eu
SRC=$1 WORK=$2 PP=$3 LOG=$4
rm -rf "$WORK"
mkdir -p "$WORK"
git -C "$SRC" archive HEAD | tar -x -C "$WORK"
for sm in gptp-processor third_party/verilog-axis; do
  rev=$(git -C "$SRC" ls-tree HEAD "$sm" | awk '{print $3}')
  rm -rf "${WORK:?}/$sm"
  git clone -q --no-checkout "$SRC/$sm" "$WORK/$sm"
  git -C "$WORK/$sm" checkout -q "$rev"
done
rm -rf "$WORK/protocol-processor"
git clone -q --no-checkout "$SRC/protocol-processor" "$WORK/protocol-processor"
git -C "$WORK/protocol-processor" checkout -q "$PP"
{
  echo "head=$(git -C "$SRC" rev-parse HEAD) processor=$(git -C "$WORK/protocol-processor" rev-parse HEAD)"
  "$VERILATOR" --version
} > "$LOG"
cd "$WORK/tb/verilator/milan_dp"
set +e
make crflic VERILATOR="$VERILATOR" VERILATOR_JOBS="${VERILATOR_JOBS:-4}" \
  CRFLIC_MDIR=obj_crflic_ctl >> "$LOG" 2>&1
rc=$?
echo "make crflic rc=$rc" >> "$LOG"
exit 0
