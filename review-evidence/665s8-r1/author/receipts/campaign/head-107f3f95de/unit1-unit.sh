#!/bin/bash
# campaign unit 1 at 107f3f95deaa69c7903954269a4eede26537990d: seed 2, no load, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c3
date -u +%FT%TZ > <scratch>/camp1/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1c --seed 2 --load none --out <scratch>/camp1/run > <scratch>/camp1/console.log 2>&1
echo $? > <scratch>/camp1/rc
date -u +%FT%TZ > <scratch>/camp1/end.txt
