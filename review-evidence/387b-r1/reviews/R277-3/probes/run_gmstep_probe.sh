#!/bin/sh
# Build and run the milan_dp gmstep leg in a disposable tree copy with one
# probe mutation planted. Usage: run_gmstep_probe.sh <pristine-tree> <work-tree> <probe>
set -eu
src=$1; work=$2; probe=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$work"; cp -a "$src" "$work"
rm -rf "$work/tb/verilator/milan_dp/obj_"* "$work/tb/verilator/tkdiag/obj_dir"
python3 "$here/plant.py" "$work" "$probe"
cd "$work/tb/verilator/milan_dp"
set +e
make gmstep VERILATOR="${VERILATOR:-verilator}"
echo "make-rc=$?"
