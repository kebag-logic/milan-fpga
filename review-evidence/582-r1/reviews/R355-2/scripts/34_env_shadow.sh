#!/bin/bash
# Reviewer probe: does any environment input change the imported contract clock?
# (a) environment variables named like clocks; (b) a PYTHONPATH entry holding a
# regular package `tb` (the repository's `tb` is a namespace directory).
# Usage: 34_env_shadow.sh <tree> <scratch> [python]
set -u
T=${1:?tree}; X=${2:?scratch}; PY=${3:-python3}
rm -rf "$X"; mkdir -p "$X/shadow/tb/verilator/nvm_capture_cpu"
touch "$X/shadow/tb/__init__.py" "$X/shadow/tb/verilator/__init__.py" "$X/shadow/tb/verilator/nvm_capture_cpu/__init__.py"
echo "CPU_HZ = 100_000_000" > "$X/shadow/tb/verilator/nvm_capture_cpu/recipe.py"
cd "$T" || exit 2
q='import sys; sys.path.insert(0,"sw/builder"); import endstation_builder as eb; print("builder BAREMETAL_CLK_HZ", eb.BAREMETAL_CLK_HZ)'
echo "--- clean environment"; env -u PYTHONPATH "$PY" -c "$q"
echo "--- clock-like environment variables"; env CPU_HZ=1 BAREMETAL_CLK_HZ=1 MILAN_CLK_HZ=1 SYS_CLK_HZ=1 "$PY" -c "$q"
echo "--- PYTHONPATH with a regular tb package"; PYTHONPATH="$X/shadow" "$PY" -c "$q"
echo "--- the shipped 1x1 under that PYTHONPATH"
PYTHONPATH="$X/shadow" "$PY" sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml -o "$X/out" 2>&1 | tail -1
echo "--- the capture gate's own import of recipe"; grep -n "sys.path\|import recipe" scripts/check_nvm_capture.py | head -4
