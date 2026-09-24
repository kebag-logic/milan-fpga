#!/bin/sh
# Build and run the milan_dp ownerless (option-off, sim_main.cpp) leg in a
# disposable tree copy; optionally plant one probe mutation first.
# Usage: run_optoff.sh <pristine-tree> <work-tree> [probe-name]
set -eu
src=$1; work=$2; probe=${3:-}
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$work"; cp -a "$src" "$work"
rm -rf "$work/tb/verilator/milan_dp/obj_"* "$work/tb/verilator/tkdiag/obj_dir"
if [ -n "$probe" ]; then python3 "$here/plant.py" "$work" "$probe"; fi
cd "$work/tb/verilator/milan_dp"
set +e
make option-off VERILATOR="${VERILATOR:-verilator}"
echo "make-rc=$?"
