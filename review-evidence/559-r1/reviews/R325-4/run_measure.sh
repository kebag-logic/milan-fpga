#!/usr/bin/env bash
# Composition timing probe for issue 559 / PR 564 (R325-4).
# Usage: run_measure.sh <candidate-checkout> <source-checkout> <scratch-dir>
# Environment: LITEX_TREE, SDK_BIN, CCBIN as documented in measure_env.sh.
# Each run is bounded to 590 s so it fits one foreground call; a bounded
# 16-capture run keeps the rows it completed in capture.log.
set -u
here=$(cd "$(dirname "$0")" && pwd)
cand=$1; src=$2; scratch=$3
# shellcheck source=/dev/null
source "$here/measure_env.sh"
run() { # <checkout> <build-dir> <captures> <traffic>
  (cd "$1" && timeout 590 python3 tb/verilator/nvm_capture_cpu/run.py \
     --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures "$3" \
     --traffic "$4" --build-dir "$2"); echo "rc=$?"
}
# 1. Candidate, traffic ON, receipt's 16-capture build (bounded: rows 0-2 complete).
run "$cand" "$scratch/m-cand-8x8-50-on" 16 on
# 2. Candidate and source, traffic OFF, 2 captures each (same BIOS on both heads).
run "$cand" "$scratch/m-cand-8x8-50-off" 2 off
run "$src"  "$scratch/m-src-8x8-50-off" 2 off
R="$cand/tb/verilator/nvm_capture_cpu/measurements.json"
python3 "$here/compare_rows.py" "$R" cand-ON-vs-receipt "$scratch/m-cand-8x8-50-on/capture.log" endstation_ax7101_8x8 50000000 on
python3 "$here/compare_rows.py" "$R" cand-OFF2-vs-src-OFF2 "$scratch/m-cand-8x8-50-off/capture.log" endstation_ax7101_8x8 50000000 off "$scratch/m-src-8x8-50-off/capture.log"
