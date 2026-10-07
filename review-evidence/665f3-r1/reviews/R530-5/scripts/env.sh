# Environment for the R530-5 runs: the pinned SDK compiler and Verilator 5.050.
P=$REVIEWS/665f3-r530-5-packet
export TMPDIR=$P/scratch/tmp
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
