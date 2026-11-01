export PATH=${TOOLS:?}/pinned-verilator-5.050:${TOOLS:?}/sv2v-v0.0.12:$PATH
export PATH=${PACKET:?}/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1/bin:$HOME/litex-milan/venv/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
