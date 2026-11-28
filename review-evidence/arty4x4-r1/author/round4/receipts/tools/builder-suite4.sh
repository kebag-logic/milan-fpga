#!/bin/bash
S=$VALIDATION_STORAGE/arty4x4-a863
cd $LANES/arty-4x4
git rev-parse HEAD > $S/gates4/test_builder.head
$S/tools/run-env.sh python3 -u -B sw/builder/test_builder.py > $S/gates4/test_builder.log 2>&1
echo $? > $S/gates4/test_builder.rc
