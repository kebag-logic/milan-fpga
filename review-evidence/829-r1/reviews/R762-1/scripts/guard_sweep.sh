#!/bin/bash
# usage: guard_sweep.sh <scratch> <outfile> ; runs the isolated PHC-load arm per guard and pad index
for g in keep 188 170; do
  cd "$1/gp_$g/tb/verilator/gptp_txts" || exit 2
  for idx in 8 9 10 12 14 18 22; do
    ( out=$(PROBE_IDX=$idx ./obj_mii/Vgptp_txts_sim 25 2>&1 | grep -E "phc window: (that frame|the history|the load)|RESULT" | sed 's/^ *//' | tr '\n' ';')
      echo "guard=$g pad_idx=$idx $out" >> "$2" ) &
    while [ "$(jobs -r | wc -l)" -ge 7 ]; do wait -n; done
  done
  wait
done
