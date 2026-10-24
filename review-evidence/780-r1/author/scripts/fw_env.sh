# Firmware gate environment for #780 (sourced after env.sh): the verified pinned RV32 SDK, GoogleTest / GoogleMock
# 1.14.0 (the runner's version) and Clang 18, as the #771 lane ran the firmware block.
export MILAN_RV32_CC=$VALIDATION_STORAGE/679-a557/sdk/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export PATH=$VALIDATION_TOOLS/clang-18/bin:$PATH
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
