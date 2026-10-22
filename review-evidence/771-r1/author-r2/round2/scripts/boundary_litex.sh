#!/usr/bin/env bash
# boundary_litex.sh OUTDIR: ctrl_boundary.py --require-rv32 --selftest under a
# LiteX interpreter whose seven packages are at sw/litex/litex_pins.txt's
# revisions (the hosted job pip-installs those pins into its python3).
set -u
out="$1"
source $VALIDATION_STORAGE/scratch/a662/env.sh
export MILAN_RV32_CC=$VALIDATION_STORAGE/771-a662-r2/rv32-sdk/host/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$VALIDATION_TOOLS/clang-18/bin:$PATH
unset MAKEFLAGS
cd $LANES/771-pin4 || exit 2
PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
{ echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)"; echo "python=$PY $($PY --version)"; date -Is; } > "$out/ctrl_boundary_litex.env"
t0=$SECONDS
"$PY" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest > "$out/ctrl_boundary_litex.log" 2>&1
echo $? > "$out/ctrl_boundary_litex.rc"
echo $((SECONDS - t0)) > "$out/ctrl_boundary_litex.seconds"
echo "head_after=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$out/ctrl_boundary_litex.env"
