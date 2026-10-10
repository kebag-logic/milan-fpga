# Source me: the pinned LiteX stack via pinned_py.sh, pinned Verilator on PATH.
K="${K:-$REVIEWS/640-m2-r591-2-packet}"
export PINS="${PINS:-$K/scratch/pins}" BASEPY="${BASEPY:?set BASEPY to a Python with the remaining LiteX dependencies}"
export MILAN_LITEX_PYTHON="$K/scripts/pinned_py.sh"
export PATH="$K/scratch/bin:$PATH" TMPDIR="$K/scratch/tmp" PYTHONDONTWRITEBYTECODE=1
