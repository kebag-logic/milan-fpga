#!/bin/sh
# Reproduce this round's executions. T: a checkout of 15c32d1b with its
# submodules at the recorded gitlinks; P: this packet. Verilator 5.050 first on PATH.
set -u; T=$1; P=$(cd "$(dirname "$0")/.." && pwd)
cd "$T"
python3 -I scripts/suite_shards.py --selftest
for i in $(seq 0 16); do echo "## shard $i/17"; bash scripts/run_all_suites.sh --ci-pieces --shard $i/17 --list; echo "rc=$?"; done > /tmp/shard_lists_17.log
bash scripts/run_all_suites.sh --list > /tmp/suite_inventory.log
python3 -I "$P/scripts/check_shard_placement.py" /tmp/shard_lists_17.log /tmp/suite_inventory.log
"$P/scripts/bg_run.sh" avtp_rxmon_make_run "$T/tb/verilator/avtp_rxmon" make VERILATOR_JOBS=4 run
"$P/scripts/bg_run.sh" crf_rx_make_all "$T/tb/verilator/crf_rx" make VERILATOR_JOBS=4 all
for l in nxn nxn8 nxn4c nxndv; do "$P/scripts/bg_run.sh" milan_dp_$l "$T/tb/verilator/milan_dp" sh -c "make VERILATOR_JOBS=4 build-$l && make exec-$l"; done
"$P/scripts/bg_run.sh" capture_coherence_dp "$T/tb/verilator/capture_coherence" make VERILATOR_JOBS=8 dp
