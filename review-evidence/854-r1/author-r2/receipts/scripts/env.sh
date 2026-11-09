# Lane environment for #854 round 2: the recipe's tools; scratch TMPDIR outside the tree.
export PYTHONHASHSEED=0
export TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/854-a756/sdk/br-milan-rv32/host/bin/riscv32-linux-gcc
export TMPDIR=$VALIDATION_STORAGE/scratch/854-a756b/tmp
mkdir -p "$TMPDIR"
