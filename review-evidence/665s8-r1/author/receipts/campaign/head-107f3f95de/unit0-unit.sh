#!/bin/bash
# campaign unit 0 at 107f3f95deaa69c7903954269a4eede26537990d: seed 1, no load, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c3
date -u +%FT%TZ > <scratch>/camp0/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1c --seed 1 --load none --out <scratch>/camp0/run > <scratch>/camp0/console.log 2>&1
echo $? > <scratch>/camp0/rc
date -u +%FT%TZ > <scratch>/camp0/end.txt
