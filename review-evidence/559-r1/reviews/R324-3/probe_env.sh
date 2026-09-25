# R324-3 probe environment. Source it; it only sets variables.
# Inputs (defaults are this review host's; override for another host):
#   PKT            this packet directory (scratch/ lives under it)
#   SDK_BIN        pinned RV32 SDK bin directory holding riscv32-linux-gcc
#   VERILATOR_BIN  directory holding the scoped Verilator 5.050 wrapper
#   LITEX_ENV_DIR  product LiteX checkout set (only read; probe_setup copies it)
PKT=${PKT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
LITEX_ENV_DIR=${LITEX_ENV_DIR:-$HOME/litex-milan}
SDK_BIN=${SDK_BIN:?set SDK_BIN to the pinned RV32 SDK bin directory}
VERILATOR_BIN=${VERILATOR_BIN:?set VERILATOR_BIN to the scoped Verilator 5.050 directory}
E=$PKT/scratch/env
export PYTHONPATH=$E/litex:$E/migen:$E/litedram:$E/litespi:$E/liteeth:$E/pythondata-software-picolibc:$E/pythondata-software-compiler_rt:$E/pythondata-cpu-vexiiriscv
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=$SDK_BIN/riscv32-linux
export PATH=$SDK_BIN:$VERILATOR_BIN:$LITEX_ENV_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
# Verilator itself reads an exported VERILATOR_BIN as its binary name: never export it.
export -n VERILATOR_BIN SDK_BIN
