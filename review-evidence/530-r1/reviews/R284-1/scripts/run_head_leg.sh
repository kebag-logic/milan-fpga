#!/bin/sh
# Build and run the obj_crflic leg (and optionally its mutant campaign) at the
# checked-out head. Usage:
#   REPO=/path/to/clone VERILATOR=/path/to/verilator-5.050 OUT=/path/to/receipts \
#     sh run_head_leg.sh [leg|mutants]
# At most 8 parallel compile jobs. Logs go to $OUT.
set -eu
: "${REPO:?}" "${VERILATOR:?}" "${OUT:?}"
what="${1:-leg}"
mkdir -p "$OUT"
export VERILATOR VERILATOR_JOBS=8
export TMPDIR="${TMPDIR:-$OUT}"
cd "$REPO"
{
  echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
  git submodule status protocol-processor third_party/verilog-axis gptp-processor
  "$VERILATOR" --version
} > "$OUT/identity_$what.txt"
case "$what" in
  leg)
    start=$(date +%s)
    set +e
    make -C tb/verilator/milan_dp crflic > "$OUT/crflic_head.log" 2>&1
    rc=$?
    set -e
    echo "rc=$rc wall_s=$(( $(date +%s) - start ))" >> "$OUT/crflic_head.log"
    ;;
  mutants)
    start=$(date +%s)
    set +e
    make -C tb/verilator/milan_dp crflic-mutants > "$OUT/crflic_mutants.log" 2>&1
    rc=$?
    set -e
    echo "rc=$rc wall_s=$(( $(date +%s) - start ))" >> "$OUT/crflic_mutants.log"
    ;;
  *) echo "unknown: $what" >&2; exit 2 ;;
esac
exit "$rc"
