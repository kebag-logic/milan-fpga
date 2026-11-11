# Environment for the review runs. Set these four before sourcing, to the product LiteX venv's python, the pinned
# RV32 SDK's bin directory, the pinned Verilator 5.050 wrapper and its VERILATOR_ROOT; R is this packet's directory.
: "${R:?packet directory}" "${PY:?LiteX venv python3}" "${RV32_BIN:?RV32 SDK bin directory}"
: "${VERILATOR_WRAPPER:?pinned Verilator 5.050 wrapper}" "${VERILATOR_ROOT:?its VERILATOR_ROOT}"
mkdir -p "$R/scratch/bin" && ln -sf "$VERILATOR_WRAPPER" "$R/scratch/bin/verilator"
export R PY VERILATOR_ROOT
export PATH=$R/scratch/bin:$RV32_BIN:$PATH
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
