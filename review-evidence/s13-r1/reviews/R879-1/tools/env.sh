# env.sh: the reviewer's tool environment (source it). PKT is the packet root.
# The RV32 SDK is the repository's pinned #504 Bootlin release (scripts/ci_rv32_sdk.py RELEASE/ARCHIVE_SHA256),
# extracted into the packet's scratch from a host copy whose sha256 equals the pin.
PKT=${PKT:-$REVIEWS/s13-r879-1-packet}
SDK=$PKT/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export HOME=$PKT/scratch/home TMPDIR=$PKT/scratch/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux
LITEX_VENV=${LITEX_VENV:?set LITEX_VENV to the LiteX virtualenv whose bin/ holds python3}
export PATH=$LITEX_VENV/bin:$V:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin:$SDK/bin
export MILAN_RV32_SDK=$SDK
