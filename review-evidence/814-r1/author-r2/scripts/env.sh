# Lane environment for #814 (sourced by every gate command): pinned Verilator 5.050, sv2v v0.0.12,
# GNU Make 4.3, tsn-gen at the CI pin, the RV32 SDK, scratch TMPDIR.
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR_JOBS=4
export PYTHONHASHSEED=0
export PYTHON_CPU_COUNT=8
export MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host/bin/riscv32-linux-gcc
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
export TMPDIR=$VALIDATION_STORAGE/scratch/814-a703b/tmp
mkdir -p "$TMPDIR"
