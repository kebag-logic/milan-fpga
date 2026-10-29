# Lane environment for the #803 gPTP adoption, round 2 (sourced by every gate command).
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR_JOBS=2
export PYTHONHASHSEED=0
export PYTHON_CPU_COUNT=4
export MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host/bin/riscv32-linux-gcc
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
export TMPDIR=$VALIDATION_STORAGE/scratch/803-a693b/tmp
mkdir -p "$TMPDIR"
