#!/bin/sh
export TREE OUT VERILATOR=${VERILATOR:?pinned 5.050 wrapper} VERILATOR_JOBS=8 PYTHONDONTWRITEBYTECODE=1
export PATH=$(dirname "$VERILATOR"):$PATH
R=$(dirname "$0")/run_probe.sh
rm -rf "$S/cap"
"$R" cap-1 python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$S/cap" -- python3 tb/verilator/input_loopback_dp/run.py --shape 1 --work "$S/cw1" --build-only
"$R" cap-8 python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$S/cap" -- python3 tb/verilator/input_loopback_dp/run.py --shape 8 --work "$S/cw8" --build-only
"$R" registry-probe python3 "$(dirname "$0")/registry_probe.py" "$TREE" "$S/cap"
