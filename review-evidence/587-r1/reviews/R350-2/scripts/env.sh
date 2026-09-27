# Reviewer reproduction environment for the #587 8x8 50 MHz default-flow run.
# Source with: REPO=<clean checkout at the reviewed head> PKT=<packet dir> VIVADO_BIN=<.../Vivado/bin>
#              LITEX_PYTHON=<litex venv python3> SDK=<verified rv32 sdk> . env.sh
: "${REPO:?}" "${PKT:?}" "${VIVADO_BIN:?}" "${LITEX_PYTHON:?}" "${SDK:?}"
export REPO LITEX_PYTHON SDK
export WORK="${WORK:-$PKT/scratch/work-default}"
export PATH="$VIVADO_BIN:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
LITEX_ENV_CC_TRIPLE="$(cd "$REPO" && PYTHONPATH=scripts python3 -c \
  'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
export LITEX_ENV_CC_TRIPLE
