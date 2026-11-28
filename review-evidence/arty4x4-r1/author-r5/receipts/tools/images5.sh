#!/bin/bash
# Round 5's image identity and the 4x4 boot at the checkout's head. usage: images5.sh (cwd = checkout root)
G=$VALIDATION_STORAGE/arty4x4-a863/gates5; T=$VALIDATION_STORAGE/arty4x4-a863/tools
git rev-parse HEAD > $G/images5.head
python3 -B $T/identity.py head $G/identity-head > $G/identity-head.log 2>&1; echo "identity rc=$?" >> $G/images5.rc
python3 -B $T/product.py endstation_arty_split_4x4 $G/p4x4 > $G/p4x4.log 2>&1; echo "product-4x4 rc=$?" >> $G/images5.rc
python3 -B -c 'import sys; sys.path.insert(0, "tb/verilator/ctrl_split_boot"); import run; run.JOBS=4; raise SystemExit(run.main())' --shape endstation_arty_split_4x4 --interfaces 1 --build-dir $G/boot-4x4 > $G/boot-4x4.log 2>&1; echo "boot-4x4 rc=$?" >> $G/images5.rc
python3 -B tb/verilator/ctrl_split_boot/run.py --native-controls --shape endstation_arty_split_4x4 --interfaces 1 --build-dir $G/boot-controls-4x4 > $G/boot-native-controls-4x4.log 2>&1; echo "boot-native-controls-4x4 rc=$?" >> $G/images5.rc
echo DONE >> $G/images5.rc
