# Firmware gate environment for #806 (sourced after env.sh): the pinned RV32 SDK this session installed with
# scripts/ci_rv32_sdk.py --archive and verified (the earlier shared copy was removed mid-run), GoogleTest / GoogleMock
# 1.14.0 (the runner's version) and Clang 18, as the #780 lane ran the firmware block.
export MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export PATH=$VALIDATION_TOOLS/clang-18/bin:$PATH
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
