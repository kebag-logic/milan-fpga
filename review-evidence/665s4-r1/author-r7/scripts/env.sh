# Lane S4 round 7 gate environment (sourced). The product LiteX venv, the gate environment's RV32 SDK (not the
# pinned build: round 6's finding, still open with the manager), a scratch bin holding only a link to the system
# meson ahead of the SDK's shim. The gates run on a clean clone of the committed head.
export SDK=$WORKSPACE_HOME/br-milan-rv32/host
export LITEX_PY=$WORKSPACE_HOME/litex-milan/venv/bin
export SCRATCH=$VALIDATION_STORAGE/scratch/665s4-a698h
export OUT=$MANAGEMENT/2026-09-23/665s4-a698h
export GATE_PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$LITEX_PY:$SCRATCH/meson-bin:$SDK/bin"
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
