#!/bin/bash
# campaign unit 1 at 267fc9815d386cd955e05cf3f1e1c17435824b70: seed 2, load none, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c1
date -u +%FT%TZ > <scratch>/camp1/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1 --seed 2 --load none --out <scratch>/camp1/run > <scratch>/camp1/console.log 2>&1
echo $? > <scratch>/camp1/rc
date -u +%FT%TZ > <scratch>/camp1/end.txt
