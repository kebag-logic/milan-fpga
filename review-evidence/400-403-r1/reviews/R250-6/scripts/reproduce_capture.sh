#!/usr/bin/env bash
# Reproduce one nvm_capture_cpu arm per tb/verilator/nvm_capture_cpu/README.md.
# Usage: reproduce_capture.sh <repo> <shape> <cpu_hz> <on|off> <build_dir> <log>
# Environment overrides: LITEX_VENV (python venv with the pinned LiteX tree),
# SDK_BIN (RV32 SDK bin directory). Runs with networking disabled.
set -euo pipefail
repo=$1 shape=$2 cpu_hz=$3 traffic=$4 build=$5 log=$6
: "${LITEX_VENV:=$HOME/litex-milan/venv}"
: "${SDK_BIN:=$HOME/br-milan-rv32/host/bin}"
# Shim first: python3 must import LiteX (the BIOS Makefile calls python3 -m litex...),
# and the SDK's env-python meson would then lack mesonbuild, so meson is the host one.
# The SDK bin follows, supplying the pinned RV32 compiler.
shim=$(dirname "$build")/pathshim
mkdir -p "$shim"
rm -f "$shim/python3"   # a symlink would lose the venv's pyvenv.cfg lookup
printf '#!/bin/sh\nexec "%s/bin/python3" "$@"\n' "$LITEX_VENV" > "$shim/python3"
chmod +x "$shim/python3"
ln -sf /usr/bin/meson "$shim/meson"
export PATH="$shim:$SDK_BIN:$PATH"
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
cd "$repo"
{
  echo "START $(date -u +%FT%TZ) head=$(git rev-parse HEAD) shape=$shape cpu_hz=$cpu_hz traffic=$traffic"
  verilator --version
  meson -v; command -v python3 meson ninja riscv32-linux-gcc
  riscv32-linux-gcc --version | head -1
  set +e
  unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape "$shape" \
    --cpu-hz "$cpu_hz" --captures 16 --traffic "$traffic" --build-dir "$build"
  rc=$?
  set -e
  echo "EXIT $rc $(date -u +%FT%TZ)"
} > "$log" 2>&1
