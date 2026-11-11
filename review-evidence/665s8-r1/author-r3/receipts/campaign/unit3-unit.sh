#!/bin/bash
# campaign unit 3 at 267fc9815d386cd955e05cf3f1e1c17435824b70: seed 4, load composed, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c1
date -u +%FT%TZ > <scratch>/camp3/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1 --seed 4 --load composed --out <scratch>/camp3/run > <scratch>/camp3/console.log 2>&1
echo $? > <scratch>/camp3/rc
date -u +%FT%TZ > <scratch>/camp3/end.txt
