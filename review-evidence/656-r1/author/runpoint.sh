#!/bin/bash
# usage: runpoint.sh <dir> <logname>   runs the physical milan_dp_gptp leg with pinned 5.050
d=$1; L=$VALIDATION_STORAGE/656-a536/logs/$2
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cd "$d"
start=$(date +%s)
echo "start $(date -Is) dir=$d verilator=$(verilator --version)" > "$L.log"
make -C tb/verilator/milan_dp_gptp >> "$L.log" 2>&1
rc=$?
end=$(date +%s)
echo "end $(date -Is) wall_total_s=$((end-start)) rc=$rc" >> "$L.log"
echo $rc > "$L.rc"
