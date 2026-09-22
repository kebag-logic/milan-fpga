#!/bin/sh
# R239: the focused ptp_ts suite at the exact head, on the verified pinned
# Verilator 5.050 selector, in the scratch export (never the review clone).
# Captures the suite log, its exit status, and the tally/verdict readings.
set -u
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
SRC=$VALIDATION_STORAGE/r239-372-r1-work/src
OUT=$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r1-r239/raw
LOG="$OUT/focused-ptp_ts.log"
"$V" --version > "$OUT/focused-tool.txt"
start=$(date +%s)
make -C "$SRC/tb/verilator/ptp_ts" VERILATOR="$V" > "$LOG" 2>&1
rc=$?
end=$(date +%s)
echo "make -C tb/verilator/ptp_ts VERILATOR=<pinned 5.050> exit=$rc wall=$((end - start))s" > "$OUT/focused-ptp_ts.exit"
python3 "$SRC/scripts/suite_tally.py" --verdict "$LOG" > "$OUT/focused-verdict.txt" 2>&1
echo "suite_tally --verdict exit=$?" >> "$OUT/focused-verdict.txt"
mkdir -p "$OUT/focused-tally/logs"
cp "$LOG" "$OUT/focused-tally/logs/ptp_ts.log"
python3 "$SRC/scripts/suite_tally.py" "$OUT/focused-tally/logs" > "$OUT/focused-tally/tally.txt" 2>&1
echo "suite_tally <dir> exit=$?" >> "$OUT/focused-tally/tally.txt"
cat "$OUT/focused-ptp_ts.exit"
