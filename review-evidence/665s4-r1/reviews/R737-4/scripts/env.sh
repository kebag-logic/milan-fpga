# Review environment: the product LiteX venv, the gate environment's RV32 SDK, pinned Verilator 5.050, a bin holding only the system meson.
P=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export SDK=$HOME/br-milan-rv32/host LITEX_PY=$HOME/litex-milan/venv/bin
mkdir -p $P/scratch/meson-bin; ln -sf /usr/bin/meson $P/scratch/meson-bin/meson
export PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$LITEX_PY:$P/scratch/meson-bin:$SDK/bin:$PATH"
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
