#!/bin/sh
# Run selected parent consumer commands (the 12 argument vectors published in
# the round-3 author evidence, consumer/results.json) in a scratch parent copy
# at 7eb3b0d4 carrying receipts/50-parent-consumer.patch and the processor
# gitlink staged at 83c84b19. Usage: 50-parent-consumer.sh <parent> <n>...
# Environment: VERILATOR_BIN_DIR is prepended to PATH (pinned 5.050 shim).
set -u
PARENT=$1; shift
PKT=$(cd "$(dirname "$0")/.." && pwd)
OUT=$PKT/receipts/50-consumer
mkdir -p "$OUT"
export PATH="$VERILATOR_BIN_DIR:$PATH"
cd "$PARENT" || exit 2
for n in "$@"; do
  case $n in
    01) set -- python3 scripts/check_cpp_idiom.py ;;
    02) set -- python3 scripts/check_py_idiom.py ;;
    03) set -- python3 scripts/xvlog_gate.py --check ;;
    04) set -- python3 scripts/check_rtl_source_lists.py ;;
    05) set -- python3 scripts/pp_srcs.py --check --selftest ;;
    06) set -- python3 sw/builder/test_builder.py ;;
    07) set -- make -C tb/verilator/pp_shadow -j8 ;;
    08) set -- python3 scripts/check_port_contracts.py ;;
    09) set -- python3 scripts/measure_naming.py --check ;;
    10) set -- python3 scripts/measure_test_evidence.py --check ;;
    11) set -- python3 scripts/docs_check.py ;;
    12) set -- python3 scripts/lint_rtl.py --check ;;
    *) echo "unknown $n"; exit 2 ;;
  esac
  t0=$(date +%s)
  ${CMD_TIMEOUT:+timeout $CMD_TIMEOUT} "$@" > "$OUT/$n.log" 2>&1
  rc=$?
  t1=$(date +%s)
  sed -i "s#$PKT#<packet>#g; s#$HOME#~#g" "$OUT/$n.log"
  echo "$n rc=$rc seconds=$((t1 - t0)) argv: $*" | tee -a "$OUT/results.txt"
done
