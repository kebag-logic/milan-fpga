#!/usr/bin/env bash
# Spot checks of the bench's "nearest passing case" choices, Verilator lint with
# scripts/lint_hdl.sh's flags. Usage: nearest_probe.sh <head-tree>  (verilator on PATH)
set -u; cd "$1" || exit 2
SRC="$(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)"
for c in "KL_aecp_resp_buf RESP_BYTES_P=17" "KL_aecp_resp_buf RESP_BYTES_P=20" "KL_aecp_resp_buf RESP_BYTES_P=23" "KL_aecp_resp_buf RESP_BYTES_P=24" \
         "KL_aecp_nvm_writer RS_TMO_CYC_P=1" "KL_aecp_nvm_writer RS_AGG_CYC_P=1" "KL_acmp_nvm_shadow RS_TMO_CYC_P=1" \
         "KL_aecp_desc_store NAME_ENTRIES_P=0" "protocol_processor_top N_AVB_IF_P=0"; do
  set -- $c
  out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module $1 -G$2 $SRC 2>&1)
  echo "$1 $2 rc=$? :: $(grep -m1 '^%' <<<"$out")"
done
