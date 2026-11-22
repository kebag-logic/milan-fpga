#!/usr/bin/env bash
# run_probe.sh: probe_minframe.cpp through the fan-out recipe on the head RTL (c2-final) and the base RTL (4ceba3d4's
# monitor and depacketizer), each the shortest frame whose PDU the receive stack delivers
set -u
P=<scratch>/r2/probe
for which in head base; do
  S=<scratch>/r2/c2-final/tb/verilator/avtp_rxmon
  extra=""
  if [ $which = base ]; then
    git -C <lane> show 4ceba3d4:hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv > $P/base_depkt.sv
    git -C <lane> show 4ceba3d4:hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv > $P/base_mon.sv
    extra="DEPKT_SRC=$P/base_depkt.sv RXMON_SRC=$P/base_mon.sv"
  fi
  cmd=$(make -s -n -C $S fanout-build FO_MDIR=$P/obj_$which $extra | head -1)
  ( cd $S && eval "${cmd/sim_fanout.cpp/$P/probe_minframe.cpp}" ) > $P/build_$which.log 2>&1; echo "build $which rc=$?"
  ( cd $S && $P/obj_$which/Vavtp_rxmon_fanout ) > $P/$which.log 2>&1; echo "run $which rc=$?"
  grep PROBE $P/$which.log > $P/$which.probe.txt
done
