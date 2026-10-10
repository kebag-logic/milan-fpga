# Reviewer environment (source it): the pinned Verilator 5.050 wrapper first
# on PATH and the pinned RV32 SDK compiler. Set TOOLS to the directory holding
# pinned-verilator-5.050/ and bootlin-504-probe/ (the #504 SDK, archive
# sha256 d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f).
: "${TOOLS:?set TOOLS to the pinned tool directory}"
export PATH="$TOOLS/pinned-verilator-5.050:$PATH"
export MILAN_RV32_CC="$TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc"
