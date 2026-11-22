#!/usr/bin/env bash
# run_probe2.sh: probe_minframe2.cpp through each revision's own nx-build recipe (its wrap and its RTL):
# 15168e14 (the true base), 4ceba3d4's RTL (the clone at ce61b2a2, the tests commit on it) and the head clone
set -u
P=<scratch>/r2/probe2
for pair in 15168e14:c2-15168 4ceba3d4:c2-base head:c2-final; do
  tag=${pair%%:*}; S=<scratch>/r2/${pair#*:}/tb/verilator/avtp_rxmon
  echo "$tag $(git -C $S rev-parse --short=8 HEAD)"
  cmd=$(make -s -n -C $S nx-build NX_MDIR=$P/obj_$tag | head -1)
  ( cd $S && eval "${cmd/sim_main_nx.cpp/$P/probe_minframe2.cpp}" ) > $P/build_$tag.log 2>&1; echo "build $tag rc=$?"
  ( cd $S && $P/obj_$tag/Vavtp_rxmon_nx_sim ) > $P/$tag.log 2>&1; echo "run $tag rc=$?"
  grep PROBE $P/$tag.log > $P/$tag.probe.txt
done
