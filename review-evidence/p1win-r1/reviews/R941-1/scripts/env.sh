# Environment for the R941-1 focused runs (sourced). Set CLONE (the detached clone at the head under review) and
# PKT (this packet) before sourcing; the tool paths are this host's pinned ones, adjust to reproduce.
: "${CLONE:?set CLONE to the clone at 85569e241625d8e4176aae7d77c524783dff30cd}"
: "${PKT:?set PKT to this packet directory}"
export CLONE PKT
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export LPY=$HOME/litex-milan/venv/bin/python3
