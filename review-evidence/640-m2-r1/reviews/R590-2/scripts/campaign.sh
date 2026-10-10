#!/usr/bin/env bash
# R590-2 reviewer campaign: run the head's owning checks concurrently, each
# with its own log and rc file.
# Usage: campaign.sh CLONE LITEX_PYTHON VERILATOR OUTDIR TMPDIR
set -u
CLONE="$1"; LPY="$2"; VER="$3"; OUT="$4"; TMP="$5"
mkdir -p "$OUT" "$TMP"
export TMPDIR="$TMP" PYTHONDONTWRITEBYTECODE=1 MILAN_LITEX_PYTHON="$LPY"
cd "$CLONE" || exit 2
start() {  # name, command...
  local name="$1"; shift
  ( "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc" ) &
}
start lane_test "$LPY" -B sw/litex/test_retained_cdc_storage.py --jobs 8
start gen_check "$LPY" -B sw/litex/gen_mac_tx_model.py --check
start gen_check_plain python3 -B sw/litex/gen_mac_tx_model.py --check
start aggregate_selftest scripts/run_litex_sims.sh --selftest
start aggregate scripts/run_litex_sims.sh "$TMP/litex-sim-logs"
start gptp_txts make -C tb/verilator/gptp_txts VERILATOR="$VER" MILAN_LITEX_PYTHON="$LPY"
wait
echo campaign-done >"$OUT/DONE"
