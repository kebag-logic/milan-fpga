#!/bin/sh
# Run the focused parent consumer gates in a scratch parent whose
# gptp-processor gitlink is staged at the reviewed head.
# usage: parent_gates.sh PARENT RECEIPT_DIR VERILATOR_BIN_DIR
set -u
parent=$1; out=$2; vbin=$3
export PATH="$vbin:$PATH" VERILATOR_JOBS=4 TMPDIR="$out/../../scratch/tmp"
run() { name=$1; shift; ( cd "$parent" && /usr/bin/time -v "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) ; }
( cd "$parent" && git rev-parse HEAD; git ls-files -s gptp-processor; git -C gptp-processor rev-parse HEAD; verilator --version ) > "$out/identity.txt" 2>&1
run py_idiom python3 scripts/check_py_idiom.py &
run gptp_shadow make -C tb/verilator/gptp_shadow -j4 &
( cd "$parent/tb/verilator/milan_dp" && make ltn_rom.hex ucode.hex gptp_ucode.hex > "$out/milan_dp_prereq.log" 2>&1 )
run milan_dp_gptp make -C tb/verilator/milan_dp gptp &
run milan_dp_gptp_lat make -C tb/verilator/milan_dp gptp-lat &
wait
echo done > "$out/ALL.done"
