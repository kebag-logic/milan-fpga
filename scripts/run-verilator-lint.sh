#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run Verilator lint on all AECP RTL modules.
# Usage: ./scripts/run-verilator-lint.sh [--strict]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AECP_DIR="${REPO_ROOT}/hdl/aecp"
COMMON_DIR="${REPO_ROOT}/hdl/common"
ADP_DIR="${REPO_ROOT}/hdl/adp"

STRICT=${1:-""}
FLAGS="--lint-only --sv"
if [[ "${STRICT}" == "--strict" ]]; then
  FLAGS="${FLAGS} -Wall"
fi

MODULES=(
  KL_aecp_packet_validator
  KL_aecp_common_parser
  KL_aecp_l0_state
  KL_aecp_timers
  KL_aecp_cmd_specific_extract
  KL_aecp_accessor
  KL_aecp_aem_store
  KL_aecp_nv_overlay
  KL_aecp_aem_dyn_mux
  KL_aecp_unsolicited_table
  KL_aecp_vu_milan
  KL_aecp_response_builder
  KL_aecp_egress_mux
)

PASS=0
FAIL=0
for MOD in "${MODULES[@]}"; do
  echo -n "Linting ${MOD}... "
  if verilator ${FLAGS} \
      "${AECP_DIR}/aecp_pkg.sv" \
      "${COMMON_DIR}/axi_stream_if.sv" \
      "${AECP_DIR}/${MOD}.sv" 2>&1 | grep -q "^%Error"; then
    echo "FAIL"
    FAIL=$((FAIL+1))
    verilator ${FLAGS} \
      "${AECP_DIR}/aecp_pkg.sv" \
      "${COMMON_DIR}/axi_stream_if.sv" \
      "${AECP_DIR}/${MOD}.sv" 2>&1 | grep "^%Error" || true
  else
    echo "OK"
    PASS=$((PASS+1))
  fi
done

echo ""
echo "Lint results: ${PASS} OK, ${FAIL} FAIL"
[[ ${FAIL} -eq 0 ]]
