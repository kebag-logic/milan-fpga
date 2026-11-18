# Environment for the harness image builds (sourced): the LiteX venv, the verified pinned RV32 SDK extracted under the
# packet's scratch, the pinned Verilator and sv2v. PACKET defaults to this script's packet; TOOLS to the shared tools.
PACKET=${PACKET:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
TOOLS=${TOOLS:-$VALIDATION_TOOLS}
export PATH=$HOME/litex-milan/venv/bin:$PACKET/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1/bin:$TOOLS/pinned-verilator-5.050:$TOOLS/sv2v-v0.0.12:$PATH
export VERILATOR=$TOOLS/pinned-verilator-5.050/verilator LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true MAKEFLAGS="-j2 --no-print-directory"
