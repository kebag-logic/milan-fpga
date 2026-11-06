# Probe environment, sourced. P is this packet's root; VERILATOR_DIR holds the pinned 5.050 binary.
export SDK=$HOME/br-milan-rv32/host
export LITEX_PY=$HOME/litex-milan/venv/bin
mkdir -p "$P/scratch/meson-bin"; ln -sf /usr/bin/meson "$P/scratch/meson-bin/meson"
export PATH="${VERILATOR_DIR:?set VERILATOR_DIR}:$LITEX_PY:$P/scratch/meson-bin:$SDK/bin:$PATH"
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
