#!/bin/bash
# q9: drop bit 19 of OFFSET_FOLD_C row 6 (32'h8008_0040 -> 32'h8000_0040), then
# (1) run the full KL_maap unit harness, (2) show a 2^18-apart MAC pair whose first
# blocks overlap under q9 but not at the head. Usage: q9_probe.sh <repo> <work> <scripts>
# Needs VERILATOR (pinned 5.050) in the environment.
set -u; R=$1; W=$2; S=$3; mkdir -p $W
sed "s/32'h8008_0040/32'h8000_0040/" $R/hdl/ieee1722/maap/KL_maap.sv > $W/q9.sv
make -s -C $R/tb/verilator/maap build MAAP_RTL=$W/q9.sv MDIR=$W/obj_q9_unit VERILATOR=$VERILATOR VERILATOR_JOBS=4 >/dev/null 2>&1 || { echo "q9 unit build failed"; exit 2; }
for v in head q9; do src=$([ $v = head ] && echo $R/hdl/ieee1722/maap/KL_maap.sv || echo $W/q9.sv)
  $VERILATOR --cc --exe --build -j 4 --top-module KL_maap -GCLK_FREQ_HZ_P=10000 -Wno-fatal -Wno-lint -Wno-style \
    -Mdir $W/fo_$v $src $S/first_offsets.cpp -o first_offsets >/dev/null 2>&1 || { echo "$v harness build failed"; exit 2; }; done
python3 -I $S/pow2_pair.py $W/q9.sv 18 > $W/pow2.txt
echo "q9 (row 6 bit 19 dropped) on a 2^18-apart pair:"; $W/fo_q9/first_offsets < $W/pow2.txt
echo "head on the same pair:"; $W/fo_head/first_offsets < $W/pow2.txt
$W/obj_q9_unit/VKL_maap_sim > $W/q9_unit.out; echo "q9 full unit harness rc=$?: $(tail -1 $W/q9_unit.out)"
