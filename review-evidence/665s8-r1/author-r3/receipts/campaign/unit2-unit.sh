#!/bin/bash
# campaign unit 2 at 267fc9815d386cd955e05cf3f1e1c17435824b70: seed 3, load composed, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c1
date -u +%FT%TZ > <scratch>/camp2/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1 --seed 3 --load composed --out <scratch>/camp2/run > <scratch>/camp2/console.log 2>&1
echo $? > <scratch>/camp2/rc
date -u +%FT%TZ > <scratch>/camp2/end.txt
