# The product environment for this round's probes. Set PACKET, LITEX_VENV, SDK_BIN, VERILATOR_DIR and SV2V_DIR first.
export PATH="$VERILATOR_DIR:$SV2V_DIR:$SDK_BIN:$LITEX_VENV/bin:$PATH"
export LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
# A private copy of pythondata_cpu_vexiiriscv, so a netlist the cache lacks never lands in a shared tree.
export PYTHONPATH="$PACKET/scratch/vexii-copy"
