#!/usr/bin/env bash
# run_plant.sh NAME PLANTER : extract the exact head's port, suite and harness,
# apply plant NAME with PLANTER, run `make run` (elab, suite at 100/37/20,
# randomized harness at 1/2/3/37) at -j 2, print the failing checks.
set -u
P=$(cd "$(dirname "$0")/.." && pwd)
HEAD=527662d659b4ead97675744d12a43af1ea92b9b3
CLONE=$REVIEWS/r436-3-ppP2
name=$1; planter=$2
d=$P/scratch/plants/$name; rm -rf "$d"; mkdir -p "$d"
git -C "$CLONE" archive "$HEAD" hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
python3 "$planter" apply "$name" "$d/hdl/packet_engine/KL_pp_nvm_port.sv" || exit 3
sed -i 's/--build -j 0/--build -j 2/' "$d/tb/nvm_port/Makefile"
cd "$d/tb/nvm_port"
# keep going past a failed build so every bound is graded
make -k run VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator} > make.log 2>&1
rc=$?
echo "== $name rc=$rc"
grep -E '^(fuzz:|[0-9]+ checks:|FAIL)' make.log | sed -E 's/^(FAIL: FZ[0-9]+ .{0,60}).*\((.*)$/\1 ... (\2/' | cut -c1-260
