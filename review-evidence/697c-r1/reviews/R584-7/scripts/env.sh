# Source me: pinned RV32 SDK (installed from the verified archive by scripts/ci_rv32_sdk.py) and pinned Verilator.
export MILAN_RV32_CC="$PACKET/scratch/rv32sdk/bin/riscv32-linux-gcc"
export VERILATOR="${PINNED_VERILATOR:?the pinned Verilator 5.050}"
export PYTHONDONTWRITEBYTECODE=1
