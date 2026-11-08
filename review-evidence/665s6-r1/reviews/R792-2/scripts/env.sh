# Tool pins for this review's runs: pinned sv2v 0.0.12, system Yosys 0.66, scoped Verilator 5.050
export TOOLS=${TOOLS:?set TOOLS to the directory holding sv2v-v0.0.12 and pinned-verilator-5.050}
export PATH=$TOOLS/sv2v-v0.0.12:$TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR=$TOOLS/pinned-verilator-5.050/verilator
export PYTHONDONTWRITEBYTECODE=1
