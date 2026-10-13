# Reviewer environment for R582-1 (portable: override the variables to re-run elsewhere).
: "${REPO:=$REVIEWS/r582-1-665f3b}"
: "${PACKET:=$REVIEWS/665f3b-r582-1-packet}"
: "${PY:=$REVIEWS/665f3b-r582-1-packet/scratch/venv312/bin/python3}"
: "${MILAN_RV32_CC:=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-buildroot-linux-gnu-gcc}"
: "${VERILATOR:=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
export REPO PACKET PY MILAN_RV32_CC VERILATOR
export TMPDIR="$PACKET/scratch/tmp"
export WORK="$PACKET/scratch/work"
