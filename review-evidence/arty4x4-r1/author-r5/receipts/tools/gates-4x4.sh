#!/bin/bash
S=$VALIDATION_STORAGE/arty4x4-a863; G=$S/gates/final
mkdir -p $G; cd $LANES/arty-4x4
git rev-parse HEAD > $G/head
B='import sys; sys.path.insert(0, "tb/verilator/ctrl_split_boot"); import run; run.JOBS=4; raise SystemExit(run.main())'
R='import sys; sys.path.insert(0, "tb/verilator/ctrl_region_decode"); import run; run.JOBS=4; raise SystemExit(run.main())'
E=$S/tools/run-env.sh
$E python3 -B -c "$B" --shape endstation_arty_split_4x4 --interfaces 1 --build-dir $G/boot-4x4 > $G/boot-4x4.log 2>&1; echo "boot-4x4 $?" >> $G/rc
$E python3 -B tb/verilator/ctrl_split_boot/run.py --native-controls --shape endstation_arty_split_4x4 --interfaces 1 --build-dir $G/boot-controls-4x4 > $G/boot-native-controls-4x4.log 2>&1; echo "boot-native-controls-4x4 $?" >> $G/rc
$E python3 -B -c "$R" --shape endstation_arty_split_4x4 --self-test --build-dir $G/region-4x4 > $G/region-4x4.log 2>&1; echo "region-4x4 $?" >> $G/rc
echo done >> $G/rc
