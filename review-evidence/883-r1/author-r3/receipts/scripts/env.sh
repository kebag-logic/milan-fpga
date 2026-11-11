# Lane environment for #883 (A768): the recipe's pinned tools; TMPDIR in scratch, outside the tree.
export PYTHONHASHSEED=0
export TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export PATH=<scratch-root>/a662/make43/bin:<tools>/sv2v-v0.0.12:<tools>/pinned-verilator-5.050:$PATH
export RV32_SDK=<scratch>/sdk
export MILAN_RV32_CC=$RV32_SDK/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=<tools>/gtest-1.14.0/lib/pkgconfig LD_LIBRARY_PATH=<tools>/gtest-1.14.0/lib
export TMPDIR=<scratch>/tmp
mkdir -p "$TMPDIR"
