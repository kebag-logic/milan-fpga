# Needs: P=<this packet directory>, VERILATOR_DIR=<pinned Verilator 5.050 directory>; LiteX venv in $HOME/litex-milan, RV32 SDK in $HOME/br-milan-rv32.
# Probe environment (sourced): product LiteX venv, the local RV32 SDK, pinned Verilator, system meson ahead of the SDK shim.
P=${P:?set P to the packet directory}
mkdir -p "$P/scratch/meson-bin"; ln -sf "$(command -v meson)" "$P/scratch/meson-bin/meson"
export PATH="${VERILATOR_DIR:?set VERILATOR_DIR to the pinned Verilator 5.050 directory}:$HOME/litex-milan/venv/bin:$P/scratch/meson-bin:$HOME/br-milan-rv32/host/bin:$PATH"
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
