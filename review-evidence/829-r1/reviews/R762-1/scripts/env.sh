# Review environment: pinned Verilator first on PATH, pinned LiteX interpreter.
export PATH="$TOOLS/pinned-verilator-5.050:$PATH"  # TOOLS names the scoped tool root
export VERILATOR="$TOOLS/pinned-verilator-5.050/verilator"
export MILAN_LITEX_PYTHON=$HOME/litex-milan/venv/bin/python3
