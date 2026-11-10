#!/bin/bash
# campaign unit 3 at 107f3f95deaa69c7903954269a4eede26537990d: seed 4, the composed load, to the second ANNOUNCE (#868)
. <scratch>/env.sh
cd <scratch>/c3
date -u +%FT%TZ > <scratch>/camp3/start.txt
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir <scratch>/b1x1c --seed 4 --load composed --out <scratch>/camp3/run > <scratch>/camp3/console.log 2>&1
echo $? > <scratch>/camp3/rc
date -u +%FT%TZ > <scratch>/camp3/end.txt
