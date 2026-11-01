# Environment for this review's commands. Set MILAN_LITEX_PYTHON and VERILATOR for the host first.
export MILAN_LITEX_PYTHON="${MILAN_LITEX_PYTHON:?the pinned LiteX interpreter}"
export VERILATOR="${VERILATOR:?a Verilator 5.050 wrapper}"
export PATH="$(dirname "$VERILATOR"):$PATH"
