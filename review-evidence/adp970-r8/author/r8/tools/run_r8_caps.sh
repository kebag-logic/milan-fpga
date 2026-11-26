#!/bin/bash
# run_r8_caps.sh: the two firmware-boundary-capture legs, as rtl-fast.yml runs them
. $VALIDATION_STORAGE/adp970-a847-scratch/env.sh
S=$VALIDATION_STORAGE/adp970-a847-scratch; cd $VALIDATION_STORAGE/adp970-a847
for leg in 0 1; do
  (python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg "$leg/2" \
     --capture-out "$S/r8/cap-$leg" > "$S/r8/cap-$leg.log" 2>&1; echo "rc=$?" >> "$S/r8/cap-$leg.log") &
done
wait
