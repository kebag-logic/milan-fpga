#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator DUT simulation harness for T1 BDD tests.
# Compiles the named KL_aecp_* module with Verilator and starts a UNIX-socket server.
# Used inside the dut-sim container (§5.2 of aem-aecp.md).
#
# Usage: run-dut-sim.sh <MODULE_NAME> [socket_path]
#   MODULE_NAME : KL_aecp_packet_validator | KL_aecp_l0_state | ...
#   socket_path : default /work/sock/aecp.sock

set -euo pipefail

MODULE="${1:-KL_aecp_packet_validator}"
SOCK="${2:-/work/sock/aecp.sock}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AECP_DIR="${REPO_ROOT}/hdl/ieee17221/aecp"
COMMON_DIR="${REPO_ROOT}/hdl/common"
BUILD_DIR="/tmp/verilator_${MODULE}"

echo "[dut-sim] Compiling ${MODULE} with Verilator..."
mkdir -p "${BUILD_DIR}"
verilator --cc --exe --build \
  --Mdir "${BUILD_DIR}" \
  --sv \
  "${AECP_DIR}/aecp_pkg.sv" \
  "${COMMON_DIR}/axi_stream_if.sv" \
  "${AECP_DIR}/${MODULE}.sv" \
  "${REPO_ROOT}/scripts/aecp_sim_main.cpp" \
  -CFLAGS "-I${REPO_ROOT}/scripts" \
  2>&1

echo "[dut-sim] Starting socket server on ${SOCK}..."
mkdir -p "$(dirname "${SOCK}")"
"${BUILD_DIR}/V${MODULE}" --socket "${SOCK}"
