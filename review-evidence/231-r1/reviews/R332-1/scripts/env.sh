# Environment for the recipe reproduction. Set PACKET to this packet's root,
# VIVADO_BIN to the Vivado 2026.1 bin directory and LITEX_PYTHON to the LiteX
# environment interpreter before sourcing. REPO is the clean checkout at the
# head under review; WORK is the external build directory; SDK is the
# verified RV32 SDK installed by scripts/ci_rv32_sdk.py.
P="${PACKET:?set PACKET}"
export REPO="$P/scratch/clean"
export WORK="$P/scratch/work"
export LITEX_PYTHON="${LITEX_PYTHON:?set LITEX_PYTHON}"
export SDK="$P/scratch/sdk"
export PATH="${VIVADO_BIN:?set VIVADO_BIN}:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
