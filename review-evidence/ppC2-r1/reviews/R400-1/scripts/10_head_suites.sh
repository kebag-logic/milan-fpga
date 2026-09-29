#!/usr/bin/env bash
# Exact-head focused suites: tb/maap, tb/rx_validator, tb/pp_top maap-internal,
# plus the tool identity. Receipts: receipts/head-*.log, receipts/tool-identity.txt
source "$(dirname "$0")/common.sh"
{
  echo "verilator wrapper: $VERILATOR"
  "$VERILATOR" --version
  sha256sum "$VERILATOR"
  sed -n 's/.*VERILATOR_ROOT=\([^ ]*\) \([^ ]*\) .*/\2/p' "$VERILATOR" | xargs -r sha256sum
  echo "clone HEAD: $(git -C "$CLONE" rev-parse HEAD) tree: $(git -C "$CLONE" rev-parse 'HEAD^{tree}')"
  g++ --version | head -1; python3 --version
} >"$RECEIPTS/tool-identity.txt" 2>&1
T=$SCRATCH/head
export_tree "$T"
run_target "$T" maap run "$RECEIPTS/head-maap-run.log"
run_target "$T" rx_validator run "$RECEIPTS/head-rx_validator-run.log"
run_target "$T" pp_top maap-internal "$RECEIPTS/head-pp_top-maap-internal.log"
