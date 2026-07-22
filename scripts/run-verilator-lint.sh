#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run Verilator lint on all AECP RTL modules.
# Usage: ./scripts/run-verilator-lint.sh [--strict]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AECP_DIR="${REPO_ROOT}/hdl/ieee17221/aecp"
COMMON_DIR="${REPO_ROOT}/hdl/common"
ADP_DIR="${REPO_ROOT}/hdl/ieee17221/adp"

STRICT=${1:-""}
FLAGS="--lint-only --sv"
if [[ "${STRICT}" == "--strict" ]]; then
  FLAGS="${FLAGS} -Wall"
fi

# The implemented AECP pipeline (the stubs cmd_specific_extract / nv_overlay /
# unsolicited_table / vu_milan / egress_mux were folded into the response
# builder + top and are no longer in the build). The generated ROM include
# (gen/aecp_aem_rom.svh) needs -Igen; the ingress imports adp_pkg.
GEN_DIR="${AECP_DIR}/gen"
INC="-I${AECP_DIR} -I${GEN_DIR} -I${COMMON_DIR}"
MODULES=(
  KL_aecp_packet_validator
  KL_aecp_common_parser
  KL_aecp_l0_state
  KL_aecp_timers
  KL_aecp_accessor
  KL_aecp_aem_store
  KL_aecp_aem_dyn_mux
  KL_aecp_response_builder
  KL_aecp_ingress
)

# regenerate the ROM include so the lint matches the model
python3 "${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}/avdecc/gen_aem_store.py" >/dev/null 2>&1 || true

PASS=0
FAIL=0
for MOD in "${MODULES[@]}"; do
  echo -n "Linting ${MOD}... "
  if verilator ${FLAGS} ${INC} \
      "${AECP_DIR}/aecp_pkg.sv" "${AECP_DIR}/../adp/adp_pkg.sv" \
      "${COMMON_DIR}/axi_stream_if.sv" \
      "${AECP_DIR}/KL_aecp_accessor.sv" \
      "${AECP_DIR}/${MOD}.sv" 2>&1 | grep -q "^%Error"; then
    echo "FAIL"; FAIL=$((FAIL+1))
    verilator ${FLAGS} ${INC} "${AECP_DIR}/aecp_pkg.sv" "${AECP_DIR}/../adp/adp_pkg.sv" \
      "${COMMON_DIR}/axi_stream_if.sv" "${AECP_DIR}/KL_aecp_accessor.sv" \
      "${AECP_DIR}/${MOD}.sv" 2>&1 | grep "^%Error" || true
  else
    echo "OK"; PASS=$((PASS+1))
  fi
done

# ACMP responder (stateless talker, hdl/ieee17221/acmp)
ACMP_DIR="${REPO_ROOT}/hdl/ieee17221/acmp"
echo -n "Linting KL_acmp_responder... "
if verilator ${FLAGS} "${ACMP_DIR}/acmp_pkg.sv" "${ACMP_DIR}/KL_acmp_responder.sv" \
    2>&1 | grep -q "^%Error"; then
  echo "FAIL"; FAIL=$((FAIL+1))
  verilator ${FLAGS} "${ACMP_DIR}/acmp_pkg.sv" "${ACMP_DIR}/KL_acmp_responder.sv" \
    2>&1 | grep "^%Error" || true
else
  echo "OK"; PASS=$((PASS+1))
fi

# full-hierarchy elaboration of KL_aecp_top (the integration check)
echo -n "Elaborating KL_aecp_top (full subsystem)... "
if verilator ${FLAGS} ${INC} --top-module KL_aecp_top \
    "${AECP_DIR}/aecp_pkg.sv" "${AECP_DIR}/../adp/adp_pkg.sv" \
    "${COMMON_DIR}/axi_stream_if.sv" \
    "${AECP_DIR}"/KL_aecp_packet_validator.sv "${AECP_DIR}"/KL_aecp_common_parser.sv \
    "${AECP_DIR}"/KL_aecp_l0_state.sv "${AECP_DIR}"/KL_aecp_timers.sv \
    "${AECP_DIR}"/KL_aecp_accessor.sv "${AECP_DIR}"/KL_aecp_aem_store.sv \
    "${AECP_DIR}"/KL_aecp_aem_dyn_mux.sv "${AECP_DIR}"/KL_aecp_response_builder.sv \
    "${AECP_DIR}"/KL_aecp_ingress.sv "${AECP_DIR}"/KL_aecp_top.sv 2>&1 | grep -q "^%Error"; then
  echo "FAIL"; FAIL=$((FAIL+1))
else
  echo "OK"; PASS=$((PASS+1))
fi

echo ""
echo "Lint results: ${PASS} OK, ${FAIL} FAIL"
[[ ${FAIL} -eq 0 ]]
