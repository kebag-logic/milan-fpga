# environment for the reviewer's runs (sourced)
export MILAN_RV32_CC=${MILAN_RV32_CC:-$P/scratch/rv32sdk/bin/riscv32-linux-gcc}
export PATH=${R849_VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}:$PATH
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
