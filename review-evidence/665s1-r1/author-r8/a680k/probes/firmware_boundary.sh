#!/bin/bash
# The hosted rtl-fast firmware-boundary job's steps after checkout and package installs, as the workflow
# runs them: the CPU-derived budgets, the RV32 SDK's self-test and its install and verification, then the
# TSN stack boundary over the firmware builders' compiles. Run from the checkout. LiteX and migen come from
# PYTHONPATH (the workflow pip-installs them). The SDK is installed from the pinned archive ($1, checked
# against the pinned digest) into a new destination ($2), as the installer requires of a local run; the
# host's own SDK tree carries no provenance receipt. The boundary then finds the SDK compiler as before.
set -euo pipefail
cpus="$(nproc)"
test "$cpus" -gt 0
export CI_BUILD_JOBS="$cpus"
export CI_TOOL_BUILD_JOBS=$(( cpus < 8 ? cpus : 8 ))
export CI_CAMPAIGN_JOBS=$(( cpus < 4 ? cpus : 4 ))
export VERILATOR_JOBS="$cpus"
export SIM_JOBS=$(( cpus < 4 ? cpus : 4 ))
export MAKEFLAGS="-j1 --no-print-directory"
git submodule status third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
dpkg-query -W libgtest-dev libgmock-dev 2>/dev/null || echo "GoogleTest from the host: $(ls /usr/include/gtest/gtest.h /usr/include/gmock/gmock.h)"
g++ --version | head -n 1
echo "+ python3 scripts/ci_rv32_sdk_selftest.py"
python3 scripts/ci_rv32_sdk_selftest.py
echo "+ python3 scripts/ci_rv32_sdk.py --destination <new> --archive <pinned archive>"
python3 scripts/ci_rv32_sdk.py --destination "$2" --archive "$1"
echo "+ python3 scripts/ci_rv32_sdk.py --destination <new> --verify-only"
python3 scripts/ci_rv32_sdk.py --destination "$2" --verify-only
echo "+ python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
