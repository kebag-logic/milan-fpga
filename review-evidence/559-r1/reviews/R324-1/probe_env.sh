# R324-1 probe environment. Source it; it only sets variables.
# Override the four inputs for another host. Defaults are this review host's.
#   PKT            this packet directory (the scratch/ tree lives under it)
#   LITEX_ENV_DIR  the existing product LiteX checkout set (read, never written)
#   SDK_BIN        pinned RV32 SDK bin directory holding riscv32-linux-gcc
#   VERILATOR_BIN  directory holding the scoped Verilator 5.050
PKT=${PKT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
LITEX_ENV_DIR=${LITEX_ENV_DIR:-$HOME/litex-milan}
SDK_BIN=${SDK_BIN:?set SDK_BIN to the pinned RV32 SDK bin directory}
VERILATOR_BIN=${VERILATOR_BIN:?set VERILATOR_BIN to the scoped Verilator 5.050 directory}
E=$PKT/scratch/env
# Scratch COPIES of the LiteX packages and a symlink overlay of the CPU netlist
# cache (probe_setup.sh) shadow the shared editable installs, so a missing
# netlist fails (no generator tree in the overlay) instead of writing into it.
export PYTHONPATH=$E/litex:$E/litedram:$E/litespi:$E/liteeth:$E/pythondata-software-picolibc:$E/pythondata-software-compiler_rt:$E/pythondata-cpu-vexiiriscv
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LITEX_ENV_CC_TRIPLE=$SDK_BIN/riscv32-linux
export PATH=$SDK_BIN:$VERILATOR_BIN:$LITEX_ENV_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
