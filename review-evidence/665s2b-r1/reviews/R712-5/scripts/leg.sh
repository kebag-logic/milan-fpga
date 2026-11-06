#!/bin/sh
# Run one CPU budget harness leg at the reviewed head with the pinned Verilator first on PATH.
# usage: leg.sh <clean clone> <build dir> <pin dir> <litex root> run.py-args...
set -u
SRC=$1; B=$2; PIN=$3; L=$4; shift 4
PATH=$PIN:$PATH; export PATH
verilator --version
mkdir -p "$(dirname "$B")" && cd "$(dirname "$B")" && "$L/venv/bin/python3" -B "$SRC/tb/verilator/ctrl_service_budget/run.py" --build-dir "$B" "$@"
echo "rc=$?"
