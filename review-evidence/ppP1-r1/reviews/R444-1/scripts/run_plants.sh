#!/usr/bin/env bash
# R444-1: plant each probe in its scratch copy, build the bench, run D3KR.
# Usage: run_plants.sh PACKET_DIR   (copies at scratch/plant{T,S1,S2})
P=$1; S=$P/scratch; R=$P/receipts
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
pids=()
for pair in plantT:T1_torn_crc_truncated plantS1:S1_blank_name_applies_stale_buffer plantS2:S2_ptof_valid_survives_reset; do
  d=${pair%%:*}; n=${pair#*:}
  python3 $P/scripts/plant.py $S/$d $n > $R/plant_$n.log 2>&1 || { echo "plant rc=$?" >> $R/plant_$n.log; continue; }
  (cd $S/$d && git diff --stat >> $R/plant_$n.log; git diff > $R/plant_$n.diff)
  (cd $S/$d/tb/pp_top && make gsi-build >> $R/plant_$n.build.log 2>&1; echo "build rc=$?" >> $R/plant_$n.log)
  (cd $S/$d/tb/pp_top && ./obj_dir/Vpp_top_sim --cuts-only > $R/plant_$n.cuts.log 2>&1; echo "cuts rc=$?" >> $R/plant_$n.log) &
  pids+=($!)
done
wait "${pids[@]}"
echo ALLDONE >> $R/plants_done.txt
