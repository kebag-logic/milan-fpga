#!/usr/bin/env bash
# launch.sh <job> <cpus>: start one round-2 job in its own pinned unit (shard0..3, cov, plants)
set -eu
T=/data-2/milan/tmp/opt-a837-r2; job=$1; export U_CPUS=$2
E="source $T/bin/env.sh &&"
case $job in
  shard[0-3]) k=${job#shard}; mkdir -p $T/cwd-s$k
    exec $T/bin/unit.sh $job $T/cwd-s$k $T/logs/fw-shard-$k.log bash -c "$E exec python3 $T/c-s$k/sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $k/4 --build-dir $T/fw-shard-$k" ;;
  cov) exec $T/bin/unit.sh cov $T/c-cov $T/logs/coverage-check.log bash -c "$E exec python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $T/coverage" ;;
  plants) mkdir -p $T/cwd-p
    exec $T/bin/unit.sh plants $T/cwd-p $T/logs/plants.log bash -c "$E python3 -I $T/bin/plant_proof.py $T/c-old $T/plant-old old > $T/logs/plant-old.log 2>&1; echo old-rc=\$? >> $T/logs/plant-old.log; python3 -I $T/bin/plant_proof.py $T/c-new $T/plant-new new > $T/logs/plant-new.log 2>&1; r=\$?; echo new-rc=\$r >> $T/logs/plant-new.log; grep -q old-rc=0 $T/logs/plant-old.log && exit \$r || exit 9" ;;
esac
