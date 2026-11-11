#!/bin/bash
# campaign unit 0 at 267fc9815d386cd955e05cf3f1e1c17435824b70: seed 1, load none, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c1
date -u +%FT%TZ > <scratch>/camp0/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1 --seed 1 --load none --out <scratch>/camp0/run > <scratch>/camp0/console.log 2>&1
echo $? > <scratch>/camp0/rc
date -u +%FT%TZ > <scratch>/camp0/end.txt
