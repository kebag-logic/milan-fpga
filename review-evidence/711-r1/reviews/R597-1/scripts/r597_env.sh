# Source with R597_PACKET set (default: this script's packet).
P=${R597_PACKET:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}
export TMPDIR=$P/scratch/tmp PYTHONDONTWRITEBYTECODE=1 MILAN_RV32_CC=$P/scratch/sdk/bin/riscv32-linux-gcc
